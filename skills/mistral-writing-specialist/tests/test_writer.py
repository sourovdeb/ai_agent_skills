import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import writer as w


class FakeAPI:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.requests = []
    def request(self, method, endpoint, payload=None):
        self.requests.append((method, endpoint, json.loads(json.dumps(payload))))
        return next(self.responses)


def answer(text='A draft.', finish='stop', calls=None):
    message = {'role': 'assistant', 'content': text}
    if calls is not None:
        message['tool_calls'] = calls
    return {'model': 'mock-model', 'usage': {'prompt_tokens': 10, 'completion_tokens': 5},
            'choices': [{'message': message, 'finish_reason': finish}]}


def call(name='get_project_context', args=None, id='t1'):
    return {'id': id, 'type': 'function', 'function': {'name': name,
            'arguments': json.dumps(args or {'section': 'canon'})}}


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'story.db'
        w.initialize(self.path, w.ROOT / 'knowledge/story-bible.template.json')
        self.db = w.connect(self.path)
    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()
    def stage(self, call_id='stage', revision=0):
        return w.execute_tool(self.db, call_id, 'stage_canon_update', {
            'section': 'canon', 'content_json': '{"facts": [{"id": "C1", "fact": "Mara has the key"}]}',
            'reason': 'Author review requested', 'expected_revision': revision})
    def test_initial_sections(self):
        self.assertEqual(set(w.export_project(self.db)['sections']), set(w.SECTIONS))
    def test_init_never_overwrites(self):
        with self.assertRaises(FileExistsError):
            w.initialize(self.path, w.ROOT / 'knowledge/story-bible.template.json')
    def test_missing_database(self):
        with self.assertRaises(ValueError):
            w.connect(self.path.parent / 'missing.db')
    def test_read_revision(self):
        result = w.execute_tool(self.db, 'read1', 'get_project_context', {'section': 'canon'})
        self.assertEqual(result['revision'], 0)
    def test_stage_is_not_approval(self):
        self.stage()
        self.assertEqual(w.export_project(self.db)['sections']['canon']['facts'], [])
    def test_approval_changes_canon(self):
        p = self.stage()
        self.assertEqual(w.approve(self.db, p['proposal_id'])['revision'], 1)
    def test_approval_retains_history(self):
        p = self.stage(); w.approve(self.db, p['proposal_id'])
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM history').fetchone()[0], 1)
    def test_approval_is_idempotent(self):
        p = self.stage(); w.approve(self.db, p['proposal_id'])
        self.assertEqual(w.approve(self.db, p['proposal_id'])['status'], 'already_approved')
    def test_stale_stage_rejected(self):
        p = self.stage(); w.approve(self.db, p['proposal_id'])
        with self.assertRaises(ValueError): self.stage('stage2', revision=0)
    def test_conflicting_approvals_rejected(self):
        p1 = self.stage('a'); p2 = self.stage('b')
        w.approve(self.db, p1['proposal_id'])
        with self.assertRaises(ValueError): w.approve(self.db, p2['proposal_id'])
    def test_duplicate_call_one_proposal(self):
        self.assertEqual(self.stage(), self.stage())
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM proposals').fetchone()[0], 1)
    def test_duplicate_id_different_action_rejected(self):
        self.stage('same')
        with self.assertRaises(ValueError):
            w.execute_tool(self.db, 'same', 'get_project_context', {'section': 'canon'})
    def test_unknown_tool_rejected(self):
        with self.assertRaises(ValueError): w.execute_tool(self.db, 'x', 'approve', {})
    def test_unknown_section_rejected(self):
        with self.assertRaises(ValueError):
            w.execute_tool(self.db, 'x', 'get_project_context', {'section': "canon'; DROP TABLE sections;"})
    def test_extra_arguments_rejected(self):
        with self.assertRaises(ValueError):
            w.execute_tool(self.db, 'x', 'get_project_context', {'section': 'canon', 'override': True})
    def test_bool_is_not_revision(self):
        with self.assertRaises(ValueError): self.stage(revision=True)
    def test_invalid_json_rejected(self):
        for text in ('not json', '[]', '{"x": NaN}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                w.execute_tool(self.db, 'bad', 'stage_canon_update', {'section': 'canon',
                    'content_json': text, 'reason': 'Test', 'expected_revision': 0})
    def test_drafts_do_not_become_canon(self):
        w.execute_tool(self.db, 'draft', 'save_draft', {'title': '../../not-a-path', 'content': 'A scene.'})
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM drafts').fetchone()[0], 1)
        self.assertEqual(w.export_project(self.db)['sections']['canon']['facts'], [])
    def test_mocked_tool_round_trip(self):
        api = FakeAPI([answer(None, calls=[call()]), answer('The canon is empty.')])
        result = w.run(api, self.db, 'continuity', 'Audit the supplied facts.')
        self.assertEqual(result['calls'], 2)
        self.assertEqual(api.requests[1][2]['messages'][-1]['role'], 'tool')
        self.assertEqual(result['model'], 'mock-model')
    def test_malformed_tool_returns_error_not_exec(self):
        api = FakeAPI([answer(None, calls=[call('shell', {'command': 'delete'})]), answer()])
        w.run(api, self.db, 'draft', 'Draft.')
        self.assertIn('not_executed', api.requests[1][2]['messages'][-1]['content'])
    def test_truncation_is_explicit(self):
        self.assertEqual(w.run(FakeAPI([answer(finish='length')]), self.db, 'draft', 'Draft.')['status'],
                         'needs_continuation')
    def test_final_call_disables_tools(self):
        cfg = w.read_json(w.ROOT / 'config.json'); cfg['max_calls'] = 1
        api = FakeAPI([answer()]); w.run(api, self.db, 'draft', 'Draft.', config=cfg)
        self.assertEqual(api.requests[0][2]['tool_choice'], 'none')
    def test_final_call_tool_violation_does_not_execute(self):
        cfg = w.read_json(w.ROOT / 'config.json'); cfg['max_calls'] = 1
        api = FakeAPI([answer(None, calls=[call()])])
        with self.assertRaises(ValueError): w.run(api, self.db, 'draft', 'Draft.', config=cfg)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM receipts').fetchone()[0], 0)
    def test_request_budget(self):
        cfg = w.read_json(w.ROOT / 'config.json'); cfg['max_request_bytes'] = 2
        api = FakeAPI([])
        with self.assertRaises(ValueError): w.run(api, self.db, 'draft', 'Draft.', config=cfg)
        self.assertEqual(api.requests, [])
    def test_sequential_tools(self):
        api = FakeAPI([answer()]); w.run(api, self.db, 'draft', 'Draft.')
        self.assertFalse(api.requests[0][2]['parallel_tool_calls'])


