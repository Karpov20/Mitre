const STORAGE_KEYS = {
  domain: "attack_domain",
  lang: "attack_lang",
};

const DOMAINS = [
  { id: "enterprise", label: "Enterprise" },
  { id: "mobile", label: "Mobile" },
  { id: "ics", label: "ICS" },
];

const NAVIGATOR_URL = "navigator/index.html";
const NAVIGATOR_ROUTE = "#/navigator";
const NAVIGATOR_DOMAIN = {
  enterprise: "enterprise-attack",
  mobile: "mobile-attack",
  ics: "ics-attack",
};
const NAVIGATOR_ATTACK_VERSION = "14";

const I18N = {
  ru: {
    nav: {
      matrix: "Матрица",
      techniques: "Техники",
      groups: "Группы",
      software: "ПО",
      mitigations: "Митигации",
      navigator: "Навигатор",
      about: "О проекте",
    },
    matrixTitle: "Матрица техник",
    matrixSubtitle: "Кликните по технике, чтобы открыть карточку.",
    loading: "Загрузка данных…",
    noDataTitle: "Нет данных для отображения",
    noDataBody:
      "Сначала сгенерируйте данные: `python3 scripts/fetch_attack.py --domain all`, затем запустите сервер: `python3 -m http.server 8000 -d site`.",
    searchPlaceholder: "Поиск: T1059, G0010, S0001, M1040…",
    searchTitle: "Результаты поиска",
    searchEmpty: "Ничего не найдено.",
    navigatorTitle: "ATT&CK Навигатор",
    navigatorBody: "Скачайте слой или откройте встроенный ATT&CK Навигатор.",
    navigatorDownload: "Скачать слой",
    navigatorOpen: "Открыть на сайте",
    navigatorEmpty: "Нет техник для слоя.",
    aboutTitle: "О проекте",
    aboutBody:
      "Это статический сайт, который отображает MITRE ATT&CK (Enterprise/Mobile/ICS) и поддерживает русскую локализацию. Сайт не является официальным продуктом MITRE.",
    techniqueNotFound: "Техника не найдена.",
    backToMatrix: "← К матрице",
    techniquesTitle: "Техники",
    groupsTitle: "Группы",
    softwareTitle: "ПО",
    mitigationsTitle: "Митигации",
    groupNotFound: "Группа не найдена.",
    softwareNotFound: "ПО не найдено.",
    mitigationNotFound: "Митигация не найдена.",
    backToTechniques: "← К техникам",
    backToGroups: "← К группам",
    backToSoftware: "← К ПО",
    backToMitigations: "← К митигациям",
    descriptionTitle: "Описание",
    relatedTitle: "Связи",
    fields: {
      tactics: "Тактики",
      platforms: "Платформы",
      detection: "Детектирование",
      subtechniques: "Подтехники",
      source: "Источник",
      aliases: "Алиасы",
      type: "Тип",
      usesTechniques: "Использует техники",
      usesSoftware: "Использует ПО",
      usedByGroups: "Используется группами",
      mitigatesTechniques: "Митигирует техники",
      relatedGroups: "Связанные группы",
      relatedSoftware: "Связанное ПО",
      relatedMitigations: "Меры защиты",
    },
  },
  en: {
    nav: {
      matrix: "Matrix",
      techniques: "Techniques",
      groups: "Groups",
      software: "Software",
      mitigations: "Mitigations",
      navigator: "Navigator",
      about: "About",
    },
    matrixTitle: "Techniques matrix",
    matrixSubtitle: "Click a technique to open details.",
    loading: "Loading data…",
    noDataTitle: "No data to display",
    noDataBody:
      "Generate data first: `python3 scripts/fetch_attack.py --domain all`, then serve: `python3 -m http.server 8000 -d site`.",
    searchPlaceholder: "Search: T1059, G0010, S0001, M1040…",
    searchTitle: "Search results",
    searchEmpty: "No results.",
    navigatorTitle: "ATT&CK Navigator",
    navigatorBody: "Download the layer or open the built-in ATT&CK Navigator.",
    navigatorDownload: "Download layer",
    navigatorOpen: "Open here",
    navigatorEmpty: "No techniques for the layer.",
    aboutTitle: "About",
    aboutBody:
      "A static site that renders MITRE ATT&CK (Enterprise/Mobile/ICS) and supports Russian localization. Not affiliated with MITRE.",
    techniqueNotFound: "Technique not found.",
    backToMatrix: "← Back to matrix",
    techniquesTitle: "Techniques",
    groupsTitle: "Groups",
    softwareTitle: "Software",
    mitigationsTitle: "Mitigations",
    groupNotFound: "Group not found.",
    softwareNotFound: "Software not found.",
    mitigationNotFound: "Mitigation not found.",
    backToTechniques: "← Back to techniques",
    backToGroups: "← Back to groups",
    backToSoftware: "← Back to software",
    backToMitigations: "← Back to mitigations",
    descriptionTitle: "Description",
    relatedTitle: "Relationships",
    fields: {
      tactics: "Tactics",
      platforms: "Platforms",
      detection: "Detection",
      subtechniques: "Sub-techniques",
      source: "Source",
      aliases: "Aliases",
      type: "Type",
      usesTechniques: "Uses techniques",
      usesSoftware: "Uses software",
      usedByGroups: "Used by groups",
      mitigatesTechniques: "Mitigates techniques",
      relatedGroups: "Related groups",
      relatedSoftware: "Related software",
      relatedMitigations: "Mitigations",
    },
  },
};

const dom = {
  navMatrix: document.getElementById("navMatrix"),
  navTechniques: document.getElementById("navTechniques"),
  navGroups: document.getElementById("navGroups"),
  navSoftware: document.getElementById("navSoftware"),
  navMitigations: document.getElementById("navMitigations"),
  navNavigator: document.getElementById("navNavigator"),
  navAbout: document.getElementById("navAbout"),
  domainSelect: document.getElementById("domainSelect"),
  langToggle: document.getElementById("langToggle"),
  searchForm: document.getElementById("searchForm"),
  searchInput: document.getElementById("searchInput"),
  main: document.getElementById("main"),
};

