// src/extension.js — WP AI Studio VS Code Extension
const { getWebviewHTML } = require('./webview');
const vscode = require('vscode');

let panel = null;
const LOG_HISTORY = [];

// ── Activation ────────────────────────────────────────────────────────────────────────────────
function activate(context) {
    context.subscriptions.push(
        vscode.commands.registerCommand('wpai.openPanel', () => openStudio(context)),
        vscode.commands.registerCommand('wpai.siteStatus', () => {
            openStudio(context);
            setTimeout(() => panel?.webview.postMessage({ cmd: 'run_status' }), 500);
        })
    );

    const cfg = vscode.workspace.getConfiguration('wpai');
    if (cfg.get('wordpressUrl')) openStudio(context);
}

// ── Main Panel ──────────────────────────────────────────────────────────────────────────────
function openStudio(context) {
    if (panel) { panel.reveal(); return; }

    panel = vscode.window.createWebviewPanel(
        'wpaiStudio', 'WP AI Studio',
        vscode.ViewColumn.One,
        { enableScripts: true, retainContextWhenHidden: true }
    );

    panel.webview.html = getWebviewHTML();

    panel.webview.onDidReceiveMessage(async msg => {
        switch (msg.cmd) {
            case 'save_settings': saveSettings(msg.data); break;
            case 'load_settings': sendSettings(); break;
            case 'site_status':   await doSiteStatus(); break;
            case 'generate':      await doGenerate(msg.data); break;
            case 'approve_post':  await doApprovePost(msg.data); break;
            case 'schedule_post': await doSchedulePost(msg.data); break;
            case 'list_posts':    await doListPosts(msg.data); break;
            case 'delete_post':   await doDeletePost(msg.data); break;
            case 'chat':          await doChat(msg.data); break;
        }
    }, undefined, context.subscriptions);

    panel.onDidDispose(() => { panel = null; });
    setTimeout(sendSettings, 300);
}

// ── Settings ────────────────────────────────────────────────────────────────────────────────
function getConfig() {
    return vscode.workspace.getConfiguration('wpai');
}

function sendSettings() {
    const c = getConfig();
    panel?.webview.postMessage({
        cmd: 'settings', data: {
            wordpressUrl:  c.get('wordpressUrl'),
            wpUser:        c.get('wpUser'),
            wpAppPassword: c.get('wpAppPassword'),
            pluginKey:     c.get('pluginKey'),
            aiProvider:    c.get('aiProvider'),
            claudeKey:     c.get('claudeKey'),
            deepseekKey:   c.get('deepseekKey'),
            ollamaUrl:     c.get('ollamaUrl'),
            ollamaModel:   c.get('ollamaModel'),
            approvalMode:  c.get('approvalMode'),
            defaultStatus: c.get('defaultStatus'),
        }
    });
}

async function saveSettings(data) {
    const c = getConfig();
    for (const [key, val] of Object.entries(data)) {
        await c.update(key, val, vscode.ConfigurationTarget.Global);
    }
    log('info', 'Settings saved');
    sendSettings();
}

// ── Logging ────────────────────────────────────────────────────────────────────────────────
function log(level, message, detail = '') {
    const entry = { level, message, detail, time: new Date().toLocaleTimeString() };
    LOG_HISTORY.push(entry);
    if (LOG_HISTORY.length > 200) LOG_HISTORY.shift();
    panel?.webview.postMessage({ cmd: 'log', data: entry });
}

// ── WordPress API Calls ─────────────────────────────────────────────────────────────────
async function wpRequest(path, method = 'GET', body = null) {
    const c = getConfig();
    const url  = c.get('wordpressUrl').replace(/\/$/, '');
    const key  = c.get('pluginKey');
    const user = c.get('wpUser');
    const pass = c.get('wpAppPassword');

    const headers = { 'Content-Type': 'application/json' };
    if (key)  headers['X-Sourov-Key'] = key;
    if (user && pass) headers['Authorization'] = 'Basic ' + Buffer.from(`${user}:${pass}`).toString('base64');

    const opts = { method, headers };
    if (body) opts.body = JSON.stringify(body);

    const endpoint = `${url}/wp-json/sourov/v1${path}`;
    log('info', `→ ${method} ${path}`);

    try {
        const fetch = (await import('node-fetch')).default;
        const res = await fetch(endpoint, opts);
        const data = await res.json();
        if (!res.ok) throw new Error(data.message || JSON.stringify(data));
        return data;
    } catch (e) {
        log('error', `WP request failed: ${e.message}`);
        throw e;
    }
}

async function doSiteStatus() {
    try {
        const data = await wpRequest('/status');
        log('info', `Site online: ${data.site} | Posts: ${data.total_posts} | Scheduled: ${data.scheduled_posts}`);
        panel?.webview.postMessage({ cmd: 'status_result', data });
    } catch (e) {
        panel?.webview.postMessage({ cmd: 'status_result', data: { error: e.message } });
    }
}

async function doListPosts(filter = {}) {
    try {
        const q = new URLSearchParams(filter).toString();
        const data = await wpRequest(`/scheduled?${q}`);
        panel?.webview.postMessage({ cmd: 'posts_list', data });
    } catch(e) {
        log('error', 'List posts failed: ' + e.message);
    }
}

async function doDeletePost({ id }) {
    try {
        await wpRequest(`/post/${id}`, 'DELETE');
        log('info', `Deleted post ID:${id}`);
        doListPosts();
    } catch(e) {
        log('error', 'Delete failed: ' + e.message);
    }
}

