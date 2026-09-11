"use strict";
const $ = (s, root = document) => root.querySelector(s);
const $$ = (s, root = document) => [...root.querySelectorAll(s)];
const FORMS = ["图文", "口播", "录屏教程", "生活记录", "混合视频"];
const STATUSES = [
  "待策划",
  "待补素材",
  "写稿中",
  "待制作",
  "待发布",
  "已发布",
  "已复盘",
  "暂停",
  "放弃",
];
const LABELS = {
  home: "本周工作台",
  profile: "账号定位",
  materials: "素材库",
  topics: "选题池",
  works: "作品库",
  reviews: "复盘库",
};
const KINDS = {
  brief: "策划单",
  draft: "稿件",
  revise: "局部修改稿",
  package: "发布包装",
  review: "单篇复盘",
  period_review: "周期复盘",
  case: "案例拆解",
};
const state = {
  data: null,
  work: null,
  variantId: null,
  busy: false,
  manualSaved: "",
  manualSource: null,
  manualVariant: null,
  view: "home",
  sectionEdits: new Map(),
};
const rid = () => crypto.randomUUID();
const today = () => new Date().toLocaleDateString("en-CA");
const val = (form, name) => form.elements.namedItem(name).value;
const number = (form, name) =>
  val(form, name).trim() === "" ? null : Number(val(form, name));
const lines = (text) =>
  text
    .split(/[\n,，]/)
    .map((x) => x.trim())
    .filter(Boolean);
