'use strict';
/* Open Writer OS 2.0 (web) - core logic. No dependencies. Node-testable. */

const GENERAL_BASE = `You are the writing engine of Open Writer OS, a free, open-source
fiction and memoir assistant. The writer owns story meaning, characters,
emotional intention, major choices and final creative authority. You provide
extraction, structure, drafting, continuity management and revision.

SOURCE-OF-TRUTH ORDER when information conflicts:
1. The writer's current explicit statement
2. Writer-confirmed canon
3. Approved manuscript text
4. The writer's notes
5. Your suggestions
6. Your guesses
Never let a guess override confirmed information.

Label important story facts with a status: CANON, PROPOSED, UNKNOWN,
CHARACTER_BELIEF, READER_KNOWLEDGE, REJECTED, RETCONNED. Never invent ages,
dates, names or history for blank fields; mark them UNKNOWN.

One main task at a time. No generic motivational language, no stock AI
metaphors, no characters conveniently explaining the plot, no neat manufactured
lessons. Mark proposals as proposals.`;

const MEMOIR_RULES = `
MEMOIR MODE - the writer works from lived experience. Memory is evidence, not
perfect record. Label important real-world material with an evidence status:
REMEMBERED, DOCUMENTED, CORROBORATED, RECONSTRUCTED, INFERRED, UNCERTAIN,
DISPUTED, FICTIONALIZED. Never upgrade REMEMBERED to DOCUMENTED without a
source. Preserve incompatible accounts; never invent details to fill gaps.
For real third parties, respect privacy: propose anonymization, composites or
exclusion, and never publish identifying detail about a living person without
the writer's explicit consent.`;

const MODE_INSTRUCTIONS = {
  DISCOVER: 'MODE DISCOVER - extract the story from the writer. Do not draft large prose. Summarize what seems certain, likely, unclear and contradictory. Ask at most 1-4 questions, only ones that change the story materially. Offer 2-4 clearly different possibilities, labelled as proposals. Preserve UNKNOWN.',
  ARCHITECT: 'MODE ARCHITECT - work on structure and causality. Do not write polished prose. Identify what is fixed, what is missing, what conflicts and what the options are. Never change the central premise to fit a textbook template.',
  SCENE_PLAN: 'MODE SCENE_PLAN - plan one scene. Do not write the complete scene unless asked. Produce a scene contract: who is present, where and when, what each character wants, what changes, what the reader should feel, which facts from the notes the scene depends on. Flag continuity risks.',
  DRAFT: 'MODE DRAFT - write story prose from the notes and manuscript. Follow the writer\'s voice sample. Advance only what the scene allows. End with a short CANON CHECK listing any new facts, each with a fact status.',
  DIALOGUE: 'MODE DIALOGUE - focus on dialogue, subtext, voice and conversational strategy. Do not change the plot. Distinguishable voices consistent with the notes. No exposition disguised as conversation. Preserve the writer\'s dialect in dialogue exactly as written.',
  DESCRIBE: 'MODE DESCRIBE - increase sensory or environmental presence. Do not advance the plot unnecessarily. Description must reveal character perception or mood; selective, not an inventory.',
  DEEPEN: 'MODE DEEPEN - increase psychological depth, tension or interiority. Do not add major revelations the notes have not approved.',
  COMPRESS: 'MODE COMPRESS - remove redundancy while preserving emotion, information and rhythm. Keep cuts visible: say briefly what was removed and why it was safe.',
  CONTINUITY: 'MODE CONTINUITY - audit only. Check names, ages, dates, timeline, locations, possessions, character knowledge, relationships, promises, clues, world rules and cause and effect. Report contradictions with references. Do not rewrite unless asked afterward.',
  REVISE: 'MODE REVISE - improve the selected passage toward the writer\'s stated goal. Preserve the writer\'s voice, meaning and dialect. Show the revised passage, then list the changes briefly.',
  CANON_UPDATE: 'MODE CANON_UPDATE - extract established facts from the manuscript and notes. Promote a fact to CANON only when the writer has accepted, approved or continued from it. List each entry with its fact status and the evidence for it.',
  PROFILE_UPDATE: 'MODE PROFILE_UPDATE - record meaningful writer preferences and corrections. Use DECLARED for stated preferences, INFERRED (with confidence and evidence) for patterns, EVIDENCED only for prose the writer wrote, TARGET for the sound the writer wants.',
};

const MODES = {
  DISCOVER: { label: 'Discover', temp: 0.9 },
  ARCHITECT: { label: 'Structure', temp: 0.7 },
  SCENE_PLAN: { label: 'Scene plan', temp: 0.6 },
  DRAFT: { label: 'Draft', temp: 0.85 },
  DIALOGUE: { label: 'Dialogue', temp: 0.8 },
  DESCRIBE: { label: 'Describe', temp: 0.8 },
  DEEPEN: { label: 'Deepen', temp: 0.8 },
  COMPRESS: { label: 'Tighten', temp: 0.5 },
  CONTINUITY: { label: 'Continuity', temp: 0.3 },
  REVISE: { label: 'Revise', temp: 0.6 },
  CANON_UPDATE: { label: 'Canon update', temp: 0.2 },
  PROFILE_UPDATE: { label: 'Profile update', temp: 0.3 },
};