function loadPref(key, fallback) {
  try {
    const v = localStorage.getItem(key);
    return v ?? fallback;
  } catch {
    return fallback;
  }
}

function savePref(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch {
    // ignore
  }
}

const state = {
  domain: loadPref(STORAGE_KEYS.domain, "enterprise"),
  lang: loadPref(STORAGE_KEYS.lang, "ru"),
};

const cache = new Map(); // domain -> { base, patchRu, tacticsById, techniquesById, groupsById, softwareById, mitigationsById }

function t(key) {
  return (I18N[state.lang] || I18N.ru)[key] ?? I18N.ru[key];
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function paragraphize(text) {
  const safe = escapeHtml(text || "");
  return safe.replaceAll("\n", "<br />");
}

function setMain(node) {
  dom.main.replaceChildren(node);
}

function card({ title, subtitle, right, bodyHtml }) {
  const wrap = document.createElement("section");
  wrap.className = "card";
  const header = document.createElement("div");
  header.className = "card__header";
  const left = document.createElement("div");
  left.style.display = "grid";
  left.style.gap = "2px";
  const h = document.createElement("div");
  h.className = "card__title";
  h.textContent = title;
  left.appendChild(h);
  if (subtitle) {
    const s = document.createElement("div");
    s.className = "muted";
    s.style.fontSize = "12px";
    s.textContent = subtitle;
    left.appendChild(s);
  }
  header.appendChild(left);
  if (right) header.appendChild(right);
  const body = document.createElement("div");
  body.className = "card__body";
  body.innerHTML = bodyHtml;
  wrap.appendChild(header);
  wrap.appendChild(body);
  return wrap;
}

function pill(text, title) {
  const el = document.createElement("span");
  el.className = "pill";
  el.textContent = text;
  if (title) el.title = title;
  return el;
}

function link(href, text) {
  const a = document.createElement("a");
  a.href = href;
  a.className = "link";
  a.textContent = text;
  return a;
}

function totalSubtitle(count) {
  return state.lang === "ru" ? `Всего: ${count}` : `Total: ${count}`;
}

function typeLabel(type) {
  const ru = { technique: "Техника", group: "Группа", software: "ПО", mitigation: "Митигация" };
  const en = { technique: "Technique", group: "Group", software: "Software", mitigation: "Mitigation" };
  return (state.lang === "ru" ? ru : en)[type] || type;
}

function softwareTypeLabel(type) {
  if (state.lang === "ru") {
    if (type === "tool") return "инструмент";
    if (type === "malware") return "вредоносное ПО";
    return type || "—";
  }
  if (type === "tool") return "tool";
  if (type === "malware") return "malware";
  return type || "—";
}

function entityItemHtml({ href, id, name, meta }) {
  const metaPart = meta ? ` • ${escapeHtml(meta)}` : "";
  return `<a class="techitem" href="${escapeHtml(href)}">
      <div class="techitem__id">${escapeHtml(id)}${metaPart}</div>
      <div class="techitem__name">${escapeHtml(name)}</div>
    </a>`;
}

function gridHtml(itemsHtml, { limit, total }) {
  if (!itemsHtml.length) return `<div class="muted">—</div>`;
  const shown = limit ? Math.min(itemsHtml.length, limit) : itemsHtml.length;
  const list = limit ? itemsHtml.slice(0, limit) : itemsHtml;
  const more =
    typeof total === "number" && typeof limit === "number" && total > limit
      ? `<div class="muted" style="font-size:12px;margin-top:8px">${escapeHtml(
          state.lang === "ru" ? `Показаны первые ${shown} из ${total}.` : `Showing first ${shown} of ${total}.`
        )}</div>`
      : "";
  return `<div class="grid">${list.join("")}</div>${more}`;
}

function uniqueSortedIds(ids) {
  return [...new Set((ids || []).filter(Boolean))].sort();
}

function buildNavigatorLayer({ name, description, domain, techniqueIds }) {
  const techniques = uniqueSortedIds(techniqueIds).map((id) => ({ techniqueID: id, score: 1 }));
  const layer = {
    versions: { attack: NAVIGATOR_ATTACK_VERSION, navigator: "5.2.0", layer: "4.5" },
    name,
    domain: NAVIGATOR_DOMAIN[domain] || NAVIGATOR_DOMAIN.enterprise,
    description,
    techniques,
    sorting: 0,
    layout: { layout: "side", aggregateFunction: "average", showID: true, showName: true },
    hideDisabled: false,
  };
  if (!techniques.length) delete layer.techniques;
  return layer;
}

function navigatorBlockHtml({ title, description, domain, techniqueIds }) {
  const s = I18N[state.lang] || I18N.ru;
  const navBase = new URL(NAVIGATOR_URL, window.location.href);
  const layerAbsUrl = new URL(`layers/${domain}.json`, navBase).href;
  const ids = uniqueSortedIds(techniqueIds);
  if (!ids.length) {
    return `<div class="navigator">
      <div class="navigator__title">${escapeHtml(s.navigatorTitle)}</div>
      <div class="muted">${escapeHtml(s.navigatorEmpty)}</div>
    </div>`;
  }

  const layer = buildNavigatorLayer({
    name: title,
    description,
    domain,
    techniqueIds: ids,
  });
  const json = JSON.stringify(layer, null, 2);
  const dataUrl = `data:application/json;charset=utf-8,${encodeURIComponent(json)}`;
  const fileName = `attack-layer-${domain}.json`;
  const openHref = `${NAVIGATOR_ROUTE}?layer=${encodeURIComponent(layerAbsUrl)}`;

  return `<div class="navigator">
    <div class="navigator__title">${escapeHtml(s.navigatorTitle)}</div>
    <div class="muted">${escapeHtml(s.navigatorBody)}</div>
    <div class="navigator__actions">
      <a class="btn" href="${dataUrl}" download="${escapeHtml(fileName)}">${escapeHtml(s.navigatorDownload)}</a>
      <a class="link" href="${openHref}">${escapeHtml(s.navigatorOpen)}</a>
    </div>
  </div>`;
}

async function fetchJson(path) {
  const res = await fetch(path, { cache: "no-cache" });
  if (!res.ok) {
    const err = new Error(`HTTP ${res.status} for ${path}`);
    err.status = res.status;
    throw err;
  }
  return res.json();
}

async function loadDomain(domain) {
  let entry = cache.get(domain);
  if (!entry) {
    const basePath = `data/${domain}.json`;
    const base = await fetchJson(basePath);
    const tacticsById = new Map();
    for (const tactic of base.tactics || []) tacticsById.set(tactic.id, tactic);
    const techniquesById = new Map();
    for (const tech of base.techniques || []) techniquesById.set(tech.id, tech);
    const groupsById = new Map();
    for (const group of base.groups || []) groupsById.set(group.id, group);
    const softwareById = new Map();
    for (const sw of base.software || []) softwareById.set(sw.id, sw);
    const mitigationsById = new Map();
    for (const m of base.mitigations || []) mitigationsById.set(m.id, m);
    entry = { base, patchRu: undefined, tacticsById, techniquesById, groupsById, softwareById, mitigationsById };
    cache.set(domain, entry);
  }

  if (state.lang === "ru" && entry.patchRu === undefined) {
    try {
      entry.patchRu = await fetchJson(`data/${domain}.ru.json`);
    } catch (e) {
      entry.patchRu = null; // no patch file yet
    }
  }

  return entry;
}

function localizedField(patchSection, id, field, fallback) {
  if (state.lang !== "ru") return fallback;
  if (!patchSection) return fallback;
  const obj = patchSection[id];
  if (!obj) return fallback;
  const v = obj[field];
  if (typeof v !== "string") return fallback;
  return v;
}

function groupName(vm, groupId) {
  const g = vm.groupsById.get(groupId);
  return g ? localizedField(vm.patchRu?.groups, groupId, "name", g.name) : groupId;
}

function softwareName(vm, softwareId) {
  const sw = vm.softwareById.get(softwareId);
  return sw ? localizedField(vm.patchRu?.software, softwareId, "name", sw.name) : softwareId;
}

function mitigationName(vm, mitigationId) {
  const m = vm.mitigationsById.get(mitigationId);
  return m ? localizedField(vm.patchRu?.mitigations, mitigationId, "name", m.name) : mitigationId;
}

function parseHash() {
  const raw = (location.hash || "#/").slice(1);
  const [pathPart, queryPart] = raw.split("?");
  const path = pathPart || "/";
  const parts = path.split("/").filter(Boolean);
  const params = new URLSearchParams(queryPart || "");
  return { path: "/" + parts.join("/"), parts, params };
}

function syncUiStrings() {
  const s = I18N[state.lang] || I18N.ru;
  if (dom.navMatrix) dom.navMatrix.textContent = s.nav.matrix;
  if (dom.navTechniques) dom.navTechniques.textContent = s.nav.techniques;
  if (dom.navGroups) dom.navGroups.textContent = s.nav.groups;
  if (dom.navSoftware) dom.navSoftware.textContent = s.nav.software;
  if (dom.navMitigations) dom.navMitigations.textContent = s.nav.mitigations;
  if (dom.navNavigator) dom.navNavigator.textContent = s.nav.navigator;
  if (dom.navAbout) dom.navAbout.textContent = s.nav.about;
  if (dom.searchInput) dom.searchInput.placeholder = s.searchPlaceholder;
}

function renderLoading() {
  setMain(
    card({
      title: t("loading"),
      subtitle: DOMAINS.find((d) => d.id === state.domain)?.label || state.domain,
      bodyHtml: `<div class="muted">${escapeHtml(t("loading"))}</div>`,
    })
  );
}

function renderNoData(err) {
  const details = err ? `<pre class="card mono">${escapeHtml(String(err))}</pre>` : "";
  setMain(
    card({
      title: t("noDataTitle"),
      subtitle: DOMAINS.find((d) => d.id === state.domain)?.label || state.domain,
      bodyHtml: `<div class="muted">${escapeHtml(t("noDataBody"))}</div>${details}`,
    })
  );
}

function renderAbout() {
  const s = I18N[state.lang] || I18N.ru;
  const detailsRu = `
    <div class="section">
      <div class="section__title">Данные</div>
      <div class="muted">Источник STIX JSON: репозиторий MITRE CTI (github.com/mitre/cti). Генерация: <span class="mono">python3 scripts/fetch_attack.py --domain all</span>.</div>
    </div>
    <div class="section">
      <div class="section__title">Перевод</div>
      <div class="muted">Русские строки — машинный перевод (Google Translate). Генерация: <span class="mono">python3 scripts/translate_attack_ru.py --domain all</span>.</div>
    </div>
  `;
  const detailsEn = `
    <div class="section">
      <div class="section__title">Data</div>
      <div class="muted">STIX JSON source: MITRE CTI repository (github.com/mitre/cti). Generate: <span class="mono">python3 scripts/fetch_attack.py --domain all</span>.</div>
    </div>
    <div class="section">
      <div class="section__title">Translation</div>
      <div class="muted">Russian strings are machine-translated (Google Translate). Generate: <span class="mono">python3 scripts/translate_attack_ru.py --domain all</span>.</div>
    </div>
  `;
  setMain(
    card({
      title: s.aboutTitle,
      subtitle: "MITRE ATT&CK • Enterprise / Mobile / ICS",
      bodyHtml: `<div class="muted">${escapeHtml(s.aboutBody)}</div>
      <div class="section">
        <div class="section__title">MITRE ATT&CK</div>
        <div class="muted">ATT&CK® content is provided under CC BY 4.0. Source: https://attack.mitre.org/</div>
      </div>
      ${state.lang === "ru" ? detailsRu : detailsEn}
      `,
    })
  );
}

function renderMatrix(vm) {
  const s = I18N[state.lang] || I18N.ru;

  const right = document.createElement("div");
  right.style.display = "flex";
  right.style.gap = "8px";
  right.style.alignItems = "center";
  right.appendChild(pill(state.lang === "ru" ? "RU" : "EN", "Язык интерфейса"));
  right.appendChild(pill(vm.base.meta?.domain || state.domain, "Домен"));

  const container = document.createElement("div");
  container.className = "grid";

  const matrixNavigatorHtml = navigatorBlockHtml({
    title: `${s.matrixTitle} (${state.domain})`,
    description: s.matrixTitle,
    domain: state.domain,
    techniqueIds: (vm.base.techniques || []).map((t) => t.id),
  });

  container.appendChild(
    card({
      title: s.matrixTitle,
      subtitle: s.matrixSubtitle,
      right,
      bodyHtml: `<div class="muted">Данные: <a class="link" href="${escapeHtml(
        vm.base.meta?.source_url || "#"
      )}" target="_blank" rel="noreferrer">${escapeHtml(vm.base.meta?.source_url || "")}</a></div>
      <div class="section">${matrixNavigatorHtml}</div>`,
    })
  );

  const matrixWrap = document.createElement("div");
  matrixWrap.className = "matrix";

  const tacticsSorted = [...(vm.base.tactics || [])].sort((a, b) => (a.order ?? 0) - (b.order ?? 0));
  for (const tactic of tacticsSorted) {
    const col = document.createElement("section");
    col.className = "card matrix__col";

    const header = document.createElement("div");
    header.className = "card__header";
    const left = document.createElement("div");
    left.style.display = "grid";
    left.style.gap = "2px";

    const tacticName = localizedField(vm.patchRu?.tactics, tactic.id, "name", tactic.name);
    const tacticDesc = localizedField(vm.patchRu?.tactics, tactic.id, "description", tactic.description);

    const nameEl = document.createElement("div");
    nameEl.className = "tactic__name";
    nameEl.textContent = tacticName;
    const metaEl = document.createElement("div");
    metaEl.className = "tactic__meta";
    metaEl.textContent = tactic.id;

    left.appendChild(nameEl);
    left.appendChild(metaEl);
    header.appendChild(left);

    if (tactic.url) {
      const a = document.createElement("a");
      a.className = "link";
      a.href = tactic.url;
      a.target = "_blank";
      a.rel = "noreferrer";
      a.textContent = "MITRE";
      header.appendChild(a);
    }

    col.appendChild(header);

    const list = document.createElement("ol");
    list.className = "techlist";
    const techIds = (vm.base.matrix || {})[tactic.id] || [];
    const subMap = vm.base.subtechniques || {};

    const addItem = (techId, isSub = false) => {
      const tech = vm.techniquesById.get(techId);
      if (!tech) return;
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.className = isSub ? "techitem techitem--sub" : "techitem";
      a.href = `#/technique/${encodeURIComponent(techId)}`;

      const idEl = document.createElement("div");
      idEl.className = "techitem__id";
      idEl.textContent = techId;
      const name = localizedField(vm.patchRu?.techniques, techId, "name", tech.name);
      const nameEl2 = document.createElement("div");
      nameEl2.className = "techitem__name";
      nameEl2.textContent = name;

      a.appendChild(idEl);
      a.appendChild(nameEl2);
      li.appendChild(a);
      list.appendChild(li);
    };

    for (const tid of techIds) {
      addItem(tid, false);
      const subIds = subMap[tid] || [];
      for (const sid of subIds) addItem(sid, true);
    }

    col.appendChild(list);
    if (tacticDesc) {
      const hint = document.createElement("div");
      hint.className = "card__body";
      hint.innerHTML = `<div class="muted" style="font-size:12px">${paragraphize(tacticDesc)}</div>`;
      col.appendChild(hint);
    }

    matrixWrap.appendChild(col);
  }

  container.appendChild(matrixWrap);
  setMain(container);
}

function renderTechnique(vm, techniqueId) {
  const tech = vm.techniquesById.get(techniqueId);
  if (!tech) {
    setMain(
      card({
        title: t("techniqueNotFound"),
        subtitle: techniqueId,
        bodyHtml: "",
      })
    );
    return;
  }

  const name = localizedField(vm.patchRu?.techniques, techniqueId, "name", tech.name);
  const desc = localizedField(vm.patchRu?.techniques, techniqueId, "description", tech.description);
  const det = localizedField(vm.patchRu?.techniques, techniqueId, "detection", tech.detection);

  const headerRight = document.createElement("div");
  headerRight.style.display = "flex";
  headerRight.style.gap = "8px";
  headerRight.style.alignItems = "center";
  headerRight.appendChild(link("#/", t("backToMatrix")));
  headerRight.appendChild(pill(techniqueId));

  const tactics = (tech.tactics || []).map((tid) => {
    const tactic = vm.tacticsById.get(tid);
    if (!tactic) return pill(tid);
    const tacticName = localizedField(vm.patchRu?.tactics, tid, "name", tactic.name);
    return pill(tacticName, tid);
  });

  const subIds = (vm.base.subtechniques || {})[techniqueId] || [];
  const subListHtml =
    subIds.length === 0
      ? `<div class="muted">—</div>`
      : `<div class="grid">${subIds
          .map((sid) => {
            const sub = vm.techniquesById.get(sid);
            const subName = sub ? localizedField(vm.patchRu?.techniques, sid, "name", sub.name) : sid;
            return `<a class="techitem" href="#/technique/${encodeURIComponent(sid)}">
                <div class="techitem__id">${escapeHtml(sid)}</div>
                <div class="techitem__name">${escapeHtml(subName)}</div>
              </a>`;
          })
          .join("")}</div>`;

  const platforms = (tech.platforms || []).length
    ? tech.platforms.map((p) => `<span class="pill">${escapeHtml(p)}</span>`).join(" ")
    : `<div class="muted">—</div>`;

  const source = tech.url
    ? `<a class="link" href="${escapeHtml(tech.url)}" target="_blank" rel="noreferrer">${escapeHtml(
        tech.url
      )}</a>`
    : `<div class="muted">—</div>`;

  const links = vm.base.links || {};
  const groupIds = links.technique_groups?.[techniqueId] || [];
  const softwareIds = links.technique_software?.[techniqueId] || [];
  const mitigationIds = links.technique_mitigations?.[techniqueId] || [];

  const groupsHtml = gridHtml(
    groupIds.map((gid) => entityItemHtml({ href: `#/group/${encodeURIComponent(gid)}`, id: gid, name: groupName(vm, gid) })),
    { limit: 200, total: groupIds.length }
  );
  const softwareHtml = gridHtml(
    softwareIds.map((sid) => {
      const sw = vm.softwareById.get(sid);
      return entityItemHtml({
        href: `#/software/${encodeURIComponent(sid)}`,
        id: sid,
        name: softwareName(vm, sid),
        meta: sw ? softwareTypeLabel(sw.type) : undefined,
      });
    }),
    { limit: 200, total: softwareIds.length }
  );
  const mitigationsHtml = gridHtml(
    mitigationIds.map((mid) =>
      entityItemHtml({ href: `#/mitigation/${encodeURIComponent(mid)}`, id: mid, name: mitigationName(vm, mid) })
    ),
    { limit: 200, total: mitigationIds.length }
  );

  const navigatorHtml = navigatorBlockHtml({
    title: `${techniqueId} ${name}`,
    description: name,
    domain: state.domain,
    techniqueIds: [techniqueId],
  });

  const subInfo =
    tech.is_subtechnique && tech.parent_id
      ? state.lang === "ru"
        ? ` • под-техника ${tech.parent_id}`
        : ` • sub of ${tech.parent_id}`
      : "";

  setMain(
    card({
      title: name,
      subtitle: `${techniqueId}${subInfo}`,
      right: headerRight,
      bodyHtml: `
        <div class="section">
          <div class="section__title">${escapeHtml(t("descriptionTitle"))}</div>
          <div class="muted">${paragraphize(desc)}</div>
        </div>

        <div class="section kv">
          <div class="muted">${escapeHtml(t("fields").tactics)}</div>
          <div>${tactics.map((x) => x.outerHTML).join(" ") || `<div class="muted">—</div>`}</div>

          <div class="muted">${escapeHtml(t("fields").platforms)}</div>
          <div>${platforms}</div>

          <div class="muted">${escapeHtml(t("fields").source)}</div>
          <div>${source}</div>
        </div>

        <div class="section">
          <div class="section__title">${escapeHtml(t("fields").detection)}</div>
          <div class="muted">${det ? paragraphize(det) : "—"}</div>
        </div>

        <div class="section">
          <div class="section__title">${escapeHtml(t("fields").subtechniques)}</div>
          ${subListHtml}
        </div>

        <div class="section">
          <div class="section__title">${escapeHtml(t("relatedTitle"))}</div>
          <div class="section">
            <div class="section__title">${escapeHtml(t("fields").relatedGroups)}</div>
            ${groupsHtml}
          </div>
          <div class="section">
            <div class="section__title">${escapeHtml(t("fields").relatedSoftware)}</div>
            ${softwareHtml}
          </div>
          <div class="section">
            <div class="section__title">${escapeHtml(t("fields").relatedMitigations)}</div>
            ${mitigationsHtml}
          </div>
        </div>

        <div class="section">
          ${navigatorHtml}
        </div>
      `,
    })
  );
}

function renderTechniquesList(vm) {
  const s = I18N[state.lang] || I18N.ru;
  const items = (vm.base.techniques || []).map((tech) => {
    const name = localizedField(vm.patchRu?.techniques, tech.id, "name", tech.name);
    const meta =
      tech.is_subtechnique && tech.parent_id
        ? state.lang === "ru"
          ? `под ${tech.parent_id}`
          : `sub of ${tech.parent_id}`
        : undefined;
    return entityItemHtml({ href: `#/technique/${encodeURIComponent(tech.id)}`, id: tech.id, name, meta });
  });

  setMain(
    card({
      title: s.techniquesTitle,
      subtitle: totalSubtitle(items.length),
      bodyHtml: gridHtml(items, {}),
    })
  );
}

function renderGroupsList(vm) {
  const s = I18N[state.lang] || I18N.ru;
  const items = (vm.base.groups || []).map((g) => {
    const name = localizedField(vm.patchRu?.groups, g.id, "name", g.name);
    return entityItemHtml({ href: `#/group/${encodeURIComponent(g.id)}`, id: g.id, name });
  });
  setMain(
    card({
      title: s.groupsTitle,
      subtitle: totalSubtitle(items.length),
      bodyHtml: gridHtml(items, {}),
    })
  );
}

function renderSoftwareList(vm) {
  const s = I18N[state.lang] || I18N.ru;
  const items = (vm.base.software || []).map((sw) => {
    const name = localizedField(vm.patchRu?.software, sw.id, "name", sw.name);
    const platforms = sw.platforms || [];
    const platformMeta =
      platforms.length > 0
        ? platforms.length <= 3
          ? platforms.join(", ")
          : `${platforms.slice(0, 3).join(", ")} +${platforms.length - 3}`
        : "";
    const meta = [softwareTypeLabel(sw.type), platformMeta].filter(Boolean).join(", ");
    return entityItemHtml({ href: `#/software/${encodeURIComponent(sw.id)}`, id: sw.id, name, meta });
  });

  setMain(
    card({
      title: s.softwareTitle,
      subtitle: totalSubtitle(items.length),
      bodyHtml: gridHtml(items, {}),
    })
  );
}

function renderMitigationsList(vm) {
  const s = I18N[state.lang] || I18N.ru;
  const items = (vm.base.mitigations || []).map((m) => {
    const name = localizedField(vm.patchRu?.mitigations, m.id, "name", m.name);
    return entityItemHtml({ href: `#/mitigation/${encodeURIComponent(m.id)}`, id: m.id, name });
  });

  setMain(
    card({
      title: s.mitigationsTitle,
      subtitle: totalSubtitle(items.length),
      bodyHtml: gridHtml(items, {}),
    })
  );
}

function renderGroup(vm, groupId) {
  const s = I18N[state.lang] || I18N.ru;
  const g = vm.groupsById.get(groupId);
  if (!g) {
    setMain(card({ title: s.groupNotFound, subtitle: groupId, bodyHtml: "" }));
    return;
  }

  const name = localizedField(vm.patchRu?.groups, groupId, "name", g.name);
  const desc = localizedField(vm.patchRu?.groups, groupId, "description", g.description);

  const headerRight = document.createElement("div");
  headerRight.style.display = "flex";
  headerRight.style.gap = "8px";
  headerRight.style.alignItems = "center";
  headerRight.appendChild(link("#/groups", s.backToGroups));
  headerRight.appendChild(pill(groupId));

  const aliases = (g.aliases || []).filter((a) => a && a !== g.name);
  const aliasesHtml = aliases.length
    ? aliases.map((a) => `<span class="pill">${escapeHtml(a)}</span>`).join(" ")
    : `<div class="muted">—</div>`;

  const source = g.url
    ? `<a class="link" href="${escapeHtml(g.url)}" target="_blank" rel="noreferrer">${escapeHtml(g.url)}</a>`
    : `<div class="muted">—</div>`;

  const links = vm.base.links || {};
  const techniqueIds = links.group_techniques?.[groupId] || [];
  const softwareIds = links.group_software?.[groupId] || [];

  const techniquesHtml = gridHtml(
    techniqueIds.map((tid) => {
      const tech = vm.techniquesById.get(tid);
      const tName = tech ? localizedField(vm.patchRu?.techniques, tid, "name", tech.name) : tid;
      return entityItemHtml({ href: `#/technique/${encodeURIComponent(tid)}`, id: tid, name: tName });
    }),
    { limit: 200, total: techniqueIds.length }
  );

  const softwareHtml = gridHtml(
    softwareIds.map((sid) => {
      const sw = vm.softwareById.get(sid);
      return entityItemHtml({
        href: `#/software/${encodeURIComponent(sid)}`,
        id: sid,
        name: softwareName(vm, sid),
        meta: sw ? softwareTypeLabel(sw.type) : undefined,
      });
    }),
    { limit: 200, total: softwareIds.length }
  );

  const navigatorHtml = navigatorBlockHtml({
    title: `${groupId} ${name}`,
    description: name,
    domain: state.domain,
    techniqueIds,
  });

  setMain(
    card({
      title: name,
      subtitle: groupId,
      right: headerRight,
      bodyHtml: `
        <div class="section">
          <div class="section__title">${escapeHtml(t("descriptionTitle"))}</div>
          <div class="muted">${paragraphize(desc)}</div>
        </div>

        <div class="section kv">
          <div class="muted">${escapeHtml(t("fields").aliases)}</div>
          <div>${aliasesHtml}</div>

          <div class="muted">${escapeHtml(t("fields").source)}</div>
          <div>${source}</div>
        </div>

        <div class="section">
          <div class="section__title">${escapeHtml(t("fields").usesTechniques)}</div>
          ${techniquesHtml}
        </div>

        <div class="section">
          <div class="section__title">${escapeHtml(t("fields").usesSoftware)}</div>
          ${softwareHtml}
        </div>

        <div class="section">
          ${navigatorHtml}
        </div>
      `,
    })
  );
}

function renderSoftware(vm, softwareId) {
  const s = I18N[state.lang] || I18N.ru;
  const sw = vm.softwareById.get(softwareId);
  if (!sw) {
    setMain(card({ title: s.softwareNotFound, subtitle: softwareId, bodyHtml: "" }));
    return;
  }

  const name = localizedField(vm.patchRu?.software, softwareId, "name", sw.name);
  const desc = localizedField(vm.patchRu?.software, softwareId, "description", sw.description);

  const headerRight = document.createElement("div");
  headerRight.style.display = "flex";
  headerRight.style.gap = "8px";
  headerRight.style.alignItems = "center";
  headerRight.appendChild(link("#/software", s.backToSoftware));
  headerRight.appendChild(pill(softwareId));

  const aliases = (sw.aliases || []).filter((a) => a && a !== sw.name);
  const aliasesHtml = aliases.length
    ? aliases.map((a) => `<span class="pill">${escapeHtml(a)}</span>`).join(" ")
    : `<div class="muted">—</div>`;

  const platforms = (sw.platforms || []).length
    ? (sw.platforms || []).map((p) => `<span class="pill">${escapeHtml(p)}</span>`).join(" ")
    : `<div class="muted">—</div>`;

  const source = sw.url
    ? `<a class="link" href="${escapeHtml(sw.url)}" target="_blank" rel="noreferrer">${escapeHtml(sw.url)}</a>`
    : `<div class="muted">—</div>`;

  const links = vm.base.links || {};
  const techniqueIds = links.software_techniques?.[softwareId] || [];
  const groupIds = links.software_groups?.[softwareId] || [];

  const techniquesHtml = gridHtml(
    techniqueIds.map((tid) => {
      const tech = vm.techniquesById.get(tid);
      const tName = tech ? localizedField(vm.patchRu?.techniques, tid, "name", tech.name) : tid;
      return entityItemHtml({ href: `#/technique/${encodeURIComponent(tid)}`, id: tid, name: tName });
    }),
    { limit: 200, total: techniqueIds.length }
  );

  const groupsHtml = gridHtml(
    groupIds.map((gid) => entityItemHtml({ href: `#/group/${encodeURIComponent(gid)}`, id: gid, name: groupName(vm, gid) })),
    { limit: 200, total: groupIds.length }
  );

  const navigatorHtml = navigatorBlockHtml({
    title: `${softwareId} ${name}`,
    description: name,
    domain: state.domain,
    techniqueIds,
  });

  setMain(
    card({
      title: name,
      subtitle: softwareId,
      right: headerRight,
      bodyHtml: `
        <div class="section">
          <div class="section__title">${escapeHtml(t("descriptionTitle"))}</div>
          <div class="muted">${paragraphize(desc)}</div>
        </div>

        <div class="section kv">
          <div class="muted">${escapeHtml(t("fields").type)}</div>
          <div><span class="pill">${escapeHtml(softwareTypeLabel(sw.type))}</span></div>

          <div class="muted">${escapeHtml(t("fields").platforms)}</div>
          <div>${platforms}</div>

          <div class="muted">${escapeHtml(t("fields").aliases)}</div>
          <div>${aliasesHtml}</div>

          <div class="muted">${escapeHtml(t("fields").source)}</div>
          <div>${source}</div>
        </div>

        <div class="section">
          <div class="section__title">${escapeHtml(t("fields").usesTechniques)}</div>
          ${techniquesHtml}
        </div>

        <div class="section">
          <div class="section__title">${escapeHtml(t("fields").usedByGroups)}</div>
          ${groupsHtml}
        </div>

        <div class="section">
          ${navigatorHtml}
        </div>
      `,
    })
  );
}

function renderMitigation(vm, mitigationId) {
  const s = I18N[state.lang] || I18N.ru;
  const m = vm.mitigationsById.get(mitigationId);
  if (!m) {
    setMain(card({ title: s.mitigationNotFound, subtitle: mitigationId, bodyHtml: "" }));
    return;
  }

  const name = localizedField(vm.patchRu?.mitigations, mitigationId, "name", m.name);
  const desc = localizedField(vm.patchRu?.mitigations, mitigationId, "description", m.description);

  const headerRight = document.createElement("div");
  headerRight.style.display = "flex";
  headerRight.style.gap = "8px";
  headerRight.style.alignItems = "center";
  headerRight.appendChild(link("#/mitigations", s.backToMitigations));
  headerRight.appendChild(pill(mitigationId));

  const source = m.url
    ? `<a class="link" href="${escapeHtml(m.url)}" target="_blank" rel="noreferrer">${escapeHtml(m.url)}</a>`
    : `<div class="muted">—</div>`;

  const links = vm.base.links || {};
  const techniqueIds = links.mitigation_techniques?.[mitigationId] || [];

  const techniquesHtml = gridHtml(
    techniqueIds.map((tid) => {
      const tech = vm.techniquesById.get(tid);
      const tName = tech ? localizedField(vm.patchRu?.techniques, tid, "name", tech.name) : tid;
      return entityItemHtml({ href: `#/technique/${encodeURIComponent(tid)}`, id: tid, name: tName });
    }),
    { limit: 200, total: techniqueIds.length }
  );

  const navigatorHtml = navigatorBlockHtml({
    title: `${mitigationId} ${name}`,
    description: name,
    domain: state.domain,
    techniqueIds,
  });

  setMain(
    card({
      title: name,
      subtitle: mitigationId,
      right: headerRight,
      bodyHtml: `
        <div class="section">
          <div class="section__title">${escapeHtml(t("descriptionTitle"))}</div>
          <div class="muted">${paragraphize(desc)}</div>
        </div>

        <div class="section kv">
          <div class="muted">${escapeHtml(t("fields").source)}</div>
          <div>${source}</div>
        </div>

        <div class="section">
          <div class="section__title">${escapeHtml(t("fields").mitigatesTechniques)}</div>
          ${techniquesHtml}
        </div>

        <div class="section">
          ${navigatorHtml}
        </div>
      `,
    })
  );
}

function renderNavigator(vm) {
  const s = I18N[state.lang] || I18N.ru;
  const route = parseHash();
  const navBase = new URL(NAVIGATOR_URL, window.location.href);
  const layerAbsUrlDefault = new URL(`layers/${state.domain}.json`, navBase).href;
  const layerParam = route.params.get("layer");
  let layerUrl = null;
  if (layerParam) {
    try {
      layerUrl = decodeURIComponent(layerParam);
    } catch (_) {
      layerUrl = layerParam;
    }
  }
  if (!layerUrl && route.params.get("autolayer") === "1") {
    layerUrl = layerAbsUrlDefault;
  }
  const clearParam = layerUrl ? "" : `&clear=${Date.now()}`;
  const baseUrl = `${NAVIGATOR_URL}?domain=${encodeURIComponent(state.domain)}&lang=${encodeURIComponent(
    state.lang
  )}${clearParam}`;
  const navUrl = layerUrl ? `${baseUrl}#layerURL=${encodeURIComponent(layerUrl)}` : baseUrl;
  const wrap = document.createElement("section");
  wrap.className = "navigator-page";
  wrap.innerHTML = `
    <div class="navigator-hero">
      <div class="navigator-hero__title">${escapeHtml(s.navigatorTitle)}</div>
      <div class="navigator-hero__subtitle muted">${escapeHtml(s.navigatorBody)}</div>
    </div>
    <div class="navigator-embed">
      <iframe class="navigator-frame" src="${navUrl}" title="${escapeHtml(s.navigatorTitle)}"></iframe>
    </div>
  `;
  setMain(wrap);
}

function renderSearch(vm, query) {
  const s = I18N[state.lang] || I18N.ru;
  const q = (query || "").trim().toLowerCase();
  if (!q) {
    location.hash = "#/";
    return;
  }

  const results = [];

  for (const tech of vm.base.techniques || []) {
    const name = localizedField(vm.patchRu?.techniques, tech.id, "name", tech.name);
    const desc = localizedField(vm.patchRu?.techniques, tech.id, "description", tech.description);
    const hay = `${tech.id} ${name} ${desc}`.toLowerCase();
    if (!hay.includes(q)) continue;
    const subMeta =
      tech.is_subtechnique && tech.parent_id
        ? state.lang === "ru"
          ? `под ${tech.parent_id}`
          : `sub of ${tech.parent_id}`
        : "";
    results.push({
      type: "technique",
      id: tech.id,
      name,
      href: `#/technique/${encodeURIComponent(tech.id)}`,
      meta: subMeta,
    });
  }

  for (const g of vm.base.groups || []) {
    const name = localizedField(vm.patchRu?.groups, g.id, "name", g.name);
    const desc = localizedField(vm.patchRu?.groups, g.id, "description", g.description);
    const aliases = (g.aliases || []).join(" ");
    const hay = `${g.id} ${name} ${aliases} ${desc}`.toLowerCase();
    if (!hay.includes(q)) continue;
    results.push({ type: "group", id: g.id, name, href: `#/group/${encodeURIComponent(g.id)}` });
  }

  for (const sw of vm.base.software || []) {
    const name = localizedField(vm.patchRu?.software, sw.id, "name", sw.name);
    const desc = localizedField(vm.patchRu?.software, sw.id, "description", sw.description);
    const aliases = (sw.aliases || []).join(" ");
    const hay = `${sw.id} ${name} ${aliases} ${desc}`.toLowerCase();
    if (!hay.includes(q)) continue;
    results.push({
      type: "software",
      id: sw.id,
      name,
      href: `#/software/${encodeURIComponent(sw.id)}`,
      meta: softwareTypeLabel(sw.type),
    });
  }

  for (const m of vm.base.mitigations || []) {
    const name = localizedField(vm.patchRu?.mitigations, m.id, "name", m.name);
    const desc = localizedField(vm.patchRu?.mitigations, m.id, "description", m.description);
    const hay = `${m.id} ${name} ${desc}`.toLowerCase();
    if (!hay.includes(q)) continue;
    results.push({ type: "mitigation", id: m.id, name, href: `#/mitigation/${encodeURIComponent(m.id)}` });
  }

  const typeOrder = { technique: 1, group: 2, software: 3, mitigation: 4 };
  results.sort((a, b) => (typeOrder[a.type] || 99) - (typeOrder[b.type] || 99) || a.id.localeCompare(b.id));

  const bodyHtml =
    results.length === 0
      ? `<div class="muted">${escapeHtml(s.searchEmpty)}</div>`
      : gridHtml(
          results.slice(0, 200).map((r) => {
            const parts = [typeLabel(r.type)];
            if (r.meta) parts.push(r.meta);
            const meta = parts.join(", ");
            return entityItemHtml({ href: r.href, id: r.id, name: r.name, meta });
          }),
          { total: results.length, limit: 200 }
        );

  setMain(
    card({
      title: s.searchTitle,
      subtitle: query,
      bodyHtml,
    })
  );
}

async function renderRoute() {
  document.documentElement.lang = state.lang;
  dom.langToggle.textContent = state.lang.toUpperCase();
  dom.domainSelect.value = state.domain;
  syncUiStrings();

  renderLoading();

  let vm;
  try {
    vm = await loadDomain(state.domain);
  } catch (err) {
    renderNoData(err);
    return;
  }

  const route = parseHash();
  if (route.path === "/about") {
    renderAbout();
    return;
  }

  if (route.path === "/navigator") {
    renderNavigator(vm);
    return;
  }

  if (route.path === "/techniques") {
    renderTechniquesList(vm);
    return;
  }

  if (route.path.startsWith("/technique/")) {
    const techniqueId = decodeURIComponent(route.parts[1] || "");
    renderTechnique(vm, techniqueId);
    return;
  }

  if (route.path === "/groups") {
    renderGroupsList(vm);
    return;
  }

  if (route.path.startsWith("/group/")) {
    const groupId = decodeURIComponent(route.parts[1] || "");
    renderGroup(vm, groupId);
    return;
  }

  if (route.path === "/software") {
    renderSoftwareList(vm);
    return;
  }

  if (route.path.startsWith("/software/")) {
    const softwareId = decodeURIComponent(route.parts[1] || "");
    renderSoftware(vm, softwareId);
    return;
  }

  if (route.path === "/mitigations") {
    renderMitigationsList(vm);
    return;
  }

  if (route.path.startsWith("/mitigation/")) {
    const mitigationId = decodeURIComponent(route.parts[1] || "");
    renderMitigation(vm, mitigationId);
    return;
  }

  if (route.path === "/search") {
    renderSearch(vm, route.params.get("q") || "");
    return;
  }

  renderMatrix(vm);
}

function init() {
  dom.domainSelect.value = state.domain;
  dom.domainSelect.addEventListener("change", () => {
    state.domain = dom.domainSelect.value;
    savePref(STORAGE_KEYS.domain, state.domain);
    renderRoute();
  });

  dom.langToggle.textContent = state.lang.toUpperCase();
  dom.langToggle.addEventListener("click", () => {
    state.lang = state.lang === "ru" ? "en" : "ru";
    savePref(STORAGE_KEYS.lang, state.lang);
    renderRoute();
  });

  dom.searchForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const q = (dom.searchInput.value || "").trim();
    if (!q) return;
    location.hash = `#/search?q=${encodeURIComponent(q)}`;
  });

  window.addEventListener("hashchange", renderRoute);
  renderRoute();
}

init();