class PackageTests(unittest.TestCase):
    def test_all_json_files_parse(self):
        for path in w.ROOT.rglob('*.json'):
            if 'private' not in path.parts: w.read_json(path)
    def test_every_mode_has_method(self):
        for mode in w.MODES:
            self.assertIn('ACTIVE METHOD', w.instructions(mode, compact=True))
    def test_function_schema_matches_handlers(self):
        tools = w.tool_definitions()
        self.assertEqual({t['function']['name'] for t in tools},
                         {'get_project_context', 'stage_canon_update', 'save_draft'})
        for tool in tools:
            schema = tool['function']['parameters']
            self.assertEqual(set(schema['required']), set(schema['properties']))
            self.assertFalse(schema['additionalProperties'])
    def test_compiled_prompt_contains_all_methods(self):
        compiled = (w.ROOT / 'prompts/studio-agent.txt').read_text()
        self.assertTrue(compiled.startswith((w.ROOT / 'prompts/director.md').read_text().rstrip()))
        for mode in set(w.SKILLS.values()):
            skill = (w.ROOT / 'writing-skills' / mode / 'SKILL.md').read_text().split('---', 2)[2].strip()
            self.assertIn(skill, compiled)
    def test_compose_never_calls_network(self):
        with patch.object(w.MistralAPI, 'request', side_effect=AssertionError('No network')), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(w.main(['compose', '--input', str(w.ROOT / 'examples/brief.txt')]), 0)
    def test_deploy_dry_run_has_no_local_functions(self):
        stream = io.StringIO()
        with patch.object(w.MistralAPI, 'request', side_effect=AssertionError('No network')), contextlib.redirect_stdout(stream):
            w.main(['deploy', '--dry-run'])
        self.assertEqual(json.loads(stream.getvalue())['tools'], [])
    def test_cloud_requires_explicit_flag(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            w.main(['models'])
        self.assertEqual(error.exception.code, 2)
    def test_missing_key_fails(self):
        with self.assertRaises(ValueError): w.MistralAPI('')
    def test_endpoint_allowlist(self):
        with self.assertRaises(ValueError): w.MistralAPI('test-only-not-a-real-key').request('POST', '/unknown')
    def test_outputs_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'out.txt'; w.write_new(path, 'original')
            with self.assertRaises(FileExistsError): w.write_new(path, 'replacement')
            self.assertEqual(path.read_text(), 'original')
    def test_invalid_template_has_no_db_side_effect(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'bad.json'; path.write_text('{"sections": {}}')
            db = Path(tmp) / 'bad.db'
            with self.assertRaises(ValueError): w.initialize(db, path)
            self.assertFalse(db.exists())
    def test_api_key_not_in_composed_packet(self):
        with patch.dict('os.environ', {'MISTRAL_API_KEY': 'PRIVATE_TEST_MARKER'}):
            self.assertNotIn('PRIVATE_TEST_MARKER', w.instructions('draft'))


if __name__ == '__main__':
    unittest.main()