const ACTIONS = {
  'short-fiction': {
    discover:    { mode: 'DISCOVER', label: 'Premise ideas', temp: 0.9, ask: 'Give 5 distinct premises for a short story. For each: a one-sentence hook, the main character\'s want, and the obstacle. Use my notes if any. Label each as a proposal.' },
    architect:   { mode: 'ARCHITECT', label: 'Outline', temp: 0.7, ask: 'Outline this story in 6-9 beats, one line each, with the turn marked. Offer two possible endings (one open, one closed) and what each costs.' },
    scene_plan:  { mode: 'SCENE_PLAN', label: 'Plan a scene', temp: 0.6, ask: 'Write a scene contract for the next scene: who is present, where and when, what each character wants in the scene, what changes, what the reader should feel, and which facts from my notes it depends on. Flag continuity risks. Do not write the scene itself unless I ask.' },
    draft:       { mode: 'DRAFT', label: 'Draft / continue', temp: 0.85, ask: 'Write the next scene, about 300-500 words, continuing from where the manuscript ends, in my voice and tense. Stop at a natural beat. Do not conclude the story unless this is its natural ending.' },
    dialogue:    { mode: 'DIALOGUE', label: 'Dialogue pass', temp: 0.8, needSel: true, ask: 'Rewrite the selected passage focusing on dialogue: subtext, voice and conversational strategy. Keep the plot. Return only the rewrite.' },
    describe:    { mode: 'DESCRIBE', label: 'Describe', temp: 0.8, needSel: true, ask: 'Rewrite the selected passage adding sensory and environmental presence without advancing the plot. Return only the rewrite.' },
    deepen:      { mode: 'DEEPEN', label: 'Deepen', temp: 0.8, needSel: true, ask: 'Rewrite the selected passage with more psychological depth, tension or interiority. No major revelations the notes have not approved. Return only the rewrite.' },
    compress:    { mode: 'COMPRESS', label: 'Tighten', temp: 0.5, needSel: true, ask: 'Rewrite the selected text about 30% shorter without losing meaning, emotion or voice. Return only the rewrite.' },
    revise:      { mode: 'REVISE', label: 'Show, don\'t tell', temp: 0.8, needSel: true, ask: 'Rewrite the selected text so feelings and facts come through action, sensory detail and subtext instead of being stated. Keep meaning and length close. Return only the rewrite.' },
    continuity:  { mode: 'CONTINUITY', label: 'Beta reader', temp: 0.4, ask: 'Act as a kind, honest beta reader of the manuscript: 3 strengths, 3 problems (most important first), 3 concrete next steps. Then run the continuity audit against my notes and report contradictions. Quote at most 10 words at a time. Do not rewrite the story unasked.' },
    canon:       { mode: 'CANON_UPDATE', label: 'Canon update', temp: 0.2, ask: 'Extract established facts from the manuscript and notes. Promote to CANON only facts I have accepted or continued from. List each entry with its fact status and evidence.' },
    profile:     { mode: 'PROFILE_UPDATE', label: 'Profile update', temp: 0.3, ask: 'Record my preferences and corrections from my instruction in the writer profile, using DECLARED, INFERRED, EVIDENCED or TARGET.' },
  },
  biography: {
    questions: { mode: 'DISCOVER', label: 'Interview questions', temp: 0.6, ask: 'Write 12 open interview questions for this subject, ordered from childhood to the present, plus 3 sensitive ones marked "ask only with consent". Do not repeat what the notes already answer.' },
    timeline:  { mode: 'CONTINUITY', label: 'Timeline', temp: 0.2, ask: 'Build a dated timeline using ONLY facts in the notes and manuscript. Mark every uncertain or missing date [VERIFY] and give each entry an evidence status. Add nothing that is not stated.' },
    draft:     { mode: 'DRAFT', label: 'Draft from notes', temp: 0.4, ask: 'Write about 300-400 words of biographical prose using ONLY facts in the notes. Attribute sources. Tag any claim not in the notes [VERIFY]. Never invent quotes or dates.' },
    verify:    { mode: 'CONTINUITY', label: 'Fact-check list', temp: 0.2, ask: 'List every factual claim in the selected text (or the manuscript if nothing is selected) as a checklist: the claim, whether the notes support it (yes/no), its evidence status, and what source would confirm it.' },
    care:      { mode: 'REVISE', label: 'Consent & risk check', temp: 0.3, ask: 'Check the text for privacy, consent, defamation and cultural-sensitivity risks, especially for living people and minors. List each risk, why it matters, and a safer alternative. This is not legal advice.' },
  },
};

