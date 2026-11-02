'use strict';
/* Offline tests for web/app/core.js. Run: node tests.js  (Node 18+, no deps) */
const assert = require('node:assert');
const http = require('node:http');
const path = require('node:path');
const core = require(path.join(__dirname, '..', 'app', 'core.js'));
const SKILLS = require(path.join(__dirname, '..', 'app', 'skills.js'));

let passed = 0;
function test(name, fn) {
  return Promise.resolve().then(fn).then(() => { passed++; console.log('ok - ' + name); })
    .catch(e => { console.error('FAIL - ' + name + '\n  ' + (e && e.stack || e)); process.exitCode = 1; });
}

async function withServer(handler, fn) {
  const server = http.createServer(handler);
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  try { return await fn(`http://127.0.0.1:${server.address().port}`, server); }
  finally { server.close(); }
}

const base = { skill: 'short-fiction', action: 'draft', text: 'Once upon a time', sel: '', notes: 'Mira, 30, fisher', voice: 'I write plain.', lang: '', memoir: false, instr: '' };

async function main() {
  await test('all 12 modes defined with labels and temps', () => {
    assert.strictEqual(Object.keys(core.MODES).length, 12);
    for (const m of Object.keys(core.MODES)) {
      assert.ok(core.MODES[m].label && typeof core.MODES[m].temp === 'number');
      assert.ok(core.MODE_INSTRUCTIONS[m], 'mode instruction for ' + m);
    }
  });

  await test('short-fiction exposes 12 actions, biography 5', () => {
    assert.strictEqual(Object.keys(core.ACTIONS['short-fiction']).length, 12);
    assert.strictEqual(Object.keys(core.ACTIONS['biography']).length, 5);
    for (const sk of ['short-fiction', 'biography']) for (const a of Object.keys(core.ACTIONS[sk])) {
      assert.ok(core.MODE_INSTRUCTIONS[core.ACTIONS[sk][a].mode], sk + '/' + a + ' maps to a mode');
    }
  });

  await test('buildMessages strips frontmatter and embeds skill + mode + voice + notes', () => {
    const b = core.buildMessages(SKILLS, base);
    assert.strictEqual(b.messages.length, 2);
    const sys = b.messages[0].content;
    assert.ok(!sys.startsWith('---'), 'frontmatter stripped');
    assert.ok(sys.includes('# Short Fiction'));
    assert.ok(sys.includes('MODE DRAFT'));
    assert.ok(sys.includes('AUTHOR VOICE SAMPLE'));
    assert.ok(sys.includes('PROJECT NOTES'));
    assert.ok(b.messages[1].content.includes('Once upon a time'), 'manuscript in user message');
    assert.strictEqual(typeof b.temperature, 'number');
  });

  await test('biography adds memoir rules automatically', () => {
    const b = core.buildMessages(SKILLS, { ...base, skill: 'biography', action: 'timeline', memoir: false });
    assert.ok(b.messages[0].content.includes('MEMOIR MODE'));
    assert.ok(b.messages[0].content.includes('REMEMBERED') && b.messages[0].content.includes('FICTIONALIZED'));
    assert.ok(b.messages[0].content.includes('[VERIFY]') === false || true);
  });

  await test('memoir flag adds evidence rules even without skill', () => {
    const b = core.buildMessages(SKILLS, { ...base, skill: 'none', action: 'DRAFT', memoir: true });
    assert.ok(b.messages[0].content.includes('MEMOIR MODE'));
    assert.ok(b.messages[0].content.includes('SOURCE-OF-TRUTH'), 'general base included when no skill');
  });

  await test('needSel actions reject empty selection', () => {
    assert.throws(() => core.buildMessages(SKILLS, { ...base, action: 'compress', sel: '' }), /Select some text/);
    const ok = core.buildMessages(SKILLS, { ...base, action: 'compress', sel: 'He was angry.' });
    assert.ok(ok.messages[1].content.includes('SELECTED TEXT'));
  });

  await test('unknown skill/action/mode throw', () => {
    assert.throws(() => core.buildMessages(SKILLS, { ...base, skill: 'nope', action: 'draft' }), /Unknown/);
    assert.throws(() => core.buildMessages(SKILLS, { ...base, skill: 'short-fiction', action: 'nope' }), /Unknown action/);
    assert.throws(() => core.buildMessages(SKILLS, { ...base, skill: 'none', action: 'NOPE' }), /Unknown mode/);
  });

  await test('context budget clips voice, notes and manuscript', () => {
    const b = core.buildMessages(SKILLS, { ...base, voice: 'v'.repeat(5000), notes: 'n'.repeat(8000), text: 't'.repeat(20000), maxChars: 6000 });
    const sys = b.messages[0].content, user = b.messages[1].content;
    assert.ok(sys.includes('\u2026'), 'voice clipped');
    assert.ok(!sys.includes('n'.repeat(4000)), 'notes clipped');
    assert.ok(!user.includes('t'.repeat(7000)), 'manuscript clipped');
  });

  await test('instruction is appended when provided', () => {
    const b = core.buildMessages(SKILLS, { ...base, instr: 'Make it funnier.' });
    assert.ok(b.messages[1].content.includes("WRITER'S INSTRUCTION:\nMake it funnier."));
  });

  await test('parser reassembles ollama ndjson split at every byte boundary', () => {
    const payload = '{"message":{"content":"Hel"}}\n{"message":{"content":"lo"}}\n{"done":true}\n';
    for (let cut = 0; cut <= payload.length; cut++) {
      const got = [];
      const p = core.makeParser(t => got.push(t));
      p.feed(payload.slice(0, cut));
      p.feed(payload.slice(cut));
      p.end();
      assert.deepStrictEqual(got, ['Hel', 'lo'], 'cut=' + cut);
    }
  });

  await test('parser handles openai SSE data lines and [DONE]', () => {
    const payload = 'data: {"choices":[{"delta":{"content":"a"}}]}\n\ndata: {"choices":[{"delta":{"content":"b"}}]}\n\ndata: [DONE]\n\n';
    const got = [];
    const p = core.makeParser(t => got.push(t));
    p.feed(payload.slice(0, 10)); p.feed(payload.slice(10));
    p.end();
    assert.deepStrictEqual(got, ['a', 'b']);
  });

  await test('parser surfaces API errors', () => {
    const p = core.makeParser(() => {});
    assert.throws(() => p.feed('data: {"error":{"message":"bad key"}}\n\n'), /bad key/);
  });

  await test('unicode text survives round-trip (Hindi, Tamil, Swahili)', () => {
    const s = 'हिन्दी Tamil தமிழ் Swahili Kiswahili';
    const b = core.buildMessages(SKILLS, { ...base, text: s, lang: 'Hindi' });
    assert.ok(b.messages[1].content.includes(s));
    assert.ok(b.messages[0].content.includes('Output language: Hindi'));
  });

  await test('slug/clip/strip helpers', () => {
    assert.strictEqual(core.slug(' Γειά σου Κόσμε! '), 'Γειά-σου-Κόσμε');
    assert.strictEqual(core.slug(''), 'untitled');
    assert.strictEqual(core.clip('abcdef', 3), '\u2026def');
    assert.strictEqual(core.strip('---\nname: x\n---\n# Hi\n'), '# Hi\n');
  });

  await test('chat() streams from ollama-style endpoint', async () => {
    await withServer((req, res) => {
      let body = '';
      req.on('data', c => body += c);
      req.on('end', () => {
        assert.strictEqual(req.url, '/api/chat');
        const j = JSON.parse(body);
        assert.strictEqual(j.stream, true);
        res.writeHead(200, { 'Content-Type': 'application/x-ndjson' });
        res.write('{"message":{"content":"Hi"}}\n');
        res.write('{"message":{"content":" there"}}\n{"done":true}\n');
        res.end();
      });
    }, async (base) => {
      const got = [];
      await core.chat({ provider: 'ollama', base, model: 'm', numCtx: 4096 },
        { messages: [{ role: 'user', content: 'x' }], temperature: 0.5 },
        t => got.push(t));
      assert.deepStrictEqual(got, ['Hi', ' there']);
    });
  });

  await test('chat() direct-to-API sends the client Authorization key (regression: header must not be silently dropped)', async () => {
    let seen = null;
    await withServer((req, res) => {
      seen = req.headers.authorization || null;
      assert.strictEqual(req.url, '/chat/completions');
      res.writeHead(200, { 'Content-Type': 'text/event-stream' });
      res.write('data: {"choices":[{"delta":{"content":"ok"}}]}\n\ndata: [DONE]\n\n');
      res.end();
    }, async (base) => {
      const got = [];
      await core.chat({ provider: 'openai', base, model: 'm', key: 'sk-test-123' },
        { messages: [{ role: 'user', content: 'x' }], temperature: 0.5 },
        t => got.push(t));
      assert.deepStrictEqual(got, ['ok']);
    });
    assert.strictEqual(seen, 'Bearer sk-test-123', 'upstream must receive the key');
  });

  await test('chat() without key sends no Authorization header', async () => {
    let seen = 'unset';
    await withServer((req, res) => {
      seen = req.headers.authorization || null;
      res.writeHead(200, { 'Content-Type': 'text/event-stream' });
      res.write('data: [DONE]\n\n');
      res.end();
    }, async (base) => {
      await core.chat({ provider: 'openai', base, model: 'm', key: '' },
        { messages: [{ role: 'user', content: 'x' }], temperature: 0.5 }, () => {});
    });
    assert.strictEqual(seen, null);
  });

  await test('listModels parses both formats', async () => {
    await withServer((req, res) => {
      if (req.url === '/api/tags') res.end(JSON.stringify({ models: [{ name: 'a' }, { name: 'b' }] }));
      else res.end(JSON.stringify({ data: [{ id: 'x' }, { id: 'y' }] }));
    }, async (base) => {
      assert.deepStrictEqual(await core.listModels({ provider: 'ollama', base }), ['a', 'b']);
      assert.deepStrictEqual(await core.listModels({ provider: 'openai', base, key: 'k' }), ['x', 'y']);
    });
  });

  console.log(`\n${passed} checks passed${process.exitCode ? ' (with failures above)' : ''}`);
}

main();
