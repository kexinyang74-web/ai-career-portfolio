'use strict';
const $ = (s, root = document) => root.querySelector(s);
const $$ = (s, root = document) => [...root.querySelectorAll(s)];
const state = {session: null, view: 'create', busy: false, profile: null, filter: '', topics: new Map(), health: null};
const labels = {create: '开始选题', favorites: '收藏夹', history: '历史记录', profile: '账号定位'};
let toastTimer;

function el(tag, text, cls) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (cls) node.className = cls;
  return node;
}
function button(text, action, cls = '') {
  const node = el('button', text, cls);
  node.type = 'button'; node.addEventListener('click', action); return node;
}
function notify(text) {
  $('#toast').textContent = text; $('#toast').hidden = false;
  clearTimeout(toastTimer); toastTimer = setTimeout(() => $('#toast').hidden = true, 3500);
}
async function api(path, method = 'GET', data) {
  let response;
  try {
    response = await fetch('/api' + path, {method, headers: data === undefined ? {} : {'Content-Type': 'application/json'}, body: data === undefined ? undefined : JSON.stringify(data)});
  } catch { throw new Error('无法连接本机服务。请确认启动窗口仍在运行，再重试。'); }
  let result;
  try { result = await response.json(); } catch { throw new Error('服务未返回有效结果，请重试。'); }
  if (!response.ok) throw new Error(typeof result.detail === 'string' ? result.detail : '操作没有完成，请检查输入后重试。');
  return result;
}
function busy(value, label) {
  state.busy = value;
  $('#busy').hidden = !value;
  $('#busy-label').textContent = label || '正在整理你的灵感…';
  $$('button, input, textarea, select').forEach(n => { if (n.id !== 'close-dialog') n.disabled = value; });
  if (!value) syncComposer();
}
async function run(action, label) {
  if (state.busy) return;
  $('#error').hidden = true; busy(true, label);
  try { await action(); }
  catch (error) { $('#error').textContent = error.message; $('#error').hidden = false; }
  finally { busy(false); }
}
function empty(title, description, art = false) {
  const box = el('div', undefined, 'empty');
  if (art) {
    const picture = el('div', undefined, 'seed-art'); picture.setAttribute('aria-hidden', 'true');
    picture.append(el('span', undefined, 'leaf'), el('span', undefined, 'leaf right'), el('span', undefined, 'soil')); box.append(picture);
  }
  box.append(el('h3', title), el('p', description));
  if (art) { const tags = el('div', undefined, 'empty-tags'); ['真实经历', '具体问题', '可亲自验证'].forEach(t => tags.append(el('span', t))); box.append(tags); }
  return box;
}
async function showView(name) {
  state.view = name;
  $$('.view').forEach(n => n.hidden = n.id !== 'view-' + name);
  $$('.nav').forEach(n => n.classList.toggle('active', n.dataset.view === name));
  $('#breadcrumb').textContent = labels[name];
  if (name === 'favorites') await loadFavorites();
  if (name === 'history') await loadHistory();
  if (name === 'profile') fillProfile();
}
function renderProfileSummary() {
  $('#audience-summary').textContent = state.profile.audience;
  $('#platform-summary').textContent = state.profile.primary_platform + '为主';
  $('#budget-summary').textContent = `${state.profile.time_budget_hours} 小时亲测与创作`;
}
function fillProfile() {
  const form = $('#profile-form'), p = state.profile;
  ['audience', 'positioning', 'primary_platform', 'time_budget_hours'].forEach(k => form.elements[k].value = p[k]);
  form.elements.secondary_platforms.value = p.secondary_platforms.join('，');
  ['AI工具', '学习成长', '生活管理'].forEach((k, i) => form.elements[['weight-ai','weight-growth','weight-life'][i]].value = p.weights[k]);
}
function pendingMessage() {
  const messages = state.session?.messages || [];
  return messages.at(-1)?.role === 'user' ? messages.at(-1) : null;
}
function syncComposer() {
  const pending = pendingMessage();
  $('#send').textContent = pending ? '重试回复 ↗' : '发送 ↗';
  $('#message-input').readOnly = !!pending;
  if (pending) $('#message-input').value = pending.content;
}
function renderSession() {
  const s = state.session;
  const messages = $('#messages'); messages.replaceChildren();
  const list = s ? s.messages : [{role: 'assistant', content: '最近在工作、学习或生活中，有哪件事让你觉得费时、困惑，或者想分享给同龄人？'}];
  list.forEach(m => {
    const row = el('div', undefined, 'message ' + m.role);
    row.append(el('span', m.role === 'user' ? '我' : '✳', 'message-avatar'), el('div', m.content, 'bubble')); messages.append(row);
  });
  messages.scrollTop = messages.scrollHeight;
  const rounds = list.filter(m => m.role === 'user').length;
  $('#round-count').textContent = rounds ? `已聊 ${rounds} 轮` : '轻松聊几句';
  $('#generate-hint').textContent = rounds >= 2 ? '已经有了一些线索，可以开始生成，也可以继续补充。' : '还没想清楚也没关系，可以先看看灵感。';
  $('#generate').textContent = s?.topics?.length ? '✧ 根据反馈重新推荐' : '✧ 现在生成选题';
  const container = $('#topics'); container.replaceChildren();
  (s?.topics || []).forEach(t => container.append(topicCard(t)));
  if (!s?.topics?.length) container.append(empty('好选题，从一点真实开始', '聊聊你的经历，再点击「现在生成」。\n你的下一篇内容，也许就藏在今天的小事里。', true));
  $('#topic-count').textContent = s?.topics?.length ? `${s.topics.length} 个想法 · 第 ${s.batch} 轮` : '等待发芽';
  $('#research-notice').textContent = s?.notice || ''; $('#research-notice').hidden = !s?.notice;
  $('#previous-wrap').hidden = !s?.previous_topics?.length;
  $('#previous-topics').replaceChildren(...(s?.previous_topics || []).map(t => topicCard(t)));
  syncComposer();
}
function topicCard(topic, favoriteView = false) {
  state.topics.set(topic.id, topic);
  const card = el('article', undefined, 'topic-card'); card.dataset.id = topic.id;
  const top = el('div', undefined, 'card-top');
  top.append(el('span', topic.category, 'category ' + ({学习成长:'growth',生活管理:'life'}[topic.category] || '')), el('span', `约 ${topic.estimated_hours} 小时`, 'card-time'));
  card.append(top, el('h3', topic.title));
  [['读者痛点',topic.pain_point],['创作角度',topic.angle],['推荐理由',topic.reason]].forEach(([label, text]) => {
    const p = el('p'); p.append(el('strong', label + ' · '), document.createTextNode(text)); card.append(p);
  });
  const missing = el('p'); missing.append(el('strong','待亲测 · '), document.createTextNode(topic.to_test.join('；'))); card.append(missing);
  if (topic.missing_info.length) { const p = el('p'); p.append(el('strong', '待补充 · '), document.createTextNode(topic.missing_info.join('；'))); card.append(p); }
  card.append(el('div', topic.platforms.join(' / ') + ' · ' + topic.verification, 'card-meta'));
  const actions = el('div', undefined, 'card-actions');
  actions.append(button(topic.favorite ? '♥ 已收藏' : '♡ 收藏', () => patch(topic.id, {favorite: !topic.favorite}), topic.favorite ? 'selected' : ''));
  actions.append(button('感兴趣', () => patch(topic.id, {feedback: topic.feedback === '感兴趣' ? '' : '感兴趣'}), topic.feedback === '感兴趣' ? 'selected' : ''));
  actions.append(button('不适合', () => patch(topic.id, {feedback: topic.feedback === '不适合' ? '' : '不适合'}), topic.feedback === '不适合' ? 'selected' : ''));
  if (favoriteView) {
    const select = el('select'); select.setAttribute('aria-label', topic.title + '的创作状态');
    ['待创作','已发布','放弃'].forEach(s => { const option = el('option', s); option.value = s; select.append(option); });
    select.value = topic.status; select.addEventListener('change', () => patch(topic.id, {status: select.value})); actions.append(select);
  }
  actions.append(button(topic.plan ? '查看策划单 ↗' : '展开策划单 ↗', () => openPlan(topic.id), 'expand')); card.append(actions);
  if (topic.feedback) {
    const wrap = el('div', undefined, 'feedback-note');
    const input = el('input'); input.maxLength = 500; input.placeholder = '补充原因，下一轮会参考（可选）'; input.value = topic.feedback_note; input.setAttribute('aria-label', '选题反馈原因');
    wrap.append(input, button('保存反馈', () => patch(topic.id, {feedback_note: input.value}), 'text-button')); card.append(wrap);
  }
  return card;
}
async function refreshSession() {
  if (state.session) { state.session = await api('/sessions/' + state.session.id); renderSession(); }
}
function patch(id, data) {
  return run(async () => { await api('/topics/' + id, 'PATCH', data); await refreshSession(); if (state.view === 'favorites') await loadFavorites(); notify('已保存'); }, '正在保存…');
}
async function loadFavorites() {
  const topics = await api('/favorites' + (state.filter ? '?status=' + encodeURIComponent(state.filter) : ''));
  $('#favorites').replaceChildren(...topics.map(t => topicCard(t, true)));
  if (!topics.length) $('#favorites').append(empty('留一点灵感给下一篇', '选题卡片上的「收藏」，会把想做的内容留在这里。'));
}
async function loadHistory() {
  const sessions = await api('/sessions'); $('#history').replaceChildren();
  sessions.forEach(s => {
    const row = button('', () => run(async () => { state.session = await api('/sessions/' + s.id); $('#message-input').value = ''; renderSession(); await showView('create'); }), 'history-item');
    const left = el('div'); left.append(el('strong', s.title), el('small', new Date(s.updated_at).toLocaleString('zh-CN') + ` · ${s.batch} 轮推荐`)); row.append(left, el('span','继续这段对话 ↗')); $('#history').append(row);
  });
  if (!sessions.length) $('#history').append(empty('还没有对话记录', '开始聊聊你的经历，记录会自动保存在这里。'));
}
function briefSection(title, content, ordered = false) {
  const section = el('section', undefined, 'brief-section'); section.append(el('h3', title));
  if (Array.isArray(content)) { const list = el(ordered ? 'ol' : 'ul'); content.forEach(t => list.append(el('li', t))); section.append(list); }
  else section.append(el('p', content));
  return section;
}
function renderPlan(topic) {
  const root = $('#plan-content'); root.replaceChildren(el('h2', topic.title), el('div', `${topic.category} · 约 ${topic.estimated_hours} 小时 · ${topic.verification}`, 'brief-label'));
  const plan = topic.plan;
  root.append(briefSection('要解决的核心问题', plan.core_question), briefSection('拟验证观点 · 不是既定结论', plan.hypotheses), briefSection('亲测步骤', plan.test_steps, true), briefSection('待补素材', plan.materials), briefSection('内容边界', plan.boundaries));
  if (topic.external_claims.length) root.append(briefSection('仍需核对的外部事实', topic.external_claims));
  const sources = briefSection('参考来源', topic.sources.length ? '搜索来源仅供核对，不能替代你的实际测试。' : '尚无经过搜索工具返回的参考来源，相关外部事实未核实。');
  topic.sources.forEach(source => {
    const p = el('p'); const a = el('a', source.title);
    try { const url = new URL(source.url); if (!['https:', 'http:'].includes(url.protocol)) return; a.href = url.href; } catch { return; }
    a.target = '_blank'; a.rel = 'noopener noreferrer'; p.append(a, el('span', ' · ' + source.claim)); sources.append(p);
  });
  if (topic.external_claims.length) sources.append(button('重新查证', () => run(async () => {
    const result = await api('/topics/' + topic.id + '/research', 'POST'); renderPlan(result.topic); await refreshSession(); notify(result.notice || '已更新参考来源');
  }, '正在尝试官方联网查证…'), 'button secondary'));
  root.append(sources);
}
function openPlan(id) {
  return run(async () => { const topic = await api('/topics/' + id + '/plan', 'POST'); renderPlan(topic); $('#plan-dialog').showModal(); $('#close-dialog').focus(); $('#plan-dialog').scrollTop = 0; await refreshSession(); }, '正在整理策划单与亲测步骤…');
}
async function ensureSession() {
  if (!state.session) state.session = await api('/sessions', 'POST');
}
$$('[data-view]').forEach(b => b.addEventListener('click', () => run(() => showView(b.dataset.view), '正在打开…')));
$('#new-session').addEventListener('click', () => run(async () => {
  state.session = await api('/sessions', 'POST'); $('#message-input').value = ''; renderSession();
}));
$('#chat-form').addEventListener('submit', event => {
  event.preventDefault(); const text = $('#message-input').value.trim(); if (!text) return;
  run(async () => {
    await ensureSession(); const pending = pendingMessage();
    const payload = {text: pending?.content || text, request_id: pending?.request_id || crypto.randomUUID()};
    try { state.session = await api('/sessions/' + state.session.id + '/messages', 'POST', payload); $('#message-input').value = ''; renderSession(); }
    catch (error) { try { await refreshSession(); } catch { /* keep draft if the local server is offline */ } throw error; }
  }, '正在听你说，整理下一个问题…');
});
$('#generate').addEventListener('click', () => run(async () => {
  // Preserve a typed but unsent experience before generating.
  await ensureSession();
  if ($('#message-input').value.trim() && !pendingMessage()) throw new Error('输入框里还有一段经历，请先发送，避免遗漏这部分信息。');
  state.session = await api('/sessions/' + state.session.id + '/generate', 'POST'); renderSession();
  state.health = await api('/health'); notify('选题已生成，挑两个你愿意动手做的吧。');
}, '正在策划选题，必要时尝试查证；可能需要一两分钟…'));
$('#profile-form').addEventListener('submit', event => {
  event.preventDefault();
  run(async () => {
    const f = $('#profile-form').elements;
    const profile = {audience:f.audience.value.trim(), positioning:f.positioning.value.trim(), primary_platform:f.primary_platform.value.trim(), secondary_platforms:f.secondary_platforms.value.split(/[,，]/).map(x => x.trim()).filter(Boolean), weights:{'AI工具':Number(f['weight-ai'].value),'学习成长':Number(f['weight-growth'].value),'生活管理':Number(f['weight-life'].value)}, time_budget_hours:Number(f.time_budget_hours.value)};
    if (Object.values(profile.weights).reduce((a,b) => a+b, 0) !== 100) throw new Error('三个内容方向的比例需要合计为100%。');
    state.profile = await api('/profile', 'PUT', profile); renderProfileSummary(); notify('账号定位已保存');
  }, '正在保存定位…');
});
$$('#favorite-filters button').forEach(b => b.addEventListener('click', () => run(async () => {
  state.filter = b.dataset.status; $$('#favorite-filters button').forEach(x => x.classList.toggle('active', x === b)); await loadFavorites();
})));
$('#close-dialog').addEventListener('click', () => $('#plan-dialog').close());
$('#plan-dialog').addEventListener('click', event => { if (event.target === $('#plan-dialog')) { const rect = event.target.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) event.target.close(); } });
renderSession();
run(async () => {
  const [profile, health, history] = await Promise.all([api('/profile'), api('/health'), api('/sessions')]);
  state.profile = profile; state.health = health; renderProfileSummary();
  if (!health.configured) { $('#connection').textContent = '尚未配置 DeepSeek 密钥。在项目的 .env 文件中填写 DEEPSEEK_API_KEY 后重启；目前可以编辑定位、查看历史。'; $('#connection').hidden = false; }
  if (history.length) { state.session = await api('/sessions/' + history[0].id); renderSession(); }
}, '正在打开你的创作空间…');
