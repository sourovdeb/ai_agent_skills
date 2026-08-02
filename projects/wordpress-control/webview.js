// src/webview.js — returns the full HTML for the VS Code panel
// Called from extension.js as: panel.webview.html = getWebviewHTML()

function getWebviewHTML() {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>WP AI Studio</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg:       #1e1e1e;
    --surface:  #252526;
    --surface2: #2d2d2d;
    --border:   #3e3e42;
    --accent:   #0e639c;
    --accent2:  #673de6;
    --green:    #4ec9b0;
    --yellow:   #dcdcaa;
    --red:      #f44747;
    --text:     #d4d4d4;
    --muted:    #858585;
    --radius:   6px;
  }
  body { background: var(--bg); color: var(--text); font-family: 'Segoe UI', sans-serif; font-size: 13px; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }

  .topbar { background: var(--surface); border-bottom: 1px solid var(--border); padding: 8px 12px; display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
  .topbar .logo { font-weight: 700; color: var(--accent2); font-size: 14px; flex: 1; }
  .provider-badge { background: var(--surface2); border: 1px solid var(--border); border-radius: 20px; padding: 2px 10px; font-size: 11px; color: var(--green); cursor: pointer; }
  .site-badge { background: var(--surface2); border: 1px solid var(--border); border-radius: 20px; padding: 2px 10px; font-size: 11px; color: var(--muted); }

  .tabs { display: flex; background: var(--surface); border-bottom: 1px solid var(--border); flex-shrink: 0; }
  .tab { padding: 8px 16px; cursor: pointer; border-bottom: 2px solid transparent; color: var(--muted); font-size: 12px; transition: all 0.15s; }
  .tab:hover { color: var(--text); }
  .tab.active { color: var(--text); border-bottom-color: var(--accent2); }

  .view { display: none; flex: 1; overflow: hidden; flex-direction: column; }
  .view.active { display: flex; }

  .chat-messages { flex: 1; overflow-y: auto; padding: 12px; display: flex; flex-direction: column; gap: 10px; }
  .msg { display: flex; gap: 8px; }
  .msg.user { flex-direction: row-reverse; }
  .msg-bubble { max-width: 80%; padding: 8px 12px; border-radius: var(--radius); line-height: 1.5; white-space: pre-wrap; }
  .msg.user .msg-bubble { background: var(--accent); color: #fff; }
  .msg.ai .msg-bubble { background: var(--surface2); border: 1px solid var(--border); }
  .msg-avatar { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0; }
  .msg.user .msg-avatar { background: var(--accent); }
  .msg.ai  .msg-avatar { background: var(--accent2); }
  .chat-input-row { display: flex; gap: 6px; padding: 10px 12px; border-top: 1px solid var(--border); background: var(--surface); flex-shrink: 0; }
  .chat-input-row textarea { flex: 1; background: var(--surface2); border: 1px solid var(--border); color: var(--text); border-radius: var(--radius); padding: 8px; font-size: 13px; resize: none; height: 60px; font-family: inherit; }
  .chat-input-row textarea:focus { outline: none; border-color: var(--accent); }

  .generate-panel { padding: 16px; display: flex; flex-direction: column; gap: 12px; overflow-y: auto; }
  .field-row { display: flex; flex-direction: column; gap: 4px; }
  .field-row label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; }
  input, textarea, select { background: var(--surface2); border: 1px solid var(--border); color: var(--text); border-radius: var(--radius); padding: 7px 10px; font-size: 13px; width: 100%; font-family: inherit; }
  input:focus, textarea:focus, select:focus { outline: none; border-color: var(--accent); }
  .btn-row { display: flex; gap: 8px; flex-wrap: wrap; }
  .btn { padding: 7px 14px; border-radius: var(--radius); border: none; cursor: pointer; font-size: 12px; font-weight: 600; transition: opacity 0.15s; }
  .btn:hover { opacity: 0.85; }
  .btn:disabled { opacity: 0.4; cursor: default; }
  .btn-primary  { background: var(--accent);  color: #fff; }
  .btn-purple   { background: var(--accent2); color: #fff; }
  .btn-green    { background: #2d7a4a;        color: #fff; }
  .btn-danger   { background: #6e2020;        color: var(--red); }
  .btn-ghost    { background: transparent; color: var(--text); border: 1px solid var(--border); }

  .review-card { background: var(--surface2); border: 1px solid var(--border); border-radius: var(--radius); padding: 14px; display: flex; flex-direction: column; gap: 10px; }
  .review-card h3 { color: var(--yellow); font-size: 14px; }
  .review-card .meta { font-size: 11px; color: var(--muted); }
  .content-preview { max-height: 200px; overflow-y: auto; background: var(--bg); border-radius: 4px; padding: 10px; font-size: 12px; line-height: 1.6; }
  .content-preview h2 { color: var(--yellow); font-size: 13px; margin: 8px 0 4px; }

  .posts-panel { padding: 12px; display: flex; flex-direction: column; gap: 8px; overflow-y: auto; }
  .post-item { background: var(--surface2); border: 1px solid var(--border); border-radius: var(--radius); padding: 10px 14px; display: flex; align-items: center; gap: 10px; }
  .post-item .title { flex: 1; font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .post-item .badge { font-size: 10px; padding: 2px 8px; border-radius: 20px; }
  .badge-draft    { background: #3a3a00; color: var(--yellow); }
  .badge-future   { background: #003a1a; color: var(--green); }
  .badge-publish  { background: #003a2a; color: #7ee8a2; }

  .logs-panel { padding: 10px 12px; overflow-y: auto; flex: 1; font-family: 'Cascadia Code', 'Courier New', monospace; font-size: 12px; line-height: 1.8; }
  .log-line { display: flex; gap: 8px; }
  .log-time { color: var(--muted); flex-shrink: 0; }
  .log-msg  { color: var(--text); }
  .log-line.error .log-msg { color: var(--red); }
  .log-line.warn  .log-msg { color: var(--yellow); }
  .log-line.ok    .log-msg { color: var(--green); }

  .settings-panel { padding: 16px; overflow-y: auto; display: flex; flex-direction: column; gap: 16px; }
  .settings-group { background: var(--surface2); border: 1px solid var(--border); border-radius: var(--radius); padding: 14px; display: flex; flex-direction: column; gap: 10px; }
  .settings-group h4 { color: var(--yellow); font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }

  .status-card { background: var(--surface2); border: 1px solid var(--border); border-radius: var(--radius); padding: 12px; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .stat { display: flex; flex-direction: column; gap: 2px; }
  .stat-label { font-size: 10px; color: var(--muted); text-transform: uppercase; }
  .stat-value { font-size: 16px; font-weight: 700; color: var(--green); }

  .spinner { display: inline-block; width: 14px; height: 14px; border: 2px solid var(--border); border-top-color: var(--accent2); border-radius: 50%; animation: spin 0.7s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
  .hidden { display: none !important; }
  .divider { height: 1px; background: var(--border); }
  .tag-list { display: flex; flex-wrap: wrap; gap: 4px; }
  .tag { background: var(--bg); border: 1px solid var(--border); border-radius: 20px; padding: 2px 8px; font-size: 11px; color: var(--muted); }
</style>
</head>
<body>

<div class="topbar">
  <span class="logo">⚡ WP AI Studio</span>
  <span class="provider-badge" id="providerBadge" onclick="switchTab('settings')">claude</span>
  <span class="site-badge" id="siteBadge">not connected</span>
  <button class="btn btn-ghost" style="padding:3px 8px;font-size:11px;" onclick="doStatus()">ping</button>
</div>

<div class="tabs">
  <div class="tab active" onclick="switchTab('chat')">&#x1F4AC; Chat</div>
  <div class="tab" onclick="switchTab('generate')">&#x270D;&#xFE0F; Generate</div>
  <div class="tab" onclick="switchTab('posts')">&#x1F4CB; Posts</div>
  <div class="tab" onclick="switchTab('logs')">&#x1F4DC; Logs</div>
  <div class="tab" onclick="switchTab('settings')">&#x2699;&#xFE0F; Settings</div>
</div>

<!-- CHAT -->
<div class="view active" id="view-chat" style="display:flex;flex-direction:column;">
  <div class="chat-messages" id="chatMessages">
    <div class="msg ai">
      <div class="msg-avatar">&#x1F916;</div>
      <div class="msg-bubble">Hi! I'm your WordPress AI assistant. Ask me to plan posts, improve SEO, suggest topics, or generate content.</div>
    </div>
  </div>
  <div class="chat-input-row">
    <textarea id="chatInput" placeholder="Ask anything about your WordPress content strategy..." onkeydown="chatKey(event)"></textarea>
    <button class="btn btn-purple" onclick="sendChat()" id="chatBtn">Send</button>
  </div>
</div>

<!-- GENERATE -->
<div class="view" id="view-generate">
  <div class="generate-panel">
    <div class="field-row"><label>Topic / Title</label><input id="genTopic" placeholder="e.g. 5 English idioms every learner should know" /></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
      <div class="field-row"><label>Tone</label>
        <select id="genTone"><option value="professional">Professional</option><option value="friendly">Friendly</option><option value="educational">Educational</option><option value="conversational">Conversational</option></select>
      </div>
      <div class="field-row"><label>Word count</label>
        <select id="genWords"><option value="400">~400 words</option><option value="600" selected>~600 words</option><option value="900">~900 words</option><option value="1200">~1200 words</option></select>
      </div>
    </div>
    <div class="btn-row">
      <button class="btn btn-purple" onclick="doGenerate()" id="genBtn">&#x2728; Generate with AI</button>
      <span id="genSpinner" class="spinner hidden"></span>
    </div>
    <div class="divider"></div>
    <div id="reviewArea" class="hidden">
      <div class="review-card">
        <h3 id="reviewTitle"></h3>
        <div class="meta"><span id="reviewSeoTitle" style="color:var(--green)"></span><br/><span id="reviewMeta" style="color:var(--muted)"></span></div>
        <div class="tag-list" id="reviewTags"></div>
        <div class="content-preview" id="reviewContent"></div>
        <div class="btn-row">
          <button class="btn btn-green" onclick="approvePub()">&#x2713; Publish Now</button>
          <button class="btn btn-primary" onclick="approveDraft()">Save as Draft</button>
          <button class="btn btn-ghost" onclick="openScheduler()">&#x1F550; Schedule</button>
          <button class="btn btn-ghost" onclick="editTitle()">&#x270F;&#xFE0F; Edit Title</button>
          <button class="btn btn-danger" onclick="discardDraft()">&#x2715; Discard</button>
        </div>
        <div id="schedulerRow" class="hidden" style="display:flex;gap:8px;align-items:center;">
          <input type="datetime-local" id="scheduleInput" style="flex:1;" />
          <button class="btn btn-green" onclick="schedulePost()">Schedule</button>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- POSTS -->
<div class="view" id="view-posts">
  <div style="display:flex;gap:8px;padding:10px 12px;border-bottom:1px solid var(--border);background:var(--surface);flex-shrink:0;">
    <select id="postFilter" onchange="loadPosts()" style="flex:1;">
      <option value="">All (draft + scheduled)</option>
      <option value="future">Scheduled only</option>
      <option value="draft">Drafts only</option>
    </select>
    <button class="btn btn-ghost" onclick="loadPosts()" style="padding:5px 10px;">&#x21BB; Refresh</button>
  </div>
  <div class="posts-panel" id="postsList"><div style="color:var(--muted);text-align:center;padding:20px;">Click Refresh to load posts</div></div>
</div>

<!-- LOGS -->
<div class="view" id="view-logs">
  <div style="display:flex;gap:8px;padding:8px 12px;border-bottom:1px solid var(--border);background:var(--surface);flex-shrink:0;">
    <span style="color:var(--muted);font-size:11px;flex:1;">Live action log</span>
    <button class="btn btn-ghost" onclick="clearLogs()" style="padding:3px 8px;font-size:11px;">Clear</button>
  </div>
  <div class="logs-panel" id="logsPanel"></div>
</div>

<!-- SETTINGS -->
<div class="view" id="view-settings">
  <div class="settings-panel">
    <div id="statusCard" class="hidden">
      <div class="status-card">
        <div class="stat"><div class="stat-label">Site</div><div class="stat-value" id="statSite" style="font-size:12px;">&#x2014;</div></div>
        <div class="stat"><div class="stat-label">WP Version</div><div class="stat-value" id="statWP" style="font-size:12px;">&#x2014;</div></div>
        <div class="stat"><div class="stat-label">Published</div><div class="stat-value" id="statPosts">&#x2014;</div></div>
        <div class="stat"><div class="stat-label">Scheduled</div><div class="stat-value" id="statSched">&#x2014;</div></div>
      </div>
    </div>
    <div class="settings-group">
      <h4>WordPress</h4>
      <div class="field-row"><label>Site URL</label><input id="s_wpUrl" placeholder="https://your-site.com" /></div>
      <div class="field-row"><label>Username</label><input id="s_wpUser" placeholder="your-wp-username" /></div>
      <div class="field-row"><label>App Password</label><input id="s_wpPass" type="password" placeholder="xxxx xxxx xxxx xxxx xxxx xxxx" /></div>
      <div class="field-row"><label>Plugin Secret Key</label><input id="s_pluginKey" type="password" placeholder="your-plugin-key" /></div>
      <button class="btn btn-primary" onclick="testConnection()" style="align-self:flex-start;">Test Connection</button>
    </div>
    <div class="settings-group">
      <h4>AI Provider</h4>
      <div class="field-row"><label>Provider</label>
        <select id="s_provider" onchange="updateProviderUI()">
          <option value="claude">Claude (Anthropic)</option>
          <option value="deepseek">DeepSeek</option>
          <option value="ollama">Ollama (local)</option>
        </select>
      </div>
      <div id="s_claudeRow"   class="field-row"><label>Claude API Key</label><input id="s_claudeKey" type="password" placeholder="sk-ant-..." /></div>
      <div id="s_deepseekRow" class="field-row hidden"><label>DeepSeek API Key</label><input id="s_deepseekKey" type="password" placeholder="sk-..." /></div>
      <div id="s_ollamaRow"   class="field-row hidden"><label>Ollama URL</label><input id="s_ollamaUrl" placeholder="http://localhost:11434" /></div>
      <div id="s_modelRow"    class="field-row hidden"><label>Model</label><input id="s_ollamaModel" placeholder="llama3" /></div>
    </div>
    <div class="settings-group">
      <h4>Behaviour</h4>
      <div class="field-row"><label>Default post status</label>
        <select id="s_status"><option value="draft">Draft (safe)</option><option value="publish">Publish immediately</option></select>
      </div>
      <label style="display:flex;align-items:center;gap:8px;cursor:pointer;">
        <input type="checkbox" id="s_approval" checked />
        <span>Approval mode &#x2014; review AI output before posting</span>
      </label>
    </div>
    <button class="btn btn-purple" onclick="saveSettings()">&#x1F4BE; Save All Settings</button>
  </div>
</div>

<script>
const vscode = acquireVsCodeApi();
let currentPost = null;
let chatHistory = [];

function switchTab(id) {
  document.querySelectorAll('.tab').forEach((t, i) => {
    const ids = ['chat','generate','posts','logs','settings'];
    t.classList.toggle('active', ids[i] === id);
  });
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.getElementById('view-' + id).classList.add('active');
  if (id === 'posts') loadPosts();
}

window.addEventListener('message', e => {
  const { cmd, data } = e.data;
  if (cmd === 'settings')      applySettings(data);
  if (cmd === 'log')           appendLog(data);
  if (cmd === 'status_result') applyStatus(data);
  if (cmd === 'posts_list')    renderPosts(data);
  if (cmd === 'review_post')   showReview(data);
  if (cmd === 'generating')    { setGenBusy(true); appendLog({level:'info', message:'Generating: ' + data.topic, time: now()}); }
  if (cmd === 'generate_error'){ setGenBusy(false); appendLog({level:'error', message: data.error, time: now()}); }
  if (cmd === 'post_created')  { appendLog({level:'ok', message:'✓ Post created ID:' + data.id, time: now()}); }
  if (cmd === 'chat_reply')    { appendChatMsg('ai', data.reply); setChatBusy(false); }
  if (cmd === 'run_status')    doStatus();
});

function applySettings(d) {
  if (!d) return;
  document.getElementById('s_wpUrl').value       = d.wordpressUrl  || '';
  document.getElementById('s_wpUser').value      = d.wpUser        || '';
  document.getElementById('s_wpPass').value      = d.wpAppPassword || '';
  document.getElementById('s_pluginKey').value   = d.pluginKey     || '';
  document.getElementById('s_provider').value    = d.aiProvider    || 'claude';
  document.getElementById('s_claudeKey').value   = d.claudeKey     || '';
  document.getElementById('s_deepseekKey').value = d.deepseekKey   || '';
  document.getElementById('s_ollamaUrl').value   = d.ollamaUrl     || '';
  document.getElementById('s_ollamaModel').value = d.ollamaModel   || '';
  document.getElementById('s_status').value      = d.defaultStatus || 'draft';
  document.getElementById('s_approval').checked  = d.approvalMode !== false;
  document.getElementById('providerBadge').textContent = d.aiProvider || 'claude';
  if (d.wordpressUrl) document.getElementById('siteBadge').textContent = new URL(d.wordpressUrl).hostname;
  updateProviderUI();
}

function updateProviderUI() {
  const p = document.getElementById('s_provider').value;
  document.getElementById('s_claudeRow').classList.toggle('hidden',   p !== 'claude');
  document.getElementById('s_deepseekRow').classList.toggle('hidden', p !== 'deepseek');
  document.getElementById('s_ollamaRow').classList.toggle('hidden',   p !== 'ollama');
  document.getElementById('s_modelRow').classList.toggle('hidden',    p !== 'ollama');
}

function saveSettings() {
  vscode.postMessage({ cmd: 'save_settings', data: {
    wordpressUrl:  document.getElementById('s_wpUrl').value.trim(),
    wpUser:        document.getElementById('s_wpUser').value.trim(),
    wpAppPassword: document.getElementById('s_wpPass').value.trim(),
    pluginKey:     document.getElementById('s_pluginKey').value.trim(),
    aiProvider:    document.getElementById('s_provider').value,
    claudeKey:     document.getElementById('s_claudeKey').value.trim(),
    deepseekKey:   document.getElementById('s_deepseekKey').value.trim(),
    ollamaUrl:     document.getElementById('s_ollamaUrl').value.trim(),
    ollamaModel:   document.getElementById('s_ollamaModel').value.trim(),
    defaultStatus: document.getElementById('s_status').value,
    approvalMode:  document.getElementById('s_approval').checked,
  }});
}

function testConnection() { doStatus(); switchTab('settings'); }
function doStatus() { vscode.postMessage({ cmd: 'site_status' }); }

function applyStatus(d) {
  if (d.error) { appendLog({level:'error', message: 'Connection failed: ' + d.error, time: now()}); return; }
  document.getElementById('statusCard').classList.remove('hidden');
  document.getElementById('statSite').textContent  = d.site    || '&#x2014;';
  document.getElementById('statWP').textContent    = d.wp_version || '&#x2014;';
  document.getElementById('statPosts').textContent = d.total_posts ?? '&#x2014;';
  document.getElementById('statSched').textContent = d.scheduled_posts ?? '&#x2014;';
  appendLog({level:'ok', message:'Connected: ' + d.site + ' | WP ' + d.wp_version, time: now()});
  document.getElementById('siteBadge').textContent = d.site || 'connected';
  document.getElementById('siteBadge').style.color = 'var(--green)';
}

function doGenerate() {
  const topic = document.getElementById('genTopic').value.trim();
  if (!topic) { document.getElementById('genTopic').focus(); return; }
  setGenBusy(true);
  document.getElementById('reviewArea').classList.add('hidden');
  vscode.postMessage({ cmd: 'generate', data: {
    topic,
    tone:      document.getElementById('genTone').value,
    wordCount: document.getElementById('genWords').value,
  }});
}

function setGenBusy(b) {
  document.getElementById('genBtn').disabled = b;
  document.getElementById('genSpinner').classList.toggle('hidden', !b);
}

function showReview(post) {
  setGenBusy(false);
  currentPost = post;
  document.getElementById('reviewTitle').textContent    = post.title;
  document.getElementById('reviewSeoTitle').textContent = 'SEO: ' + (post.seo_title || post.title);
  document.getElementById('reviewMeta').textContent     = post.meta_desc || '';
  document.getElementById('reviewContent').innerHTML    = post.content || '';
  const tagDiv = document.getElementById('reviewTags');
  tagDiv.innerHTML = (post.tags || []).map(t => '<span class="tag">' + t + '</span>').join('');
  document.getElementById('reviewArea').classList.remove('hidden');
  document.getElementById('schedulerRow').classList.add('hidden');
  switchTab('generate');
}

function approvePub()   { vscode.postMessage({ cmd: 'approve_post',  data: { postData: currentPost } }); }
function approveDraft() { vscode.postMessage({ cmd: 'approve_post',  data: { postData: {...currentPost, status:'draft'} } }); }
function openScheduler(){ document.getElementById('schedulerRow').classList.toggle('hidden'); }
function schedulePost() {
  const dt = document.getElementById('scheduleInput').value;
  if (!dt) return;
  vscode.postMessage({ cmd: 'schedule_post', data: { postData: currentPost, schedule: dt.replace('T',' ') + ':00' } });
}
function editTitle() {
  const t = prompt('Edit title:', currentPost.title);
  if (t) { currentPost.title = t; document.getElementById('reviewTitle').textContent = t; }
}
function discardDraft() { document.getElementById('reviewArea').classList.add('hidden'); currentPost = null; }

function loadPosts() {
  const filter = document.getElementById('postFilter').value;
  document.getElementById('postsList').innerHTML = '<div style="color:var(--muted);padding:20px;text-align:center;"><span class="spinner"></span> Loading...</div>';
  vscode.postMessage({ cmd: 'list_posts', data: filter ? { post_status: filter } : {} });
}

function renderPosts(posts) {
  const el = document.getElementById('postsList');
  if (!posts.length) { el.innerHTML = '<div style="color:var(--muted);padding:20px;text-align:center;">No posts found</div>'; return; }
  el.innerHTML = posts.map(p =>
    '<div class="post-item"><span class="badge badge-' + p.status + '">' + p.status + '</span>' +
    '<span class="title" title="' + escHtml(p.title) + '">' + escHtml(p.title) + '</span>' +
    '<span style="color:var(--muted);font-size:11px;flex-shrink:0;">' + (p.scheduled||'').slice(0,10) + '</span>' +
    '<button class="btn btn-ghost" style="padding:3px 8px;font-size:11px;" onclick="deletePost(' + p.id + ')">&#x2715;</button>' +
    '<a href="' + p.link + '" style="color:var(--accent);font-size:11px;" title="View">&#x2197;</a></div>'
  ).join('');
}

function deletePost(id) {
  if (confirm('Delete post ID:' + id + '?')) vscode.postMessage({ cmd: 'delete_post', data: { id } });
}

function sendChat() {
  const input = document.getElementById('chatInput');
  const msg = input.value.trim();
  if (!msg) return;
  input.value = '';
  appendChatMsg('user', msg);
  chatHistory.push({ role: 'user', content: msg });
  setChatBusy(true);
  vscode.postMessage({ cmd: 'chat', data: { message: msg, history: chatHistory.slice(-10) } });
}

function chatKey(e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendChat(); } }

function appendChatMsg(role, text) {
  const div = document.createElement('div');
  div.className = 'msg ' + role;
  div.innerHTML = '<div class="msg-avatar">' + (role === 'user' ? '&#x1F464;' : '&#x1F916;') + '</div><div class="msg-bubble">' + escHtml(text) + '</div>';
  const box = document.getElementById('chatMessages');
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
  if (role === 'ai') chatHistory.push({ role: 'assistant', content: text });
}

function setChatBusy(b) { document.getElementById('chatBtn').disabled = b; }

function appendLog(entry) {
  const el = document.getElementById('logsPanel');
  const div = document.createElement('div');
  div.className = 'log-line ' + (entry.level || 'info');
  div.innerHTML = '<span class="log-time">' + entry.time + '</span><span class="log-msg">' + escHtml(entry.message) + '</span>';
  el.appendChild(div);
  el.scrollTop = el.scrollHeight;
}
function clearLogs() { document.getElementById('logsPanel').innerHTML = ''; }

function now() { return new Date().toLocaleTimeString(); }
function escHtml(t) { return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

vscode.postMessage({ cmd: 'load_settings' });
</script>
</body>
</html>`;
}

module.exports = { getWebviewHTML };