function el(tag, text, cls) {
  const n = document.createElement(tag);
  if (text !== undefined) n.textContent = text;
  if (cls) n.className = cls;
  return n;
}
function action(text, fn, cls = "") {
  const b = el("button", text, cls);
  b.type = "button";
  b.addEventListener("click", () => run(fn));
  return b;
}
function link(text, url) {
  const a = el("a", text);
  a.href = url;
  return a;
}
function empty(text, detail = "") {
  const n = el("div", undefined, "empty");
  n.append(el("strong", text), el("span", detail));
  return n;
}
function option(value, text) {
  const n = el("option", text);
  n.value = value;
  return n;
}
function fill(form, data) {
  for (const [key, value] of Object.entries(data || {})) {
    const input = form.elements.namedItem(key);
    if (!input || input.type === "file") continue;
    if (input.type === "checkbox") input.checked = Boolean(value);
    else input.value = Array.isArray(value) ? value.join("，") : (value ?? "");
  }
}
function field(label, value = "", type = "text") {
  const wrap = el("label", label),
    input = el(type === "textarea" ? "textarea" : "input");
  if (type !== "textarea") input.type = type;
  input.value = value ?? "";
  wrap.append(input);
  return { wrap, input };
}
function notify(message) {
  $("#studio-toast").textContent = message;
  $("#studio-toast").hidden = false;
  clearTimeout(notify.timer);
  notify.timer = setTimeout(() => ($("#studio-toast").hidden = true), 4000);
}
async function api(path, method = "GET", body) {
  let response, pendingKey;
  if (body?.request_id) {
    const payload = { ...body };
    delete payload.request_id;
    const fingerprint = await crypto.subtle.digest(
      "SHA-256",
      new TextEncoder().encode(
        method + " " + path + " " + JSON.stringify(payload),
      ),
    );
    pendingKey =
      "studio-pending-" +
      [...new Uint8Array(fingerprint)]
        .map((n) => n.toString(16).padStart(2, "0"))
        .join("");
    const previous = sessionStorage.getItem(pendingKey);
    body = { ...body, request_id: previous || body.request_id };
    sessionStorage.setItem(pendingKey, body.request_id);
  }
  try {
    response = await fetch("/api/studio" + path, {
      method,
      headers: body === undefined ? {} : { "Content-Type": "application/json" },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  } catch {
    throw Error("无法连接本机服务。请确认启动窗口仍在运行，再重试。");
  }
  let result;
  try {
    result = await response.json();
  } catch {
    throw Error("服务没有返回有效内容，请稍后重试。");
  }
  if (!response.ok) {
    let detail = result.detail;
    if (Array.isArray(detail))
      detail = detail
        .map((x) => `${(x.loc || []).slice(1).join(" / ")}：${x.msg}`)
        .join("\n");
    throw Error(
      typeof detail === "string" ? detail : "操作未完成，请检查输入后重试。",
    );
  }
  if (pendingKey) sessionStorage.removeItem(pendingKey);
  return result;
}
async function run(fn) {
  if (state.busy) return;
  state.busy = true;
  $("#studio-error").hidden = true;
  $("#studio-busy").hidden = false;
  const locked = $$(
    "button:not(:disabled),input:not(:disabled),textarea:not(:disabled),select:not(:disabled)",
  );
  locked.forEach((n) => (n.disabled = true));
  try {
    await fn();
  } catch (e) {
    $("#studio-error").textContent = e.message;
    $("#studio-error").hidden = false;
  } finally {
    state.busy = false;
    $("#studio-busy").hidden = true;
    locked.forEach((n) => {
      if (n.isConnected) n.disabled = false;
    });
  }
}
function submit(id, fn) {
  $(id).addEventListener("submit", (e) => {
    e.preventDefault();
    run(() => fn(e.currentTarget));
  });
}
function allArtifacts() {
  if (!state.work) return [];
  const result = [
    ...(state.work.artifacts || []),
    ...(state.work.variants || []).flatMap((v) => v.artifacts || []),
  ];
  return [...new Map(result.map((a) => [a.id, a])).values()].sort((a, b) =>
    String(b.created_at).localeCompare(String(a.created_at)),
  );
}
function variant() {
  return state.work?.variants.find(
    (v) => String(v.id) === String(state.variantId),
  );
}
function requireVariant() {
  const v = variant();
  if (!v) throw Error("请先为作品添加一种内容形式。");
  return v;
}
function formOptions(select, items) {
  select.replaceChildren(...items.map((x) => option(x, x)));
}
async function refresh() {
  state.data = await api("/bootstrap");
  renderHome();
  renderMaterialList();
  renderWorkList();
}
async function navigate(view) {
  if (!LABELS[view]) view = "home";
  state.view = view;
  $$(".view").forEach((n) => (n.hidden = n.id !== "view-" + view));
  $$("[data-view]").forEach((n) => {
    const selected = n.dataset.view === view;
    n.classList.toggle("active", selected);
    n.setAttribute("aria-current", selected ? "page" : "false");
  });
  $("#breadcrumb").textContent = LABELS[view];
  if (view === "profile") {
    renderProfile();
    await loadCandidates();
  }
  if (view === "topics") await loadFavorites();
  if (view === "reviews") await loadReviews();
  if (view === "works" && !state.work && state.data.works.length)
    await openWork(state.data.works[0].id);
}
function workArtifacts(w) {
  return [
    ...new Map(
      [
        ...(w.artifacts || []),
        ...(w.variants || []).flatMap((v) => v.artifacts || []),
      ].map((a) => [a.id, a]),
    ).values(),
  ].sort((a, b) => String(b.created_at).localeCompare(String(a.created_at)));
}
function workMissing(w) {
  const artifacts = workArtifacts(w),
    selected = [];
  const brief = artifacts.find((a) => a.kind === "brief");
  if (brief) selected.push(brief);
  for (const v of w.variants || []) {
    const draft = artifacts.find(
      (a) => ["draft", "revise"].includes(a.kind) && a.variant_id === v.id,
    );
    if (draft) selected.push(draft);
  }
  return [...new Set(selected.flatMap((a) => a.data?.missing || []))];
}
function nextStep(w) {
  const variants = w.variants || [],
    artifacts = workArtifacts(w);
  if (!w.material_ids?.length) return "补充并关联真实素材";
  if (!variants.length) return "选择一种内容形式";
  if (!artifacts.some((a) => ["draft", "revise"].includes(a.kind)))
    return "写下第一版稿件";
  if (!artifacts.some((a) => a.kind === "package"))
    return "准备标题、封面与发布包装";
  if (!variants.some((v) => v.publications?.length))
    return "完成制作并登记发布";
  if (!artifacts.some((a) => a.kind === "review"))
    return "记录观察，完成单篇复盘";
  return "把这次经验带入下一轮选题";
}
function renderHome() {
  const weekly = state.data.weekly || {};
  const works = [...(state.data.works || [])].sort((a, b) =>
    String(b.updated_at || b.created_at).localeCompare(
      String(a.updated_at || a.created_at),
    ),
  );
  const stats = [
    [
      "正在创作",
      works.filter((w) =>
        (w.variants || []).some(
          (v) => !["已复盘", "放弃", "暂停"].includes(v.status),
        ),
      ).length,
    ],
    ["素材积累", (state.data.materials || []).length],
    ["本周计划", `${weekly.planned_hours || 0} h`],
    [
      "每周可用",
      `${weekly.budget_hours ?? state.data.profile.weekly_hours ?? 0} h`,
    ],
  ];
  $("#stats").replaceChildren(
    ...stats.map(([title, value]) => {
      const n = el("div", undefined, "stat");
      n.append(el("span", title), el("strong", String(value)));
      return n;
    }),
  );
  renderWeek(weekly);
  $("#recent-works").replaceChildren(
    ...works.slice(0, 3).map((w) => {
      const n = el("article", undefined, "card");
      n.append(
        el("h3", w.title),
        el(
          "p",
          `${(w.variants || []).length} 种形式 · ${String(w.updated_at || w.created_at).slice(0, 10)}`,
        ),
        el("p", "下一步：" + nextStep(w), "muted"),
      );
      const missing = workMissing(w);
      if (missing.length)
        n.append(
          el(
            "p",
            "待补充：" +
              missing.slice(0, 3).join("；") +
              (missing.length > 3 ? `（共 ${missing.length} 项）` : ""),
            "muted",
          ),
        );
      n.append(
        action("继续创作 ↗", async () => {
          await openWork(w.id);
          location.hash = "works";
        }),
      );
      return n;
    }),
  );
  if (!works.length)
    $("#recent-works").append(
      empty(
        "第一篇作品，从这里开始",
        "先记一条素材，或直接创建一个你想分享的主题。",
      ),
    );
}
function renderWeek(weekly) {
  $("#week-summary").textContent =
    `计划 ${weekly.planned_hours || 0} 小时 / 预算 ${weekly.budget_hours ?? state.data.profile.weekly_hours ?? 0} 小时 · 已记录实际 ${weekly.actual_hours || 0} 小时`;
  $("#weekly-tasks").replaceChildren(
    ...(weekly.tasks || []).map((t) => taskCard(t, true)),
  );
  if (!weekly.tasks?.length)
    $("#weekly-tasks").append(
      empty("给创作留一点时间", "在作品中生成制作清单，再按每周预算排期。"),
    );
  $("#unscheduled-tasks").replaceChildren(
    ...(weekly.unscheduled || []).map((t) => taskCard(t, true)),
  );
}
function renderProfile() {
  const p = state.data.profile;
  fill($("#profile-form"), p);
  $("#interview-form").elements.interview.value =
    typeof p.interview === "string"
      ? p.interview
      : JSON.stringify(p.interview || "");
  $("#profile-forms").replaceChildren(
    ...FORMS.map((name) => {
      const n = el("label", name),
        c = el("input");
      c.type = "checkbox";
      c.name = "content_forms";
      c.value = name;
      c.checked = (p.content_forms || []).includes(name);
      n.prepend(c);
      return n;
    }),
  );
  $("#weight-fields").replaceChildren(
    ...Object.entries(p.weights || {}).map(([name, weight]) =>
      weightRow(name, weight),
    ),
  );
  $("#profile-versions").replaceChildren(
    el(
      "p",
      `当前版本 v${p.version || 1} · 共 ${(state.data.profile_versions || []).length} 个保存版本`,
    ),
  );
  const history = el("details");
  history.append(el("summary", "查看历史定位"));
  for (const old of state.data.profile_versions || []) {
    const item = el(
      "p",
      `v${old.version} · ${String(old.created_at).slice(0, 16)}\n${old.positioning || old.profile?.positioning || ""}`,
    );
    history.append(item);
  }
  $("#profile-versions").append(history);
  if (!$("#profile-form").elements.on_camera.value) {
    $("#profile-form").elements.on_camera.append(
      option(p.on_camera || "视内容决定", p.on_camera || "视内容决定"),
    );
    $("#profile-form").elements.on_camera.value = p.on_camera || "视内容决定";
  }
}
function weightRow(name = "", weight = 0) {
  const row = el("div", undefined, "weight-row");
  const direction = field("方向名称", name),
    percent = field("比例 %", weight, "number");
  direction.input.dataset.direction = "";
  direction.input.required = true;
  percent.input.dataset.weight = "";
  percent.input.min = 0;
  percent.input.max = 100;
  percent.input.step = 1;
  percent.input.required = true;
  row.append(
    direction.wrap,
    percent.wrap,
    action("移除方向", () => row.remove()),
  );
  return row;
}
async function saveProfile(form) {
  const body = { ...state.data.profile };
  for (const k of ["id", "version", "created_at", "updated_at"]) delete body[k];
  for (const name of [
    "audience",
    "positioning",
    "goal",
    "primary_platform",
    "voice",
    "boundaries",
    "on_camera",
  ])
    body[name] = val(form, name);
  for (const name of ["secondary_platforms", "columns"])
    body[name] = lines(val(form, name));
  body.content_forms = $$("[name=content_forms]:checked", form).map(
    (n) => n.value,
  );
  body.weekly_hours = number(form, "weekly_hours");
  body.time_budget_hours = number(form, "time_budget_hours");
  body.confirmed = form.elements.confirmed.checked;
  body.interview = val($("#interview-form"), "interview");
  const entries = $$(".weight-row", form).map((row) => [
    $("[data-direction]", row).value.trim(),
    Number($("[data-weight]", row).value),
  ]);
  if (
    entries.some(([name]) => !name) ||
    new Set(entries.map(([name]) => name)).size !== entries.length
  )
    throw Error("每个内容方向都需要填写不同的名称。");
  body.weights = Object.fromEntries(entries);
  if (Object.values(body.weights).reduce((a, b) => a + b, 0) !== 100)
    throw Error("内容方向比例需要合计 100%。");
  await api("/profile", "PUT", body);
  await refresh();
  renderProfile();
  notify("定位已保存为新版本");
}
async function loadCandidates() {
  const data = await api("/positioning");
  renderCandidates(Array.isArray(data) ? data : []);
}
function renderCandidates(artifacts) {
  const root = $("#positioning-candidates");
  root.replaceChildren();
  for (const artifact of artifacts.slice(-3).reverse()) {
    const candidates = artifact.data?.candidates || [];
    for (const [i, c] of candidates.entries()) {
      const card = el("article", undefined, "panel");
      card.dataset.positioningId = artifact.id;
      card.append(el("span", `候选 ${i + 1}`, "tag"), el("h3", c.positioning));
      for (const [key, label] of [
        ["audience", "服务人群"],
        ["pillars", "内容支柱"],
        ["difference", "差异"],
        ["voice", "表达语气"],
        ["boundaries", "边界"],
        ["columns", "栏目"],
        ["tradeoff", "取舍"],
      ])
        if (c[key])
          card.append(
            el(
              "p",
              `${label}：${Array.isArray(c[key]) ? c[key].join(" / ") : c[key]}`,
              "muted",
            ),
          );
      card.append(
        action("采用并填写定位", () => {
          fill($("#profile-form"), c);
          notify("已填写候选，请检查后保存定位新版本。");
          $("#profile-form").scrollIntoView({ behavior: "smooth" });
        }),
      );
      root.append(card);
    }
  }
}
function materialCard(m) {
  const n = el("article", undefined, "card");
  n.append(
    el("span", `${m.kind} · ${m.verification}`, "tag"),
    el("h3", m.title),
    el("p", m.text),
  );
  if (m.url) {
    try {
      const u = new URL(m.url);
      if (["https:", "http:"].includes(u.protocol)) {
        const a = link("查看参考来源 ↗", u.href);
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        n.append(a);
      }
    } catch {}
  }
  if (m.missing?.length)
    n.append(el("p", "待补充：" + m.missing.join("；"), "muted"));
  const images = el("div", undefined, "images");
  for (const img of m.images || []) {
    const a = link("", img.url),
      im = el("img");
    im.src = img.url;
    im.alt = img.name || m.title + " 附件";
    im.loading = "lazy";
    a.target = "_blank";
    a.rel = "noopener";
    a.append(im);
    images.append(a);
  }
  n.append(images);
  const buttons = el("div", undefined, "actions");
  buttons.append(
    action("编辑素材", () => {
      fill($("#material-form"), m);
      $("#material-form-title").textContent = "编辑素材";
      $("#material-form").scrollIntoView({ behavior: "smooth" });
    }),
    action("06 · 案例拆解", async () => {
      await api(`/materials/${m.id}/analyze`, "POST", { request_id: rid() });
      await refresh();
      notify("案例拆解已保存");
    }),
  );
  n.append(buttons);
  for (const a of m.analyses || []) {
    const d = el("details");
    d.append(
      el("summary", "查看案例拆解"),
      el("div", a.data?.markdown || "", "prose"),
    );
    if (a.data?.missing?.length)
      d.append(el("p", "待补充：" + a.data.missing.join("；"), "muted"));
    n.append(d);
  }
  return n;
}
function renderMaterialList() {
  $("#material-list").replaceChildren(
    ...state.data.materials.map(materialCard),
  );
  $("#material-count").textContent = `${state.data.materials.length} 条素材`;
  if (!state.data.materials.length)
    $("#material-list").append(
      empty(
        "今天的小事，可能是明天的作品",
        "记下真实过程，也保留没弄清楚的问题。",
      ),
    );
}
async function saveMaterial(form) {
  const body = {};
  for (const k of ["title", "kind", "text", "url", "verification"])
    body[k] = val(form, k);
  body.missing = lines(val(form, "missing"));
  const existing = val(form, "id");
  const m = await api(
    "/materials" + (existing ? "/" + existing : ""),
    existing ? "PUT" : "POST",
    body,
  );
  form.elements.id.value = m.id;
  for (const file of form.elements.images.files) {
    if (!["image/png", "image/jpeg", "image/webp"].includes(file.type))
      throw Error("图片支持 PNG、JPEG 或 WebP。素材文字已保存。");
    const response = await fetch(`/api/studio/materials/${m.id}/image`, {
      method: "POST",
      headers: { "Content-Type": file.type },
      body: file,
    });
    if (!response.ok) {
      const err = await response.json();
      throw Error(
        typeof err.detail === "string"
          ? err.detail
          : "图片保存失败，素材文字已保存。请重试附件。",
      );
    }
  }
  form.elements.images.value = "";
  await refresh();
  notify("素材已保存");
}
async function loadFavorites() {
  const response = await fetch("/api/favorites");
  if (!response.ok) throw Error("暂时无法读取收藏选题，请稍后重试。");
  const data = await response.json();
  const topics = Array.isArray(data) ? data : data.topics || [];
  $("#favorite-list").replaceChildren(
    ...topics.map((t) => {
      const n = el("article", undefined, "card");
      n.append(
        el("span", t.category || "待验证选题", "tag"),
        el("h3", t.title),
        el("p", t.angle || t.reason || t.pain_point || ""),
        action(
          "由此创建作品",
          async () => {
            const w = await api("/works", "POST", {
              title: t.title,
              topic_id: t.id,
              material_ids: [],
              request_id: rid(),
            });
            await refresh();
            await openWork(w.id);
            location.hash = "works";
          },
          "primary",
        ),
      );
      return n;
    }),
  );
  if (!topics.length)
    $("#favorite-list").append(
      empty("还没有收藏的选题", "进入选题访谈，收藏你想亲自验证和分享的内容。"),
    );
}
function renderWorkList() {
  $("#work-list").replaceChildren(
    ...state.data.works.map((w) => {
      const b = action(w.title, () => openWork(w.id));
      b.classList.toggle("active", w.id === state.work?.id);
      b.append(
        el(
          "small",
          `${(w.variants || []).length} 种形式 · ${String(w.updated_at || w.created_at).slice(0, 10)}`,
        ),
      );
      return b;
    }),
  );
  if (!state.data.works.length)
    $("#work-list").append(empty("还没有作品", "先给这一篇起个名字。"));
}
function resetManual() {
  const f = $("#manual-artifact-form");
  f.reset();
  state.manualSaved = "";
  state.manualSource = null;
  state.manualVariant = null;
  $("#editor-status").textContent = "手动编辑与导出无需配置 AI 密钥。";
}
async function openWork(id) {
  if (state.work) await saveManualIfDirty();
  state.work = await api("/works/" + id);
  const chosen = state.work.variants.find(
    (v) => String(v.id) === String(state.variantId),
  );
  state.variantId = chosen?.id || state.work.variants[0]?.id || null;
  sessionStorage.setItem("studio-work", String(id));
  renderWorkList();
  renderWork();
  resetManual();
  resetPublication();
}
async function reloadWork() {
  const id = state.work.id;
  state.work = await api("/works/" + id);
  state.data.works = state.data.works.map((work) =>
    work.id === state.work.id ? state.work : work,
  );
  renderHome();
  renderWorkList();
  renderWork();
}
function renderWork() {
  $("#work-detail").hidden = false;
  $("#work-title").textContent = state.work.title;
  $("#work-edit-form").elements.title.value = state.work.title;
  $("#work-materials").replaceChildren(
    ...state.data.materials.map((m) => {
      const l = el("label", m.title),
        c = el("input");
      c.type = "checkbox";
      c.value = m.id;
      c.checked = (state.work.material_ids || []).includes(m.id);
      l.prepend(c);
      return l;
    }),
  );
  if (!state.data.materials.length)
    $("#work-materials").append(
      el("span", "先到素材库记录素材，即可在这里关联。", "muted"),
    );
  const p = state.work.profile_snapshot || {};
  $("#profile-snapshot").textContent =
    `${p.positioning || "尚未设置定位"}\n服务人群：${p.audience || "待填写"}\n表达语气：${p.voice || "待填写"}\n边界：${p.boundaries || "待填写"}`;
  $("#variant-picker").replaceChildren(
    ...state.work.variants.map((v) =>
      option(v.id, `${v.form} · ${v.platform} · ${v.status}`),
    ),
  );
  $("#variant-picker").value = state.variantId ?? "";
  $("#variant-status").value = variant()?.status || STATUSES[0];
  $("#variant-platform").value = variant()?.platform || "";
  renderTemplates();
  renderArtifacts();
  renderTasks();
  renderPublications();
  $("#tasks-export").href = `/api/studio/works/${state.work.id}/tasks/export`;
}
function renderTemplates() {
  const old = $("#template-picker").value;
  const templates = state.data.templates?.[variant()?.form] || [];
  $("#template-picker").replaceChildren(
    option("", "自动适配当前形式"),
    ...templates.map((t) =>
      option(
        typeof t === "string" ? t : t.id,
        typeof t === "string" ? t : t.name,
      ),
    ),
  );
  if (templates.includes(old)) $("#template-picker").value = old;
}
function renderArtifacts() {
  const artifacts = allArtifacts();
  const old = $("#source-picker").value;
  $("#source-picker").replaceChildren(
    option("", "不使用已有稿件"),
    ...artifacts
      .filter((a) => ["draft", "revise"].includes(a.kind))
      .map((a) => {
        const v = state.work.variants.find((v) => v.id === a.variant_id);
        return option(
          a.id,
          `${v?.form || "稿件"} · ${KINDS[a.kind]} v${a.version}${a.confirmed ? " · 已确认" : ""}`,
        );
      }),
  );
  if (artifacts.some((a) => String(a.id) === old))
    $("#source-picker").value = old;
  const visible = artifacts.filter(
    (a) => !a.variant_id || String(a.variant_id) === String(state.variantId),
  );
  $("#artifact-list").replaceChildren(
    ...visible.map((a, index) => artifactCard(a, index === 0)),
  );
  if (!visible.length)
    $("#artifact-list").append(
      empty(
        "这里会保留每一次打磨",
        "生成稿件，或保存一个人工版本。确认后的版本仍可导出和另存修改。",
      ),
    );
}
function artifactText(a) {
  const d = a.data || {};
  if (d.markdown) return d.markdown;
  return [
    ...(d.titles || []).map((t, i) => `标题 ${i + 1}：${t}`),
    d.cover && "封面：" + d.cover,
    d.intro,
    ...(d.sections || []).map(
      (s, i) =>
        `${i + 1}. ${s.heading || ""}\n${s.text || ""}\n画面：${s.visual || ""}\n字幕：${s.subtitle || ""}\n时长：${s.seconds ?? ""} 秒\n转场：${s.transition || ""}`,
    ),
    d.closing,
    d.publish_text && "发布文案：" + d.publish_text,
  ]
    .filter(Boolean)
    .join("\n\n");
}
function artifactCard(a, latest = false) {
  const n = el("details", undefined, "artifact");
  n.dataset.artifactId = a.id;
  n.open =
    latest ||
    [...state.sectionEdits.keys()].some((key) => key.startsWith(a.id + ":"));
  const head = el("summary", undefined, "artifact-head");
  head.append(
    el("strong", `${KINDS[a.kind] || a.kind} v${a.version}`),
    el("span", a.confirmed ? "已确认" : "待确认", "tag"),
  );
  n.append(
    head,
    el(
      "p",
      String(a.created_at || "")
        .replace("T", " ")
        .slice(0, 16),
      "muted",
    ),
    el("div", artifactText(a), "prose"),
  );
  if (a.data?.missing?.length)
    n.append(el("p", "待补充：" + a.data.missing.join("；"), "muted"));
  const buttons = el("div", undefined, "actions");
  if (!a.confirmed)
    buttons.append(
      action("确认此版本", async () => {
        await api("/artifacts/" + a.id, "PATCH", { confirmed: true });
        await reloadWork();
        notify("已确认，后续修改将保存为新版本");
      }),
    );
  buttons.append(
    action("复制到人工编辑器", async () => {
      await saveManualIfDirty();
      const f = $("#manual-artifact-form");
      f.elements.kind.value = a.kind === "revise" ? "draft" : a.kind;
      f.elements.markdown.value = artifactText(a);
      state.manualSource = a.id;
      state.manualVariant = a.variant_id;
      state.manualSaved = "";
      $("#editor-status").textContent =
        `正在基于 v${a.version} 编辑，保存后会建立新版本。`;
      f.scrollIntoView({ behavior: "smooth" });
    }),
    link("导出 Markdown ↗", `/api/studio/artifacts/${a.id}/export?format=md`),
  );
  if (a.data?.sections?.length)
    buttons.append(
      link(
        "导出分镜 CSV ↗",
        `/api/studio/artifacts/${a.id}/export?format=csv`,
      ),
    );
  n.append(buttons);
  if (a.data?.sections)
    for (const [index, section] of a.data.sections.entries())
      n.append(sectionEditor(a, index, section));
  return n;
}
function sectionEditor(a, index, section) {
  const key = a.id + ":" + index,
    cached = state.sectionEdits.get(key);
  const d = el("details", undefined, "section-editor");
  d.dataset.sectionIndex = index;
  d.open = Boolean(cached);
  d.append(
    el("summary", `修改第 ${index + 1} 段：${section.heading || "未命名段落"}`),
  );
  const inputs = {};
  for (const [name, label, type] of [
    ["heading", "小节标题", "text"],
    ["text", "正文 / 口播", "textarea"],
    ["visual", "画面说明", "textarea"],
    ["seconds", "时长（秒）", "number"],
    ["subtitle", "字幕", "textarea"],
    ["transition", "转场", "text"],
  ]) {
    const f = field(label, cached?.values?.[name] ?? section[name], type);
    inputs[name] = f.input;
    if (name === "seconds") {
      f.input.min = 0;
      f.input.step = 1;
    }
    d.append(f.wrap);
  }
  const instruction = field(
    "这一段想怎么改？",
    cached?.instruction || "",
    "textarea",
  );
  d.append(instruction.wrap);
  const status = el(
    "p",
    cached ? "有未保存的本段编辑" : "本段修改将另存为新版本",
    "muted",
  );
  d.append(status);
  const values = () =>
    Object.fromEntries(Object.entries(inputs).map(([k, n]) => [k, n.value]));
  const baseline = Object.fromEntries(
    Object.keys(inputs).map((k) => [k, String(section[k] ?? "")]),
  );
  const remember = () => {
    const changed =
      JSON.stringify(values()) !== JSON.stringify(baseline) ||
      instruction.input.value.trim();
    if (changed)
      state.sectionEdits.set(key, {
        values: values(),
        instruction: instruction.input.value,
      });
    else state.sectionEdits.delete(key);
    status.textContent = changed
      ? "有未保存的本段编辑"
      : "本段修改将另存为新版本";
  };
  for (const input of [...Object.values(inputs), instruction.input])
    input.addEventListener("input", remember);
  const editedData = () => {
    const data = structuredClone(a.data);
    data.sections[index] = {
      ...section,
      ...Object.fromEntries(
        Object.entries(inputs).map(([k, n]) => [
          k,
          k === "seconds" ? Number(n.value) : n.value,
        ]),
      ),
    };
    return data;
  };
  const buttons = el("div", undefined, "actions");
  buttons.append(
    action("保存本段人工修改", async () => {
      await api(`/works/${state.work.id}/artifacts`, "POST", {
        kind: "draft",
        variant_id: a.variant_id,
        source_id: a.id,
        data: editedData(),
        request_id: rid(),
      });
      state.sectionEdits.delete(key);
      await reloadWork();
      notify("本段修改已另存新版本");
    }),
    action("让助手修改本段", async () => {
      if (!instruction.input.value.trim())
        throw Error("请先填写这一段的修改要求。");
      await saveManualIfDirty();
      const data = editedData();
      let source = a;
      if (JSON.stringify(data) !== JSON.stringify(a.data)) {
        const pending = state.sectionEdits.get(key);
        if (
          pending?.sourceId &&
          pending.sourceSignature === JSON.stringify(data)
        ) {
          source = { id: pending.sourceId };
        } else {
          source = await api(`/works/${state.work.id}/artifacts`, "POST", {
            kind: "draft",
            variant_id: a.variant_id,
            source_id: a.id,
            data,
            request_id: rid(),
          });
          state.sectionEdits.set(key, {
            values: values(),
            instruction: instruction.input.value,
            sourceId: source.id,
            sourceSignature: JSON.stringify(data),
          });
        }
      }
      await api(`/works/${state.work.id}/generate`, "POST", {
        ...generationSettings(),
        kind: "revise",
        variant_id: a.variant_id,
        source_id: source.id,
        section_index: index,
        instruction: instruction.input.value,
        request_id: rid(),
      });
      state.sectionEdits.delete(key);
      await reloadWork();
      notify("局部修改已生成新版本");
    }),
    action("放弃本段未保存修改", () => {
      state.sectionEdits.delete(key);
      renderArtifacts();
    }),
  );
  d.append(buttons);
  return d;
}
function manualSignature() {
  const f = $("#manual-artifact-form");
  return JSON.stringify([val(f, "kind"), val(f, "markdown")]);
}
async function saveManualIfDirty() {
  const f = $("#manual-artifact-form");
  if (val(f, "markdown").trim() && manualSignature() !== state.manualSaved)
    return saveManual(f, true);
  return null;
}
async function saveManual(f, silent = false) {
  if (!state.work) throw Error("请先创建或选择作品。");
  const markdown = val(f, "markdown");
  if (!markdown.trim()) throw Error("请填写人工稿件正文后保存。");
  const kind = val(f, "kind");
  const variantId =
    kind === "brief" ? null : state.manualVariant || requireVariant().id;
  const a = await api(`/works/${state.work.id}/artifacts`, "POST", {
    kind,
    variant_id: variantId,
    source_id: state.manualSource,
    data: { markdown, missing: [] },
    request_id: rid(),
  });
  state.manualSaved = manualSignature();
  state.manualSource = a.id;
  state.manualVariant = a.variant_id;
  $("#editor-status").textContent =
    `已保存 v${a.version} · 继续编辑后会另存新版本。`;
  if (!silent) {
    await reloadWork();
    notify("人工内容已保存为新版本");
  }
  return a;
}
function generationSettings() {
  const f = $("#generation-form");
  return {
    page_count: number(f, "page_count"),
    duration_seconds: number(f, "duration_seconds"),
    template: val(f, "template"),
    instruction: val(f, "instruction"),
  };
}
async function generate(kind) {
  if (!state.work) throw Error("请先创建或选择作品。");
  const saved = await saveManualIfDirty();
  const v = kind === "brief" ? null : requireVariant();
  let source = $("#source-picker").value || null;
  if (saved && ["draft", "package"].includes(kind)) {
    source = saved.id;
    // Keep the auto-saved source selected so retrying an uncertain response
    // submits the exact same generation request and reuses its request id.
    $("#source-picker").append(
      option(saved.id, `刚保存的人工稿件 v${saved.version}`),
    );
    $("#source-picker").value = saved.id;
  }
  if (kind === "package" && !source)
    throw Error("请先选择一份参考稿件，再生成发布包装。");
  const result = await api(`/works/${state.work.id}/generate`, "POST", {
    ...generationSettings(),
    kind,
    variant_id: v?.id || null,
    source_id: source,
    section_index: null,
    request_id: rid(),
  });
  await reloadWork();
  notify(`${KINDS[result.kind] || KINDS[kind]}已保存为新版本`);
}
function taskCard(task, weekly = false) {
  const n = el("div", undefined, "task" + (task.done ? " done" : ""));
  const label = el("label", task.title),
    checkbox = el("input");
  checkbox.type = "checkbox";
  checkbox.checked = task.done;
  label.prepend(checkbox);
  n.append(label);
  if (weekly) {
    const w = state.data.works.find((w) => w.id === task.work_id);
    n.append(
      el(
        "span",
        `${w?.title || ""} · ${task.due_date || "未排期"} · 预计 ${task.estimated_hours} 小时`,
        "muted",
      ),
    );
    checkbox.addEventListener("change", () =>
      run(async () => {
        try {
          await api("/tasks/" + task.id, "PATCH", { done: checkbox.checked });
          await refresh();
        } catch (e) {
          checkbox.checked = task.done;
          throw e;
        }
      }),
    );
    return n;
  }
  const row = el("div", undefined, "form-row");
  const due = field("截止日期", task.due_date, "date"),
    estimate = field("预计小时", task.estimated_hours, "number"),
    actual = field("实际小时", task.actual_hours, "number");
  for (const f of [estimate, actual]) {
    f.input.min = 0;
    f.input.step = 0.1;
  }
  row.append(due.wrap, estimate.wrap, actual.wrap);
  n.append(
    row,
    action("保存任务", async () => {
      await api("/tasks/" + task.id, "PATCH", {
        done: checkbox.checked,
        due_date: due.input.value || null,
        estimated_hours: Number(estimate.input.value),
        ...(actual.input.value === ""
          ? {}
          : { actual_hours: Number(actual.input.value) }),
      });
      await reloadWork();
      await refresh();
      notify("制作任务已保存");
    }),
  );
  return n;
}
function renderTasks() {
  const tasks = (state.work.tasks || []).filter(
    (t) => !t.variant_id || String(t.variant_id) === String(state.variantId),
  );
  $("#task-list").replaceChildren(...tasks.map((t) => taskCard(t)));
}
function resetPublication() {
  const f = $("#publication-form");
  f.reset();
  f.elements.id.value = "";
  f.elements.published_at.value = today();
  f.elements.platform.value = variant()?.platform || "小红书";
}
function renderPublications() {
  const publications = variant()?.publications || [];
  $("#publication-list").replaceChildren(
    ...publications.map((p) => {
      const n = el("article", undefined, "card");
      n.append(
        el("h3", `${p.platform} · ${p.published_at}`),
        el(
          "p",
          `观察 ${p.observation_days} 天 · 阅读 / 播放 ${p.metrics?.views ?? "未记录"} · 赞 ${p.metrics?.likes ?? "未记录"} · 收藏 ${p.metrics?.saves ?? "未记录"}`,
        ),
        el("p", p.reflection || "", "muted"),
        action("编辑发布记录", () => {
          fill($("#publication-form"), { ...p, ...p.metrics });
          $("#publication-form").scrollIntoView({ behavior: "smooth" });
        }),
      );
      return n;
    }),
  );
}
async function savePublication(f) {
  const v = requireVariant();
  const body = {};
  for (const k of [
    "platform",
    "published_at",
    "url",
    "comments_text",
    "reflection",
  ])
    body[k] = val(f, k);
  body.observation_days = number(f, "observation_days");
  body.actual_hours = number(f, "actual_hours");
  body.metrics = Object.fromEntries(
    ["views", "likes", "comments", "saves", "completion_rate"].map((k) => [
      k,
      number(f, k),
    ]),
  );
  const id = val(f, "id");
  if (!id) body.request_id = rid();
  const result = await api(
    id ? "/publications/" + id : `/variants/${v.id}/publications`,
    id ? "PUT" : "POST",
    body,
  );
  f.elements.id.value = result.id;
  await reloadWork();
  notify("发布记录已保存");
}
async function loadReviews() {
  const data = await api("/reviews");
  $("#review-list").replaceChildren(
    ...data.map((a) => {
      const card = el("article", undefined, "panel");
      card.append(
        el("h2", `${KINDS[a.kind]} · ${String(a.created_at).slice(0, 10)}`),
        el("div", artifactText(a), "prose"),
      );
      if (a.data?.missing?.length)
        card.append(el("p", "待补充：" + a.data.missing.join("；"), "muted"));
      const title = field("从这次复盘想到的待验证选题");
      card.append(
        title.wrap,
        action("采纳为待验证选题", async () => {
          if (!title.input.value.trim())
            throw Error("请为待验证选题填写标题。");
          await api(`/reviews/${a.id}/ideas`, "POST", {
            title: title.input.value,
            request_id: rid(),
          });
          notify("已回流到选题池，作为待验证选题。");
        }),
        link(
          "导出复盘 Markdown ↗",
          `/api/studio/artifacts/${a.id}/export?format=md`,
        ),
      );
      return card;
    }),
  );
  if (!data.length)
    $("#review-list").append(
      empty(
        "每次尝试，都有值得留下的经验",
        "在作品里登记发布数据，写下观察，再进行复盘。",
      ),
    );
}
$$("[data-view]").forEach((b) =>
  b.addEventListener("click", () => {
    location.hash = b.dataset.view;
  }),
);
$$("[data-go]").forEach((b) =>
  b.addEventListener("click", () => {
    location.hash = b.dataset.go;
  }),
);
window.addEventListener("hashchange", () =>
  run(() => navigate(location.hash.slice(1))),
);
$("#add-direction").addEventListener("click", () =>
  $("#weight-fields").append(weightRow()),
);
submit("#profile-form", saveProfile);
submit("#interview-form", async (f) => {
  const interview = val(f, "interview");
  if (!interview.trim()) throw Error("请先写下你的访谈信息。");
  const result = await api("/positioning", "POST", {
    interview,
    request_id: rid(),
  });
  renderCandidates([result]);
  notify("三个候选已生成，选择后还需要保存定位。");
});
submit("#material-form", saveMaterial);
$("#new-material").addEventListener("click", () => {
  $("#material-form").reset();
  $("#material-form").elements.id.value = "";
  $("#material-form-title").textContent = "记录一条素材";
});
submit("#new-work-form", async (f) => {
  await saveManualIfDirty();
  const w = await api("/works", "POST", {
    title: val(f, "title"),
    topic_id: null,
    material_ids: [],
    request_id: rid(),
  });
  await refresh();
  await openWork(w.id);
  f.reset();
  notify("作品已创建");
});
submit("#work-edit-form", async (f) => {
  await api("/works/" + state.work.id, "PUT", {
    title: val(f, "title"),
    material_ids: $$("input:checked", $("#work-materials")).map((n) => n.value),
  });
  await reloadWork();
  await refresh();
  notify("作品信息已保存");
});
submit("#variant-form", async (f) => {
  await saveManualIfDirty();
  const v = await api(`/works/${state.work.id}/variants`, "POST", {
    form: val(f, "form"),
    platform: val(f, "platform"),
    request_id: rid(),
  });
  state.variantId = v.id;
  resetManual();
  await reloadWork();
  resetPublication();
  await refresh();
  notify("内容形式已添加");
});
$("#variant-picker").addEventListener("change", () => {
  const next = $("#variant-picker").value;
  run(async () => {
    try {
      await saveManualIfDirty();
      state.variantId = next;
      renderWork();
      resetManual();
      resetPublication();
    } catch (e) {
      $("#variant-picker").value = state.variantId;
      throw e;
    }
  });
});
$("#save-variant").addEventListener("click", () =>
  run(async () => {
    const v = requireVariant();
    await api("/variants/" + v.id, "PATCH", {
      status: $("#variant-status").value,
      platform: $("#variant-platform").value,
    });
    await reloadWork();
    await refresh();
    notify("形式状态与平台已保存");
  }),
);
submit("#manual-artifact-form", saveManual);
$("#clear-editor").addEventListener("click", () =>
  run(async () => {
    await saveManualIfDirty();
    resetManual();
  }),
);
$$("[data-generate]").forEach((b) =>
  b.addEventListener("click", () => run(() => generate(b.dataset.generate))),
);
$("#generation-form").addEventListener("submit", (e) => e.preventDefault());
$("#generate-sop").addEventListener("click", () =>
  run(async () => {
    await api(`/works/${state.work.id}/sop`, "POST", {
      variant_id: requireVariant().id,
      request_id: rid(),
    });
    await reloadWork();
    await refresh();
    notify("制作清单已准备好，可逐项调整时间");
  }),
);
submit("#schedule-form", async (f) => {
  const weekly = await api("/schedule", "POST", {
    week_start: val(f, "week_start"),
  });
  state.data.weekly = weekly;
  renderHome();
  notify("已按预算排期，超出预算的任务留在尚未排期");
});
$("#load-week").addEventListener("click", () =>
  run(async () => {
    const date = val($("#schedule-form"), "week_start");
    state.data.weekly = await api(
      "/weekly?week_start=" + encodeURIComponent(date),
    );
    renderHome();
  }),
);
submit("#publication-form", savePublication);
$("#new-publication").addEventListener("click", resetPublication);
submit("#period-form", async (f) => {
  const start = val(f, "start_date"),
    end = val(f, "end_date");
  if (start > end) throw Error("开始日期不能晚于结束日期。");
  await api("/reviews/period", "POST", {
    start_date: start,
    end_date: end,
    request_id: rid(),
  });
  await loadReviews();
  notify("周期复盘已保存");
});
window.addEventListener("beforeunload", (e) => {
  if (
    state.sectionEdits.size ||
    (val($("#manual-artifact-form"), "markdown").trim() &&
      manualSignature() !== state.manualSaved)
  ) {
    e.preventDefault();
    e.returnValue = "";
  }
});
formOptions($("#new-form"), FORMS);
formOptions($("#variant-status"), STATUSES);
const monday = new Date();
monday.setDate(monday.getDate() - ((monday.getDay() + 6) % 7));
$("#schedule-form").elements.week_start.value =
  monday.toLocaleDateString("en-CA");
$("#publication-form").elements.published_at.value = today();
$("#period-form").elements.end_date.value = today();
const month = new Date();
month.setDate(1);
$("#period-form").elements.start_date.value = month.toLocaleDateString("en-CA");
run(async () => {
  await refresh();
  const remembered = sessionStorage.getItem("studio-work");
  if (remembered && state.data.works.some((w) => String(w.id) === remembered))
    await openWork(remembered);
  await navigate(location.hash.slice(1) || "home");
});