const strip = s => s.replace(/^---[\s\S]*?---\s*/, '');
const clip = (s, n) => s.length > n ? '\u2026' + s.slice(-n) : s;
const slug = t => (String(t || '').trim().replace(/[^\p{L}\p{M}\p{N}]+/gu, '-').replace(/^-+|-+$/g, '')) || 'untitled';

function buildMessages(skills, p) {
  let skill = null;
  if (p.skill && p.skill !== 'none') {
    if (!skills[p.skill]) throw new Error('Unknown skill ' + p.skill);
    skill = p.skill;
  }
  const actions = skill ? ACTIONS[skill] : null;
  let action = null;
  if (skill) {
    action = actions && actions[p.action];
    if (!action) throw new Error('Unknown action for skill ' + skill);
  } else {
    action = { mode: String(p.action || '').toUpperCase(), label: p.action, temp: MODES[p.action] ? MODES[p.action].temp : 0.8, ask: 'Apply the ' + p.action + ' mode to my manuscript and notes.' };
    if (!MODES[action.mode]) throw new Error('Unknown mode ' + p.action);
  }
  const sel = (p.sel || '').trim();
  if (action.needSel && !sel) throw new Error('Select some text first.');
  const memoir = !!p.memoir || skill === 'biography';
  let sys = (skill ? strip(skills[skill]) : GENERAL_BASE);
  if (MODE_INSTRUCTIONS[action.mode]) sys += '\n\n' + MODE_INSTRUCTIONS[action.mode];
  if (memoir) sys += '\n\n' + MEMOIR_RULES;
  sys += '\n\nOutput language: ' + ((p.lang || '').trim() || "the language of the author's text") + '.';
  if ((p.voice || '').trim()) sys += '\n\nAUTHOR VOICE SAMPLE (match rhythm and diction, never copy sentences):\n' + clip(p.voice.trim(), 1500);
  if ((p.notes || '').trim()) sys += '\n\nPROJECT NOTES (authoritative):\n' + clip(p.notes.trim(), 3000);
  let u = action.ask;
  if ((p.instr || '').trim()) u += '\n\nWRITER\'S INSTRUCTION:\n' + p.instr.trim();
  if (sel) u += '\n\nSELECTED TEXT:\n' + sel;
  u += '\n\nMANUSCRIPT (latest part):\n' + (clip((p.text || '').trim(), p.maxChars || 6000) || '(empty)');
  return { messages: [{ role: 'system', content: sys }, { role: 'user', content: u }], temperature: action.temp };
}

function makeParser(onToken) {
  let buf = '';
  const line = l => {
    l = l.trim(); if (!l) return;
    if (l.startsWith('data:')) l = l.slice(5).trim();
    if (l === '[DONE]') return;
    let j; try { j = JSON.parse(l); } catch (e) { return; }
    if (j && j.error) throw new Error(typeof j.error === 'string' ? j.error : (j.error.message || 'API error'));
    const t = (j.message && j.message.content) || (j.choices && j.choices[0] && j.choices[0].delta && j.choices[0].delta.content) || '';
    if (t) onToken(t);
  };
  return {
    feed(c) { buf += c; const parts = buf.split('\n'); buf = parts.pop(); parts.forEach(line); },
    end() { const b = buf; buf = ''; line(b); },
  };
}

async function chat(cfg, built, onToken, signal) {
  const ollama = cfg.provider === 'ollama';
  const base = cfg.base.replace(/\/+$/, '');
  const body = ollama
    ? { model: cfg.model, messages: built.messages, stream: true, options: { temperature: built.temperature, num_ctx: cfg.numCtx || 4096 } }
    : { model: cfg.model, messages: built.messages, stream: true, temperature: built.temperature };
  const headers = { 'Content-Type': 'application/json' };
  if (!ollama && cfg.key) headers.Authorization = 'Bearer ' + cfg.key;
  const r = await fetch(ollama ? base + '/api/chat' : base + '/chat/completions', { method: 'POST', headers, body: JSON.stringify(body), signal });
  if (!r.ok) throw new Error('HTTP ' + r.status + ': ' + (await r.text()).slice(0, 200));
  const parser = makeParser(onToken), dec = new TextDecoder(), rd = r.body.getReader();
  for (;;) { const x = await rd.read(); if (x.done) break; parser.feed(dec.decode(x.value, { stream: true })); }
  parser.end();
}

async function listModels(cfg) {
  const ollama = cfg.provider === 'ollama';
  const base = cfg.base.replace(/\/+$/, '');
  const headers = {};
  if (!ollama && cfg.key) headers.Authorization = 'Bearer ' + cfg.key;
  const r = await fetch(ollama ? base + '/api/tags' : base + '/models', { headers });
  if (!r.ok) throw new Error('HTTP ' + r.status);
  const j = await r.json();
  return ollama ? (j.models || []).map(m => m.name) : (j.data || []).map(m => m.id);
}

if (typeof module !== 'undefined') module.exports = { ACTIONS, MODES, MODE_INSTRUCTIONS, GENERAL_BASE, MEMOIR_RULES, buildMessages, makeParser, chat, listModels, slug, clip, strip };