async function doApprovePost({ postData, schedule }) {
    try {
        log('info', `Approving: "${postData.title}"`);
        const result = await wpRequest('/ai-post', 'POST', {
            ...postData,
            status: schedule ? 'future' : 'publish',
            schedule: schedule || '',
        });
        log('info', `✓ Published → ID:${result.id} | ${result.link}`);
        panel?.webview.postMessage({ cmd: 'post_created', data: result });
    } catch(e) {
        log('error', 'Approve failed: ' + e.message);
    }
}

async function doSchedulePost({ postData, schedule }) {
    try {
        log('info', `Scheduling: "${postData.title}" → ${schedule}`);
        const result = await wpRequest('/ai-post', 'POST', {
            ...postData,
            status: 'future',
            schedule,
        });
        log('info', `✓ Scheduled → ID:${result.id}`);
        panel?.webview.postMessage({ cmd: 'post_created', data: result });
        doListPosts();
    } catch(e) {
        log('error', 'Schedule failed: ' + e.message);
    }
}

// ── AI Providers ────────────────────────────────────────────────────────────────────────────
async function callAI(systemPrompt, userPrompt) {
    const c = getConfig();
    const provider = c.get('aiProvider');
    log('info', `AI generating via ${provider}...`);

    try {
        const fetch = (await import('node-fetch')).default;

        if (provider === 'claude') {
            const res = await fetch('https://api.anthropic.com/v1/messages', {
                method: 'POST',
                headers: {
                    'x-api-key': c.get('claudeKey'),
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'claude-sonnet-4-20250514',
                    max_tokens: 2000,
                    system: systemPrompt,
                    messages: [{ role: 'user', content: userPrompt }],
                }),
            });
            const d = await res.json();
            return d.content[0].text;
        }

        if (provider === 'deepseek') {
            const res = await fetch('https://api.deepseek.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${c.get('deepseekKey')}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'deepseek-chat',
                    messages: [
                        { role: 'system', content: systemPrompt },
                        { role: 'user',   content: userPrompt },
                    ],
                }),
            });
            const d = await res.json();
            return d.choices[0].message.content;
        }

        if (provider === 'ollama') {
            const res = await fetch(`${c.get('ollamaUrl')}/api/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model:  c.get('ollamaModel'),
                    prompt: `${systemPrompt}\n\n${userPrompt}`,
                    stream: false,
                }),
            });
            const d = await res.json();
            return d.response;
        }

        throw new Error(`Unknown provider: ${provider}`);
    } catch(e) {
        log('error', `AI call failed: ${e.message}`);
        throw e;
    }
}

// ── Generate Post ───────────────────────────────────────────────────────────────────────────
async function doGenerate({ topic, tone = 'professional', wordCount = 600 }) {
    panel?.webview.postMessage({ cmd: 'generating', data: { topic } });

    const system = `You are a WordPress content writer. Always respond with ONLY a valid JSON object — no markdown, no explanation.`;
    const user = `Write a complete WordPress blog post about: "${topic}"
Tone: ${tone}. Target length: ${wordCount} words.

Return this exact JSON structure:
{
  "title": "compelling title",
  "content": "full HTML with <h2>, <p>, <ul> tags",
  "meta_desc": "SEO meta description under 160 chars",
  "seo_title": "SEO title under 60 chars",
  "tags": ["tag1", "tag2", "tag3"],
  "excerpt": "2-sentence summary"
}`;

    try {
        let raw = await callAI(system, user);
        raw = raw.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
        const post = JSON.parse(raw);
        log('info', `✓ Generated: "${post.title}"`);

        const c = getConfig();
        if (c.get('approvalMode')) {
            panel?.webview.postMessage({ cmd: 'review_post', data: post });
        } else {
            await doApprovePost({ postData: post });
        }
    } catch(e) {
        log('error', `Generate failed: ${e.message}`);
        panel?.webview.postMessage({ cmd: 'generate_error', data: { error: e.message } });
    }
}

// ── Chat ──────────────────────────────────────────────────────────────────────────────────
async function doChat({ message, history = [] }) {
    const system = `You are a WordPress and content strategy assistant.
You help plan posts, improve SEO, suggest topics, and assist with English teaching content.
Be concise and practical.`;

    const messages = history.map(m => ({ role: m.role, content: m.content }));
    messages.push({ role: 'user', content: message });

    try {
        const c = getConfig();
        const fetch = (await import('node-fetch')).default;
        let reply = '';

        if (c.get('aiProvider') === 'claude') {
            const res = await fetch('https://api.anthropic.com/v1/messages', {
                method: 'POST',
                headers: {
                    'x-api-key': c.get('claudeKey'),
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'claude-sonnet-4-20250514',
                    max_tokens: 1000,
                    system,
                    messages,
                }),
            });
            const d = await res.json();
            reply = d.content[0].text;
        } else if (c.get('aiProvider') === 'deepseek') {
            const res = await fetch('https://api.deepseek.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${c.get('deepseekKey')}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'deepseek-chat',
                    messages: [{ role: 'system', content: system }, ...messages],
                }),
            });
            const d = await res.json();
            reply = d.choices[0].message.content;
        } else {
            reply = await callAI(system, message);
        }

        panel?.webview.postMessage({ cmd: 'chat_reply', data: { reply } });
    } catch(e) {
        panel?.webview.postMessage({ cmd: 'chat_reply', data: { reply: `Error: ${e.message}` } });
    }
}

function deactivate() {}
module.exports = { activate, deactivate };
