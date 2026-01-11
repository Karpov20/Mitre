(() => {
  if (window.__ATTACK_NAV_TRANSLATED__) return;
  window.__ATTACK_NAV_TRANSLATED__ = true;

  const EXACT = {
    "MITRE ATT&CK Navigator": "ATT&CK Навигатор",
    "MITRE ATT&CK® Navigator": "ATT&CK Навигатор",
    "ATT&CK Navigator": "ATT&CK Навигатор",
    "The ATT&CK Navigator is a web-based tool for annotating and exploring ATT&CK matrices. It can be used to visualize defensive coverage, red/blue team planning, the frequency of detected techniques, and more.":
      "ATT&CK Навигатор — веб-инструмент для аннотирования и изучения матриц ATT&CK. Он помогает визуализировать покрытие защит, планирование red/blue team, частоту обнаружения техник и многое другое.",
    "help": "справка",
    "changelog": "изменения",
    "theme": "тема",
    "new tab": "новая вкладка",
    "close tab": "закрыть вкладку",
    "Create New Layer": "Создать новый слой",
    "Create a new empty layer": "Создать новый пустой слой",
    "Open Existing Layer": "Открыть существующий слой",
    "Load a layer from your computer or a URL": "Загрузить слой с компьютера или по URL",
    "Create Layer from Other Layers": "Создать слой из других слоев",
    "Select layers to inherit properties from": "Выберите слои для наследования свойств",
    "Select the domain for the new layer.": "Выберите домен для нового слоя.",
    "Select the domain for the new layer. Only layers of the same domain and version can be merged.":
      "Выберите домен для нового слоя. Можно объединять только слои одного домена и версии.",
    "Only layers of the same domain and version can be merged.":
      "Можно объединять только слои одного домена и версии.",
    "Create Customized Navigator": "Создать настраиваемый навигатор",
    "Create a hyperlink to a customized ATT&CK Navigator": "Создать ссылку на настроенный ATT&CK Навигатор",
    "More Options": "Дополнительные параметры",
    "Create layer": "Создать слой",
    "Create layer from version": "Создать слой из версии",
    "Create layer from bundle": "Создать слой из набора",
    "Select a version": "Выберите версию",
    "Select a domain": "Выберите домен",
    "Use constants (numbers) and layer variables (yellow, above) to write an expression for the initial value of scores in the new layer.":
      "Используйте константы (числа) и переменные слоя (желтые выше), чтобы задать выражение для начального значения оценок в новом слое.",
    "A full list of supported operations can be found": "Полный список поддерживаемых операций можно найти",
    "Leave blank to initialize scores to 0.": "Оставьте пустым, чтобы инициализировать оценки нулем.",
    "Leave blank to initialize scores to 0. Here's a list of available layer variables:":
      "Оставьте пустым, чтобы инициализировать оценки нулем. Список доступных переменных слоя:",
    "Here's a list of available layer variables:": "Список доступных переменных слоя:",
    "Select which layer to import comments from. Leave blank to initialize with no comments.":
      "Выберите, из какого слоя импортировать комментарии. Оставьте пустым, чтобы начать без комментариев.",
    "Select which layer to import comments from.": "Выберите, из какого слоя импортировать комментарии.",
    "Leave blank to initialize with no comments.": "Оставьте пустым, чтобы начать без комментариев.",
    "Select which layer to import enabled/disabled states from. Leave blank to initialize all to enabled.":
      "Выберите, из какого слоя импортировать состояния включено/отключено. Оставьте пустым, чтобы все были включены.",
    "Select which layer to import enabled/disabled states from.":
      "Выберите, из какого слоя импортировать состояния включено/отключено.",
    "Leave blank to initialize all to enabled.": "Оставьте пустым, чтобы все были включены.",
    "Select which layer to import filters from. Leave blank to initialize with no filters.":
      "Выберите, из какого слоя импортировать фильтры. Оставьте пустым, чтобы начать без фильтров.",
    "Select which layer to import filters from.": "Выберите, из какого слоя импортировать фильтры.",
    "Leave blank to initialize with no filters.": "Оставьте пустым, чтобы начать без фильтров.",
    "Select which layer to import manually assigned colors from. Leave blank to initialize with no colors.":
      "Выберите, из какого слоя импортировать вручную заданные цвета. Оставьте пустым, чтобы начать без цветов.",
    "Select which layer to import manually assigned colors from.":
      "Выберите, из какого слоя импортировать вручную заданные цвета.",
    "Leave blank to initialize with no colors.": "Оставьте пустым, чтобы начать без цветов.",
    "Select which layer to import technique links from. Leave blank to initialize without links.":
      "Выберите, из какого слоя импортировать ссылки техник. Оставьте пустым, чтобы начать без ссылок.",
    "Select which layer to import technique links from.":
      "Выберите, из какого слоя импортировать ссылки техник.",
    "Leave blank to initialize without links.": "Оставьте пустым, чтобы начать без ссылок.",
    "Select which layer to import technique metadata from. Leave blank to initialize without metadata.":
      "Выберите, из какого слоя импортировать метаданные техник. Оставьте пустым, чтобы начать без метаданных.",
    "Select which layer to import technique metadata from.":
      "Выберите, из какого слоя импортировать метаданные техник.",
    "Leave blank to initialize without metadata.": "Оставьте пустым, чтобы начать без метаданных.",
    "Select which layer to import the legend from. Leave blank to initialize with an empty legend.":
      "Выберите, из какого слоя импортировать легенду. Оставьте пустым, чтобы начать с пустой легендой.",
    "Select which layer to import the legend from.": "Выберите, из какого слоя импортировать легенду.",
    "Leave blank to initialize with an empty legend.": "Оставьте пустым, чтобы начать с пустой легендой.",
    "Select which layer to import the scoring gradient from. Leave blank to initialize with the default scoring gradient.":
      "Выберите, из какого слоя импортировать градиент оценок. Оставьте пустым, чтобы использовать градиент по умолчанию.",
    "Select which layer to import the scoring gradient from.":
      "Выберите, из какого слоя импортировать градиент оценок.",
    "Leave blank to initialize with the default scoring gradient.":
      "Оставьте пустым, чтобы использовать градиент по умолчанию.",
    "Collection or STIX bundle URL": "URL коллекции или STIX-пакета",
    "Load from URL": "Загрузить по URL",
    "Bundle domain": "Домен набора",
    "Bundle version number": "Версия набора",
    "Aggregate Function": "Функция агрегирования",
    "Name": "Название",
    "Layer Settings": "Настройки слоя",
    "Layer settings": "Настройки слоя",
    "Layer name": "Название слоя",
    "Layer Name": "Название слоя",
    "Description": "Описание",
    "Domain": "Домен",
    "Version": "Версия",
    "Search": "Поиск",
    "Search techniques": "Поиск техник",
    "Filters": "Фильтры",
    "Filter": "Фильтр",
    "Sorting": "Сортировка",
    "Legend": "Легенда",
    "Color Setup": "Настройка цветов",
    "Show/Hide Disabled": "Показать/Скрыть отключенные",
    "Show Disabled": "Показать отключенные",
    "Hide Disabled": "Скрыть отключенные",
    "Sub-techniques": "Подтехники",
    "Sub-technique": "Подтехника",
    "Techniques": "Техники",
    "Technique": "Техника",
    "Tactics": "Тактики",
    "Tactic": "Тактика",
    "Matrix": "Матрица",
    "Download Layer": "Скачать слой",
    "Download layer": "Скачать слой",
    "Export": "Экспорт",
    "Import": "Импорт",
    "Open": "Открыть",
    "Close": "Закрыть",
    "Cancel": "Отмена",
    "Apply": "Применить",
    "Save": "Сохранить",
    "Reset": "Сбросить",
    "Delete": "Удалить",
    "Clear": "Очистить",
    "Add": "Добавить",
    "Remove": "Удалить",
    "Score": "Оценка",
    "Scores": "Оценки",
    "Comments": "Комментарии",
    "Metadata": "Метаданные",
    "Links": "Ссылки",
    "Select": "Выбрать",
    "Deselect": "Снять выбор",
    "Select all": "Выбрать все",
    "Deselect all": "Снять выбор",
    "Enabled": "Включено",
    "Disabled": "Отключено",
    "Add Item": "Добавить элемент",
    "Upload from local": "Загрузить локально",
    "Top ^": "Вверх ^",
    "Back": "Назад",
    "Done": "Готово",
    "Dismiss": "Скрыть",
    "Start": "Начать",
    "Yes": "Да",
    "No": "Нет",
    "Options": "Параметры",
    "Overview": "Обзор",
    "Finish": "Готово",
    "Skipped": "Пропущено",
    "Labels": "Метки",
    "Comment:": "Комментарий:",
    "Score:": "Оценка:",
    "Custom": "Пользовательский",
    "Landscape": "Альбомная",
    "Portrait": "Портретная",
    "Small: 11x17": "Маленький: 11x17",
    "Medium: 18x24": "Средний: 18x24",
    "Large 24x36": "Большой 24x36",
    "US Legal: 8.5x14": "US Legal: 8.5x14",
    "US Letter: 8.5x11": "US Letter: 8.5x11",
    "dark": "темная",
    "light": "светлая",
    "monospace": "моноширинный",
    "sans-serif": "без засечек",
    "serif": "с засечками",
    "none": "нет",
    "show all": "показать все",
    "show expanded": "показать раскрытые",
    "show none": "скрыть все",
    "use system": "как в системе",
    "custom navigator url": "URL настраиваемого навигатора",
    "coloring": "окраска",
    "comments": "комментарии",
    "links": "ссылки",
    "metadata": "метаданные",
    "domain": "домен",
    "filters": "фильтры",
    "font": "шрифт",
    "font size": "размер шрифта",
    "gradient": "градиент",
    "header height": "высота заголовка",
    "height": "высота",
    "legend": "легенда",
    "legend X position": "позиция легенды по X",
    "legend Y position": "позиция легенды по Y",
    "legend height": "высота легенды",
    "legend width": "ширина легенды",
    "orientation": "ориентация",
    "score": "оценка",
    "score expression": "выражение оценки",
    "size": "размер",
    "states": "состояния",
    "theme ▾": "тема ▾",
    "width": "ширина",
    "add another color": "добавить цвет"
  };

  const normalize = (value) => value.replace(/\s+/g, " ").trim();
  const EXACT_LOWER = Object.fromEntries(
    Object.entries(EXACT).map(([key, value]) => [key.toLowerCase(), value])
  );
  const EXACT_NORM = Object.fromEntries(Object.entries(EXACT).map(([key, value]) => [normalize(key), value]));
  const EXACT_LOWER_NORM = Object.fromEntries(
    Object.entries(EXACT).map(([key, value]) => [normalize(key).toLowerCase(), value])
  );

  const DYNAMIC = [
    { re: /^MITRE ATT&CK(?:®)? Navigator v/i, replace: "ATT&CK Навигатор v" },
    { re: /^MITRE ATT&CK(?:®)? Navigator$/i, replace: "ATT&CK Навигатор" },
    { re: /^ATT&CK Navigator v/i, replace: "ATT&CK Навигатор v" },
    { re: /^ATT&CK Navigator$/i, replace: "ATT&CK Навигатор" },
    { re: /^default layer\b\s*/i, replace: "Слой по умолчанию " }
  ];

  const WORDS = {
    layer: "слой",
    layers: "слои",
    technique: "техника",
    techniques: "техники",
    tactic: "тактика",
    tactics: "тактики",
    matrix: "матрица",
    score: "оценка",
    scores: "оценки",
    filter: "фильтр",
    filters: "фильтры",
    legend: "легенда",
    color: "цвет",
    colors: "цвета",
    background: "фон",
    show: "показать",
    hide: "скрыть",
    search: "поиск",
    download: "скачать",
    upload: "загрузить",
    import: "импорт",
    export: "экспорт",
    select: "выбрать",
    deselect: "снять",
    enabled: "включено",
    disabled: "отключено",
    settings: "настройки",
    options: "параметры",
    add: "добавить",
    remove: "удалить",
    comment: "комментарий",
    comments: "комментарии",
    link: "ссылка",
    links: "ссылки",
    metadata: "метаданные",
    overview: "обзор",
    orientation: "ориентация",
    width: "ширина",
    height: "высота",
    size: "размер",
    font: "шрифт",
    domain: "домен",
    here: "здесь",
    version: "версия",
    "sub-techniques": "подтехники",
    "sub-technique": "подтехника"
  };

  const ATTRS = ["placeholder", "title", "aria-label", "aria-placeholder"];
  const SKIP_TAGS = new Set(["SCRIPT", "STYLE", "NOSCRIPT", "MAT-ICON", "CODE", "PRE", "KBD"]);
  const hasLetters = /[A-Za-z]/;
  const wordRegex = /\b([A-Za-z][A-Za-z-]*)\b/g;

  const applyCase = (original, replacement) => {
    if (!replacement) return replacement;
    if (original.toUpperCase() === original) return replacement.toUpperCase();
    if (original.toLowerCase() === original) return replacement.toLowerCase();
    if (original[0].toUpperCase() === original[0] && original.slice(1).toLowerCase() === original.slice(1)) {
      return replacement[0].toUpperCase() + replacement.slice(1);
    }
    return replacement;
  };

  const translateSentence = (sentence) => {
    const raw = sentence ?? "";
    const trimmed = raw.trim();
    if (!trimmed || !hasLetters.test(trimmed)) return null;
    const normalized = normalize(trimmed);
    const exact = EXACT[trimmed];
    if (exact) return exact;
    const exactNorm = EXACT_NORM[normalized];
    if (exactNorm) return exactNorm;
    const exactLower = EXACT_LOWER[trimmed.toLowerCase()];
    if (exactLower) return applyCase(trimmed, exactLower);
    const exactNormLower = EXACT_LOWER_NORM[normalized.toLowerCase()];
    if (exactNormLower) return applyCase(trimmed, exactNormLower);

    for (const rule of DYNAMIC) {
      if (rule.re.test(trimmed)) {
        return trimmed.replace(rule.re, rule.replace);
      }
    }

    const out = trimmed.replace(wordRegex, (word) => {
      const repl = WORDS[word.toLowerCase()];
      if (!repl) return word;
      return applyCase(word, repl);
    });
    if (out !== trimmed) return out;
    return null;
  };

  const translateValue = (value) => {
    const raw = value ?? "";
    const trimmed = raw.trim();
    if (!trimmed || !hasLetters.test(trimmed)) return null;
    const normalized = normalize(trimmed);
    const exact = EXACT[trimmed];
    if (exact) return raw.replace(trimmed, exact);
    const exactNorm = EXACT_NORM[normalized];
    if (exactNorm) return raw.replace(trimmed, exactNorm);
    const exactLower = EXACT_LOWER[trimmed.toLowerCase()];
    if (exactLower) return raw.replace(trimmed, applyCase(trimmed, exactLower));
    const exactNormLower = EXACT_LOWER_NORM[normalized.toLowerCase()];
    if (exactNormLower) return raw.replace(trimmed, applyCase(trimmed, exactNormLower));

    for (const rule of DYNAMIC) {
      if (rule.re.test(trimmed)) {
        const out = trimmed.replace(rule.re, rule.replace);
        return raw.replace(trimmed, out);
      }
    }

    const sentenceParts = trimmed.split(/(?<=[.!?])\s+/);
    if (sentenceParts.length > 1) {
      const translatedParts = [];
      let changed = false;
      for (const part of sentenceParts) {
        const translated = translateSentence(part);
        if (translated) {
          translatedParts.push(translated);
          changed = true;
        } else {
          translatedParts.push(part);
        }
      }
      if (changed) return raw.replace(trimmed, translatedParts.join(" "));
    }

    const out = trimmed.replace(wordRegex, (word) => {
      const repl = WORDS[word.toLowerCase()];
      if (!repl) return word;
      return applyCase(word, repl);
    });
    if (out !== trimmed) return raw.replace(trimmed, out);
    return null;
  };

  const shouldSkip = (el) => {
    if (!el) return false;
    if (SKIP_TAGS.has(el.tagName)) return true;
    if (el.closest) {
      if (el.closest("mat-icon")) return true;
      if (el.closest(".material-icons, .material-symbols-outlined")) return true;
    }
    return false;
  };

  const translateNode = (node) => {
    if (node.nodeType === Node.TEXT_NODE) {
      const parent = node.parentElement;
      if (parent && shouldSkip(parent)) return;
      const translated = translateValue(node.nodeValue);
      if (translated) node.nodeValue = translated;
      return;
    }
    if (node.nodeType !== Node.ELEMENT_NODE) return;
    const el = node;
    if (shouldSkip(el)) return;
    for (const attr of ATTRS) {
      const value = el.getAttribute(attr);
      if (!value) continue;
      const translated = translateValue(value);
      if (translated) el.setAttribute(attr, translated.trim());
    }
    for (const child of node.childNodes) translateNode(child);
  };

  const translateTree = (root) => {
    if (!root) return;
    translateNode(root);
  };

  const patchLinks = (root) => {
    if (!root || !root.querySelectorAll) return;
    for (const link of root.querySelectorAll("a[href]")) {
      const href = link.getAttribute("href") || "";
      if (href.includes("attack.mitre.org")) {
        link.setAttribute("href", "../#/");
        link.setAttribute("rel", "noreferrer");
      }
    }
  };

  const patchTitle = () => {
    if (document.title && /Navigator/i.test(document.title)) {
      document.title = "ATT&CK Навигатор";
    }
  };

  const maybeClearNavigatorState = () => {
    let params;
    try {
      params = new URL(window.location.href).searchParams;
    } catch (_) {
      return;
    }
    const token = params.get("clear");
    if (!token) return;
    const clearedKey = "attack_nav_cleared_token";
    try {
      if (localStorage.getItem(clearedKey) === token) {
        return;
      }
      const keep = {
        attack_domain: localStorage.getItem("attack_domain"),
        attack_lang: localStorage.getItem("attack_lang")
      };
      localStorage.clear();
      if (keep.attack_domain) localStorage.setItem("attack_domain", keep.attack_domain);
      if (keep.attack_lang) localStorage.setItem("attack_lang", keep.attack_lang);
      localStorage.setItem(clearedKey, token);
      const url = new URL(window.location.href);
      url.searchParams.delete("clear");
      window.location.replace(url.toString());
    } catch (_) {
      return;
    }
  };

  const apply = () => {
    maybeClearNavigatorState();
    translateTree(document.body);
    patchLinks(document);
    patchTitle();
  };
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", apply);
  } else {
    apply();
  }

  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      for (const node of mutation.addedNodes) {
        translateNode(node);
        patchLinks(node);
      }
    }
  });
  observer.observe(document.documentElement, { childList: true, subtree: true });
  document.documentElement.lang = "ru";
})();
