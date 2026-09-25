#!/usr/bin/env python3
"""Mistral writing workbench. Python 3.10+, standard library only.
Local state is private; network use requires an explicit --allow-cloud flag.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import time
import uuid
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
SECTIONS = ('braindump', 'genre', 'style', 'synopsis', 'characters', 'worldbuilding',
            'outline', 'timeline', 'canon', 'sources', 'session')
MODES = ('bible', 'outline', 'draft', 'edit', 'continuity', 'research', 'audiobook')
SKILLS = {'bible': 'story-bible', 'outline': 'story-bible', 'draft': 'scene-draft',
          'edit': 'editor', 'continuity': 'continuity', 'research': 'research',
          'audiobook': 'audiobook'}
MAX_TEXT = 60000


def loads(text: str):
    def reject(value):
        raise ValueError('Non-finite JSON numbers are not supported')
    return json.loads(text, parse_constant=reject)


def dump(value) -> str:
    return json.dumps(value, ensure_ascii=False, allow_nan=False)


def read_json(path: Path):
    return loads(path.read_text(encoding='utf-8'))


def connect(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise ValueError('Project not found; run init first')
    db = sqlite3.connect(str(path), timeout=10)
    db.row_factory = sqlite3.Row
    return db


def initialize(path: Path, template: Path) -> None:
    data = read_json(template)
    if set(data.get('sections', {})) != set(SECTIONS):
        raise ValueError('Template must contain every named section, with no extras')
    if any(not isinstance(v, dict) for v in data['sections'].values()):
        raise ValueError('Each section must be a JSON object')
    if len(dump(data)) > MAX_TEXT:
        raise ValueError('Template too large; start with a focused project')
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    db = sqlite3.connect(str(path))
    try:
        with db:
            db.executescript('''
            CREATE TABLE sections(name TEXT PRIMARY KEY, content TEXT NOT NULL, revision INTEGER NOT NULL);
            CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE proposals(id TEXT PRIMARY KEY, section TEXT NOT NULL, content TEXT NOT NULL,
              reason TEXT NOT NULL, base_revision INTEGER NOT NULL, status TEXT NOT NULL);
            CREATE TABLE history(section TEXT, revision INTEGER, content TEXT, PRIMARY KEY(section,revision));
            CREATE TABLE drafts(id TEXT PRIMARY KEY, title TEXT, content TEXT);
            CREATE TABLE receipts(id TEXT PRIMARY KEY, signature TEXT NOT NULL, result TEXT NOT NULL);
            ''')
            db.execute('INSERT INTO meta VALUES (?,?)', ('project', dump(data.get('project', {}))))
            db.executemany('INSERT INTO sections VALUES (?,?,0)',
                           [(k, dump(v)) for k, v in data['sections'].items()])
    finally:
        db.close()


def tool_definitions():
    return read_json(ROOT / 'tools.json')


def validate_call(name: str, args: dict) -> None:
    schemas = {t['function']['name']: t['function']['parameters'] for t in tool_definitions()}
    if name not in schemas:
        raise ValueError('Unknown tool; arbitrary commands are not supported')
    schema = schemas[name]
    if not isinstance(args, dict) or set(args) != set(schema['required']):
        raise ValueError('Tool arguments must match the required fields exactly')
    for key, value in args.items():
        rule = schema['properties'][key]
        expected = str if rule['type'] == 'string' else int
        if type(value) is not expected:
            raise ValueError(f'Wrong type for {key}')
        if 'enum' in rule and value not in rule['enum']:
            raise ValueError(f'Invalid {key}')
        if isinstance(value, str) and (not value.strip() or len(value) > MAX_TEXT):
            raise ValueError(f'Empty or oversized {key}')
        if type(value) is int and value < 0:
            raise ValueError(f'Negative {key}')


def execute_tool(db: sqlite3.Connection, call_id: str, name: str, args: dict) -> dict:
    """Transactions + receipts prevent repeated calls from duplicating local writes."""
    validate_call(name, args)
    signature = hashlib.sha256(dump([name, args]).encode()).hexdigest()
    with db:
        db.execute('BEGIN IMMEDIATE')
        old = db.execute('SELECT * FROM receipts WHERE id=?', (call_id,)).fetchone()
        if old:
            if old['signature'] != signature:
                raise ValueError('Call ID was reused with different arguments')
            return loads(old['result'])
        if name == 'get_project_context':
            row = db.execute('SELECT * FROM sections WHERE name=?', (args['section'],)).fetchone()
            result = {'section': row['name'], 'revision': row['revision'],
                      'content': loads(row['content']), 'authority': 'user-maintained project data'}
        elif name == 'stage_canon_update':
            content = loads(args['content_json'])
            if not isinstance(content, dict):
                raise ValueError('content_json must encode an object, not a list or string')
            row = db.execute('SELECT revision FROM sections WHERE name=?', (args['section'],)).fetchone()
            if row['revision'] != args['expected_revision']:
                raise ValueError('Stale section revision; read current context first')
            proposal = uuid.uuid4().hex
            db.execute('INSERT INTO proposals VALUES (?,?,?,?,?,?)',
                       (proposal, args['section'], dump(content), args['reason'], row['revision'], 'pending'))
            result = {'proposal_id': proposal, 'status': 'pending', 'canon_changed': False}
        else:  # save_draft: create a new version, never replace an existing one.
            draft = uuid.uuid4().hex
            db.execute('INSERT INTO drafts VALUES (?,?,?)', (draft, args['title'], args['content']))
            result = {'draft_id': draft, 'status': 'saved_locally', 'canon_changed': False}
        db.execute('INSERT INTO receipts VALUES (?,?,?)', (call_id, signature, dump(result)))
        return result


def approve(db: sqlite3.Connection, proposal_id: str) -> dict:
    """Host-only operation. Approval is deliberately NOT exposed as an LLM tool."""
    with db:
        db.execute('BEGIN IMMEDIATE')
        p = db.execute('SELECT * FROM proposals WHERE id=?', (proposal_id,)).fetchone()
        if not p:
            raise ValueError('Proposal not found')
        if p['status'] == 'approved':
            return {'proposal_id': proposal_id, 'status': 'already_approved'}
        row = db.execute('SELECT * FROM sections WHERE name=?', (p['section'],)).fetchone()
        if row['revision'] != p['base_revision']:
            raise ValueError('Approval conflict: section changed since proposal; create a new proposal')
        db.execute('INSERT INTO history VALUES (?,?,?)', (row['name'], row['revision'], row['content']))
        db.execute('UPDATE sections SET content=?, revision=revision+1 WHERE name=?',
                   (p['content'], p['section']))
        db.execute("UPDATE proposals SET status='approved' WHERE id=?", (proposal_id,))
        return {'proposal_id': proposal_id, 'status': 'approved', 'revision': row['revision'] + 1}


def instructions(mode: str, compact: bool = False) -> str:
    core = ROOT / 'prompts' / ('compact.md' if compact else 'director.md')
    method = ROOT / 'writing-skills' / SKILLS[mode] / 'SKILL.md'
    return core.read_text(encoding='utf-8') + '\n\nACTIVE METHOD\n' + method.read_text(encoding='utf-8')


class APIError(RuntimeError):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Do not forward a credential to any redirected host.


class MistralAPI:
    """Fixed official endpoint. No SDK, provider gateway, or implicit model escalation."""
    def __init__(self, key: str):
        if not key.strip():
            raise ValueError('Set MISTRAL_API_KEY in your environment; do not paste it into a prompt')
        self.key = key
        self.opener = urllib.request.build_opener(NoRedirect())

    def request(self, method: str, endpoint: str, payload=None):
        allowed = {('GET', '/models'), ('POST', '/chat/completions'), ('POST', '/agents')}
        if (method, endpoint) not in allowed:
            raise ValueError('Endpoint is not allowlisted')
        body = None if payload is None else dump(payload).encode('utf-8')
        request = urllib.request.Request('https://api.mistral.ai/v1' + endpoint, data=body, method=method,
                    headers={'Authorization': 'Bearer ' + self.key, 'Content-Type': 'application/json'})
        for attempt in range(3):
            try:
                with self.opener.open(request, timeout=90) as response:
                    raw = response.read(2_000_001)
                    if len(raw) > 2_000_000:
                        raise APIError('Response too large; request outcome may require checking')
                    return loads(raw.decode('utf-8'))
            except urllib.error.HTTPError as error:
                if error.code == 429 and attempt < 2:
                    delay = error.headers.get('Retry-After', '2')
                    time.sleep(min(10, max(1, float(delay))) if delay.isdigit() else 2)
                    continue
                raise APIError(f'Mistral HTTP {error.code}; no provider switch or blind write retry') from None
            except (urllib.error.URLError, TimeoutError) as error:
                raise APIError('Network failure; outcome unknown. Check Studio before retrying deployment') from None
        raise APIError('Retry limit reached')


def run(api, db, mode: str, text: str, compact=False, config=None) -> dict:
    config = config or read_json(ROOT / 'config.json')
    model = config['model']
    messages = [{'role': 'system', 'content': instructions(mode, compact)},
                {'role': 'user', 'content': text}]
    usage = []
    scope = uuid.uuid4().hex
    for round_number in range(config['max_calls']):
        # A UTF-8 byte ceiling is conservative, but not a tokenizer or price estimate.
        if len(dump(messages).encode('utf-8')) > config['max_request_bytes']:
            raise ValueError('Context budget reached; split the task or export a focused checkpoint')
        payload = {'model': model, 'messages': messages, 'tools': tool_definitions(),
                   'max_tokens': config['max_output_tokens'], 'temperature': config['temperature'],
                   'parallel_tool_calls': False,
                   'tool_choice': 'none' if round_number == config['max_calls'] - 1 else 'auto'}
        response = api.request('POST', '/chat/completions', payload)
        choice = response['choices'][0]
        message = choice['message']
        usage.append(response.get('usage', {}))
        calls = message.get('tool_calls') or []
        if not calls:
            return {'status': 'needs_continuation' if choice.get('finish_reason') == 'length' else 'completed',
                    'model': response.get('model', model), 'content': message.get('content'),
                    'usage_by_call': usage, 'calls': round_number + 1}
        if len(calls) > 8:
            raise ValueError('Tool batch limit exceeded')
        if round_number == config['max_calls'] - 1:
            raise ValueError('Model requested tools after the final-call budget; no tools were executed')
        messages.append({'role': 'assistant', 'content': message.get('content'), 'tool_calls': calls})
        for call in calls:
            try:
                result = execute_tool(db, scope + ':' + call['id'], call['function']['name'],
                                      loads(call['function']['arguments']))
            except (ValueError, KeyError, TypeError) as error:
                result = {'error': str(error), 'status': 'not_executed'}
            messages.append({'role': 'tool', 'tool_call_id': call['id'], 'content': dump(result)})
    raise ValueError('Call budget exhausted')


def export_project(db) -> dict:
    sections = db.execute('SELECT * FROM sections ORDER BY name').fetchall()
    return {'schema_version': '1.0',
            'project': loads(db.execute("SELECT value FROM meta WHERE key='project'").fetchone()[0]),
            'sections': {r['name']: loads(r['content']) for r in sections},
            'section_revisions': {r['name']: r['revision'] for r in sections}}


def write_new(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(text)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=('init', 'compose', 'run', 'proposals', 'approve', 'export', 'models', 'deploy'))
    p.add_argument('--db', type=Path, default=Path('private/story.db'))
    p.add_argument('--template', type=Path, default=ROOT / 'knowledge/story-bible.template.json')
    p.add_argument('--mode', choices=MODES, default='draft')
    p.add_argument('--input', type=Path)
    p.add_argument('--output', type=Path)
    p.add_argument('--proposal')
    p.add_argument('--compact', action='store_true')
    p.add_argument('--allow-cloud', action='store_true')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--web-search', action='store_true')
    p.add_argument('--library-id', action='append', default=[])
    args = p.parse_args(argv)
    config = read_json(ROOT / 'config.json')
    if args.output and args.output.exists():
        raise ValueError('Output already exists; choose a new versioned filename')
    if args.command == 'init':
        initialize(args.db, args.template)
        print('Created local project:', args.db)
        return 0
    if args.command in ('compose', 'run'):
        if not args.input:
            p.error('--input is required')
        if args.input.stat().st_size > config['max_request_bytes']:
            raise ValueError('Input too large; select one scene or excerpt')
        text = args.input.read_text(encoding='utf-8')
        if not text.strip():
            raise ValueError('Input is empty')
        if args.command == 'compose' or args.dry_run:
            output = instructions(args.mode, args.compact) + '\n\nUSER TASK\n' + text
            if args.output:
                write_new(args.output, output)
            else:
                print(output)
            return 0
    if args.command == 'deploy':
        payload = {'name': 'Story Studio - Writing Director',
                   'description': 'Story Bible, scene drafting, editing, continuity, research and narration coaching.',
                   'model': config['model'],
                   'instructions': (ROOT / 'prompts/studio-agent.txt').read_text(encoding='utf-8'),
                   'tools': ([{'type': 'web_search'}] if args.web_search else []) +
                            ([{'type': 'document_library', 'library_ids': args.library_id}] if args.library_id else []),
                   'completion_args': {'temperature': config['temperature'], 'max_tokens': config['max_output_tokens']}}
        # No local functions are registered on this hosted agent: Studio cannot run our SQLite code.
        if args.dry_run:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            return 0
    if args.command in ('run', 'models', 'deploy'):
        if not args.allow_cloud:
            p.error('Network use requires --allow-cloud; use compose or --dry-run without a key')
        api = MistralAPI(os.environ.get('MISTRAL_API_KEY', ''))
        if args.command == 'models':
            print(dump(api.request('GET', '/models')))
            return 0
        if args.command == 'deploy':
            receipt = api.request('POST', '/agents', payload)
            # Save before reporting success. A repeated invocation creates another agent.
            target = args.output or Path('private') / ('agent-' + uuid.uuid4().hex + '.json')
            write_new(target, json.dumps(receipt, indent=2, ensure_ascii=False))
            print(dump({'agent_id': receipt.get('id'), 'receipt': str(target)}))
            return 0
    db = connect(args.db)
    try:
        if args.command == 'run':
            result = run(api, db, args.mode, text, args.compact, config)
        elif args.command == 'proposals':
            result = [dict(row) for row in db.execute('SELECT * FROM proposals ORDER BY rowid')]
        elif args.command == 'approve':
            if not args.proposal:
                p.error('--proposal is required; inspect proposals before approving')
            result = approve(db, args.proposal)
        else:
            result = export_project(db)
        output = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            write_new(args.output, output)
        else:
            print(output)
        return 0
    finally:
        db.close()


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, sqlite3.Error, APIError, KeyError, TypeError) as error:
        print('ERROR:', str(error), file=sys.stderr)
        raise SystemExit(1)
