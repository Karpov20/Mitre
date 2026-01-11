#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set
from urllib.parse import urljoin, urlparse


BASE_URL = "https://mitre-attack.github.io/attack-navigator/"
ATTACK_VERSION = "14"
INDEX_NAME = "MITRE ATT&CK"
COLLECTION_NAMES = {
    "enterprise": "Enterprise ATT&CK",
    "mobile": "Mobile ATT&CK",
    "ics": "ICS ATT&CK",
}

ASSET_EXT_RE = re.compile(r"""["']([^"'?#]+\.(?:css|js|svg|png|jpg|jpeg|gif|webp|ico|json|woff2?|ttf|eot|map))["']""")
URL_REF_RE = re.compile(r"url\\(([^)]+)\\)")
GTAG_JS_RE = re.compile(r"<script[^>]*googletagmanager\\.com/gtag/js[^>]*></script>", re.S)
GTAG_INLINE_RE = re.compile(r"<script>.*?dataLayer.*?</script>", re.S)
BASE_RE = re.compile(r"<base href=\"[^\"]*\">", re.I)
HTML_LANG_RE = re.compile(r"(<html\\s[^>]*?)\\slang=\"[^\"]*\"", re.I)
FONT_URL_RE = re.compile(r"url\(([^)]+)\)")
OVERRIDE_LINK = '<link rel="stylesheet" href="override.css">'
TRANSLATE_SCRIPT = '<script src="translate.js" defer></script>'
FONT_CSS_URLS = {
    "material-icons.css": "https://fonts.googleapis.com/icon?family=Material+Icons",
    "material-symbols.css": "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200",
}
FONT_LINKS = [
    '<link rel="stylesheet" href="assets/fonts/material-icons.css">',
    '<link rel="stylesheet" href="assets/fonts/material-symbols.css">',
]
OVERRIDE_CSS = """\
:root {
  --attack-bg: #0b1020;
  --attack-panel: rgba(255, 255, 255, 0.06);
  --attack-panel-2: rgba(255, 255, 255, 0.09);
  --attack-text: rgba(255, 255, 255, 0.92);
  --attack-muted: rgba(255, 255, 255, 0.7);
  --attack-border: rgba(255, 255, 255, 0.12);
  --attack-accent: #7c3aed;
  --attack-accent-2: #22c55e;
  --attack-accent-soft: rgba(124, 58, 237, 0.2);
  --attack-panel-solid: rgba(10, 12, 24, 0.96);
  --attack-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
  --attack-radius: 14px;
  --attack-radius-sm: 10px;
  --attack-font: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

@media (prefers-color-scheme: light) {
  :root {
    --attack-bg: #f6f7fb;
    --attack-panel: rgba(16, 24, 40, 0.06);
    --attack-panel-2: rgba(16, 24, 40, 0.09);
    --attack-text: rgba(16, 24, 40, 0.92);
    --attack-muted: rgba(16, 24, 40, 0.72);
    --attack-border: rgba(16, 24, 40, 0.15);
    --attack-accent: #6d28d9;
    --attack-accent-2: #16a34a;
    --attack-accent-soft: rgba(109, 40, 217, 0.14);
    --attack-panel-solid: rgba(255, 255, 255, 0.98);
    --attack-shadow: 0 12px 30px rgba(16, 24, 40, 0.12);
  }
}

html,
body {
  background: radial-gradient(1200px 800px at 20% 0%, rgba(124, 58, 237, 0.22), transparent 55%),
    radial-gradient(900px 700px at 90% 10%, rgba(34, 197, 94, 0.14), transparent 50%),
    var(--attack-bg);
  color: var(--attack-text);
  font: 14.5px/1.45 var(--attack-font);
}

body {
  margin: 0;
}

a {
  color: var(--attack-accent);
}

html {
  --mdc-theme-primary: var(--attack-accent);
  --mdc-theme-secondary: var(--attack-accent-2);
  --mdc-theme-background: transparent;
  --mdc-theme-surface: var(--attack-panel);
  --mdc-theme-on-surface: var(--attack-text);
  --mdc-theme-on-primary: #fff;
  --mat-app-background-color: transparent;
  --mat-app-text-color: var(--attack-text);
  --mat-option-label-text-color: var(--attack-text);
  --mat-option-selected-state-label-text-color: var(--attack-accent);
  --mat-option-hover-state-layer-color: var(--attack-accent-soft);
  --mat-option-focus-state-layer-color: var(--attack-accent-soft);
  --mat-option-selected-state-layer-color: var(--attack-accent-soft);
  --mdc-elevated-card-container-color: var(--attack-panel);
  --mdc-outlined-card-container-color: var(--attack-panel);
  --mdc-outlined-card-outline-color: var(--attack-border);
  --mdc-filled-text-field-container-color: var(--attack-panel-2);
  --mat-select-panel-background-color: var(--attack-panel);
  --mat-menu-container-color: var(--attack-panel);
  --mat-sidenav-container-background-color: var(--attack-panel);
  --mat-sidenav-content-background-color: transparent;
  --mat-sidenav-container-text-color: var(--attack-text);
  --mat-toolbar-container-background-color: var(--attack-panel);
  --mat-toolbar-container-text-color: var(--attack-text);
  --mdc-dialog-container-color: var(--attack-panel);
}

[class*="mat-elevation-z"],
.mat-mdc-elevation-specific {
  box-shadow: var(--attack-shadow);
}

.app-container {
  padding: 12px;
}

.nav-app {
  display: grid;
  gap: 12px;
}

.tabs-container {
  border: 1px solid var(--attack-border);
  border-radius: var(--attack-radius);
  background: var(--attack-panel);
  box-shadow: var(--attack-shadow);
  overflow: hidden;
}

.tabs {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 10px;
  background: var(--attack-panel-2);
  border-bottom: 1px solid var(--attack-border);
}

.tab-title {
  font-weight: 650;
  letter-spacing: 0.2px;
}

.new-tab,
.add-tab,
.tab-enumerator {
  border-radius: var(--attack-radius-sm);
  border: 1px solid var(--attack-border);
  background: var(--attack-panel);
  color: var(--attack-text);
}

.tab-enumerator-highlight {
  background: var(--attack-accent);
  color: #fff;
}

.tab-close {
  color: var(--attack-muted);
}

.tab-close:hover {
  color: var(--attack-text);
}

.version-footer {
  align-self: flex-end;
  border: 1px dashed var(--attack-border);
  background: color-mix(in srgb, var(--attack-panel) 80%, transparent);
  color: var(--attack-muted);
  padding: 6px 12px;
  border-radius: 999px;
}

.logo h1 {
  margin: 0;
  font-size: 22px;
  font-weight: 750;
  letter-spacing: 0.3px;
}

.logo a {
  color: var(--attack-text);
  text-decoration: none;
}

.logo a:hover {
  color: var(--attack-accent);
}

.help-links-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.mat-mdc-button-base,
.mat-mdc-raised-button,
.mat-mdc-unelevated-button,
.mat-mdc-outlined-button {
  border-radius: var(--attack-radius-sm);
  border: 1px solid var(--attack-border);
  background-color: var(--attack-panel-2);
  color: var(--attack-text);
}

.mat-mdc-button-base:hover {
  background-color: var(--attack-accent-soft);
  border-color: var(--attack-accent);
}

.mat-app-background,
.mat-drawer-inner-container,
.mat-mdc-dialog-container .mdc-dialog__surface,
.mat-mdc-menu-panel,
.mat-mdc-select-panel,
.mat-mdc-autocomplete-panel,
.mat-mdc-card {
  background-color: var(--attack-panel);
  color: var(--attack-text);
  border: 1px solid var(--attack-border);
  box-shadow: var(--attack-shadow);
}

.mat-mdc-tab-header,
.mat-mdc-tab-nav-bar {
  background-color: var(--attack-panel);
  border-bottom: 1px solid var(--attack-border);
}

.mat-mdc-tab-group,
.mat-mdc-tab-nav-bar {
  color: var(--attack-text);
}

.mdc-tab__text-label {
  color: var(--attack-text);
}

.mdc-tab--active .mdc-tab__text-label {
  color: var(--attack-accent);
}

.controlsContainer,
.theme-use-system .controlsContainer,
.theme-override-dark .controlsContainer,
.theme-override-light .controlsContainer {
  background-color: var(--attack-panel);
  border-bottom: 1px solid var(--attack-border);
  backdrop-filter: blur(10px);
}

.controlsContainer .control-sections > li {
  border-left: 1px solid var(--attack-border);
}

.controlsContainer .control-sections > li .section-label {
  background-color: var(--attack-panel-2);
  color: var(--attack-muted);
  border: 1px solid var(--attack-border);
  border-radius: 8px 8px 0 0;
}

.controlsContainer .control-sections > li .dropdown-container {
  background-color: var(--attack-panel);
  border-color: var(--attack-border);
  box-shadow: var(--attack-shadow);
}

.controlsContainer .control-sections > li .control-row-item .control-row-button {
  border-radius: 8px;
  border: 1px solid var(--attack-border);
  background-color: var(--attack-panel-2);
  color: var(--attack-text);
}

.controlsContainer .control-sections > li .control-row-item .control-row-button:hover {
  background-color: var(--attack-accent-soft);
  border-color: var(--attack-accent);
}

.headers-align {
  display: grid;
  gap: 10px;
}

.mat-expansion-panel {
  border-radius: var(--attack-radius);
  border: 1px solid var(--attack-border);
  background: var(--attack-panel);
  overflow: hidden;
}

.mat-expansion-panel-header {
  background: var(--attack-panel-2);
  color: var(--attack-text);
}

.mat-expansion-panel:not(:first-of-type) {
  margin-top: 8px;
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 8px 0 4px;
}

.multi-column-container {
  display: grid;
  grid-template-columns: minmax(240px, 1fr) minmax(260px, 1fr);
  gap: 16px;
}

.multi-column-container .md-column + .md-column {
  border-left: 1px solid var(--attack-border);
  padding-left: 16px;
}

@media (max-width: 960px) {
  .multi-column-container {
    grid-template-columns: 1fr;
  }

  .multi-column-container .md-column + .md-column {
    border-left: none;
    border-top: 1px solid var(--attack-border);
    padding-left: 0;
    padding-top: 16px;
  }
}

.section {
  color: var(--attack-muted);
}

.text-deemphasis {
  color: var(--attack-muted);
}

.contextMenu-header,
.control-section-header {
  background: var(--attack-panel-2);
  border-bottom: 1px solid var(--attack-border);
  color: var(--attack-text);
}

.matrix {
  border-radius: var(--attack-radius);
  border: 1px solid var(--attack-border);
  background: var(--attack-panel);
  overflow: hidden;
}

.matrix-name {
  background: var(--attack-panel-2);
  color: var(--attack-text);
  font-weight: 650;
  padding: 8px 10px;
  border-bottom: 1px solid var(--attack-border);
}

.matrix-column {
  border-left: 1px solid var(--attack-border);
}

.technique,
.technique-name,
.subtechnique,
.supertechnique {
  color: var(--attack-text);
}

.subtechnique .technique-name {
  color: var(--attack-muted);
}

.techniques-table {
  border-collapse: separate;
  border-spacing: 0 6px;
}

.technique-cell,
.subtechniques-td {
  border: 1px solid var(--attack-border);
}

.control-label {
  color: var(--attack-muted);
}

.mat-mdc-form-field .mdc-notched-outline__leading,
.mat-mdc-form-field .mdc-notched-outline__notch,
.mat-mdc-form-field .mdc-notched-outline__trailing {
  border-color: var(--attack-border);
}

.mat-mdc-form-field {
  background: var(--attack-panel-2);
  border-radius: var(--attack-radius-sm);
  border: 1px solid var(--attack-border);
}

.mat-mdc-form-field .mdc-text-field {
  background: transparent;
}

.mat-mdc-form-field.mat-focused .mdc-notched-outline__leading,
.mat-mdc-form-field.mat-focused .mdc-notched-outline__notch,
.mat-mdc-form-field.mat-focused .mdc-notched-outline__trailing {
  border-color: var(--attack-accent);
}

.mat-mdc-input-element,
.mat-mdc-select-value-text,
.mat-mdc-form-field .mdc-floating-label,
.mat-mdc-form-field-hint {
  color: var(--attack-text);
}

.checkbox-custom + .checkbox-custom-label:before {
  border-color: var(--attack-border);
  background: var(--attack-panel);
}

.material-icons,
.material-symbols-outlined,
mat-icon,
.mat-icon {
  font-family: "Material Icons", "Material Symbols Outlined", "Material Icons Round", sans-serif !important;
  font-feature-settings: "liga";
  -webkit-font-feature-settings: "liga";
  font-variant-ligatures: normal;
}

.tabs-container,
.version-footer {
  display: none !important;
}

.mat-mdc-button-base,
.mdc-button {
  background: var(--attack-panel);
  color: var(--attack-text);
  border: 1px solid var(--attack-border);
  text-transform: none;
}

.mat-mdc-button-base:hover,
.mdc-button:hover {
  background: var(--attack-panel-2);
  border-color: var(--attack-accent);
}

.mat-mdc-select-value-text,
.mat-mdc-option .mdc-list-item__primary-text,
.mat-mdc-menu-item .mdc-list-item__primary-text {
  color: var(--attack-text);
}

.mat-mdc-select,
.mat-mdc-option,
.mat-mdc-menu-item {
  background: var(--attack-panel);
}

.cdk-overlay-pane .mat-mdc-select-panel,
.cdk-overlay-pane .mat-mdc-menu-panel,
.cdk-overlay-pane .mat-mdc-autocomplete-panel {
  background-color: var(--attack-panel-solid);
  border: 1px solid var(--attack-border);
  box-shadow: var(--attack-shadow);
  backdrop-filter: blur(12px);
}

.cdk-overlay-pane .mat-mdc-option.mdc-list-item,
.cdk-overlay-pane .mat-mdc-menu-item {
  background-color: var(--attack-panel-2);
}

.cdk-overlay-pane .mat-mdc-option.mdc-list-item--selected,
.cdk-overlay-pane .mat-mdc-option:hover,
.cdk-overlay-pane .mat-mdc-menu-item:hover {
  background-color: var(--attack-accent-soft);
}

.cdk-overlay-pane .mat-mdc-option + .mat-mdc-option,
.cdk-overlay-pane .mat-mdc-menu-item + .mat-mdc-menu-item {
  border-top: 1px solid var(--attack-border);
}
"""
TRANSLATE_JS = r"""(() => {
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

  const getDomainParam = () => {
    const params = new URL(window.location.href).searchParams;
    const raw = (params.get("domain") || "").toLowerCase();
    if (raw === "mobile" || raw === "ics" || raw === "enterprise") return raw;
    return "enterprise";
  };

  const tryAutoCreateLayer = () => {
    if (window.__ATTACK_NAV_AUTO_LAYER__) return true;
    if (document.querySelector(".matrix, .techniques-table")) {
      window.__ATTACK_NAV_AUTO_LAYER__ = true;
      return true;
    }
    const domain = getDomainParam();
    const labels = { enterprise: "Enterprise", mobile: "Mobile", ics: "ICS" };
    const targetLabel = labels[domain] || "Enterprise";
    const header = document.querySelector("mat-expansion-panel mat-expansion-panel-header");
    if (header && header.getAttribute("aria-expanded") !== "true") {
      header.click();
    }
    const buttons = Array.from(document.querySelectorAll(".button-group button"));
    const match = buttons.find((btn) => btn.textContent.trim().toLowerCase() === targetLabel.toLowerCase());
    if (match) {
      match.click();
      window.__ATTACK_NAV_AUTO_LAYER__ = true;
      return true;
    }
    return false;
  };

  const scheduleAutoLayer = () => {
    if (window.__ATTACK_NAV_AUTO_LAYER__) return;
    let attempts = 0;
    const timer = setInterval(() => {
      attempts += 1;
      if (tryAutoCreateLayer() || attempts >= 20) {
        clearInterval(timer);
      }
    }, 400);
  };

  const apply = () => {
    translateTree(document.body);
    patchLinks(document);
    patchTitle();
    scheduleAutoLayer();
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
"""


def _read_url(url: str, timeout: float | None = 30.0) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "attack-ru-site/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _write_text(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _is_local_path(path: str) -> bool:
    if not path:
        return False
    if path.startswith("http://") or path.startswith("https://"):
        return False
    if path.startswith("data:"):
        return False
    if path.startswith("//"):
        return False
    return True


def _extract_asset_paths(text: str) -> Set[str]:
    out: Set[str] = set()
    for m in ASSET_EXT_RE.findall(text):
        if _is_local_path(m):
            out.add(m)
    for m in URL_REF_RE.findall(text):
        if isinstance(m, tuple):
            m = "".join(m)
        cleaned = m.strip().strip("'\"")
        if _is_local_path(cleaned):
            out.add(cleaned)
    return out


def _download_assets(base_url: str, out_dir: Path, paths: Iterable[str]) -> List[Path]:
    downloaded: List[Path] = []
    for rel in paths:
        url = urljoin(base_url, rel)
        dest = out_dir / rel
        if dest.exists():
            downloaded.append(dest)
            continue
        try:
            data = _read_url(url)
        except Exception:
            continue
        _write_bytes(dest, data)
        downloaded.append(dest)
    return downloaded


def _download_font_css(url: str, out_dir: Path, file_name: str) -> None:
    css = _read_url(url, timeout=15.0).decode("utf-8", errors="ignore")
    font_urls: List[str] = []
    for m in FONT_URL_RE.findall(css):
        if isinstance(m, tuple):
            m = "".join(m)
        cleaned = m.strip().strip("'\"")
        if not cleaned or cleaned.startswith("data:"):
            continue
        font_urls.append(cleaned)

    stem = Path(file_name).stem
    for font_url in font_urls:
        parsed = urlparse(font_url)
        base = Path(parsed.path).name
        local_name = f"{stem}-{base}"
        dest = out_dir / local_name
        if not dest.exists():
            try:
                data = _read_url(font_url, timeout=15.0)
            except Exception:
                continue
            _write_bytes(dest, data)
        css = css.replace(font_url, local_name)

    _write_text(out_dir / file_name, css)


def _utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _patch_external_refs(obj: Dict[str, Any]) -> None:
    stix_type = obj.get("type")
    if stix_type not in ("attack-pattern", "intrusion-set", "malware", "tool", "course-of-action"):
        return
    refs = obj.get("external_references") or []
    for ref in refs:
        if ref.get("source_name") != "mitre-attack":
            continue
        external_id = ref.get("external_id")
        if not external_id:
            continue
        if stix_type == "attack-pattern":
            ref["url"] = f"../#/technique/{external_id}"
        elif stix_type == "intrusion-set":
            ref["url"] = f"../#/group/{external_id}"
        elif stix_type in ("malware", "tool"):
            ref["url"] = f"../#/software/{external_id}"
        elif stix_type == "course-of-action":
            ref["url"] = f"../#/mitigation/{external_id}"


def _extract_external_id(obj: Dict[str, Any]) -> str | None:
    for ref in obj.get("external_references") or []:
        if ref.get("source_name") != "mitre-attack":
            continue
        external_id = ref.get("external_id")
        if external_id:
            return external_id
    return None


def _apply_localization(stix: Dict[str, Any], patch: Dict[str, Any]) -> None:
    if not patch:
        return
    maps = {
        "attack-pattern": patch.get("techniques") or {},
        "x-mitre-tactic": patch.get("tactics") or {},
        "intrusion-set": patch.get("groups") or {},
        "malware": patch.get("software") or {},
        "tool": patch.get("software") or {},
        "course-of-action": patch.get("mitigations") or {},
    }
    for obj in stix.get("objects") or []:
        stix_type = obj.get("type")
        mapping = maps.get(stix_type)
        if not mapping:
            continue
        external_id = _extract_external_id(obj)
        if not external_id:
            continue
        localized = mapping.get(external_id)
        if not localized:
            continue
        name = localized.get("name")
        description = localized.get("description")
        if name:
            obj["name"] = name
        if description:
            obj["description"] = description


def _prepare_local_stix(
    data_dir: Path, assets_dir: Path, localization: Dict[str, Dict[str, Any]] | None = None
) -> Dict[str, str]:
    mapping = {
        "enterprise": "enterprise-attack.json",
        "mobile": "mobile-attack.json",
        "ics": "ics-attack.json",
    }
    out_paths: Dict[str, str] = {}
    for domain, file_name in mapping.items():
        src = data_dir / f"{domain}.stix.json"
        if not src.exists():
            raise RuntimeError(f"Не найден файл {src}. Сначала запустите scripts/fetch_attack.py")
        stix = _load_json(src)
        for obj in stix.get("objects") or []:
            _patch_external_refs(obj)
        if localization and localization.get(domain):
            _apply_localization(stix, localization[domain])
        dst = assets_dir / file_name
        _write_json(dst, stix)
        out_paths[domain] = f"assets/{file_name}"
    return out_paths


def _build_index(out_paths: Dict[str, str]) -> Dict[str, Any]:
    now = _utc_now_iso()
    return {
        "id": "local-collection-index",
        "name": INDEX_NAME,
        "description": "Local ATT&CK mirror for this site",
        "created": now,
        "modified": now,
        "collections": [
            {
                "id": "x-mitre-collection--local-enterprise",
                "name": COLLECTION_NAMES["enterprise"],
                "description": "Local Enterprise ATT&CK dataset",
                "created": now,
                "versions": [{"version": ATTACK_VERSION, "modified": now, "url": out_paths["enterprise"]}],
            },
            {
                "id": "x-mitre-collection--local-mobile",
                "name": COLLECTION_NAMES["mobile"],
                "description": "Local Mobile ATT&CK dataset",
                "created": now,
                "versions": [{"version": ATTACK_VERSION, "modified": now, "url": out_paths["mobile"]}],
            },
            {
                "id": "x-mitre-collection--local-ics",
                "name": COLLECTION_NAMES["ics"],
                "description": "Local ICS ATT&CK dataset",
                "created": now,
                "versions": [{"version": ATTACK_VERSION, "modified": now, "url": out_paths["ics"]}],
            },
        ],
    }


def _update_config(config_path: Path) -> None:
    cfg = _load_json(config_path)
    cfg["collection_index_url"] = "assets/index.json"
    cfg["banner"] = ""
    if isinstance(cfg.get("default_layers"), dict):
        cfg["default_layers"]["enabled"] = False
        cfg["default_layers"]["urls"] = []
    if isinstance(cfg.get("features"), list):
        for feat in cfg["features"]:
            if feat.get("name") == "header":
                feat["enabled"] = False
    _write_json(config_path, cfg)


def _sanitize_index(html: str) -> str:
    html = html.replace(
        '<script async src="https://www.googletagmanager.com/gtag/js?id=G-GFD952VXH6"></script>', ""
    )
    html = GTAG_JS_RE.sub("", html)
    html = GTAG_INLINE_RE.sub("", html)
    if BASE_RE.search(html):
        html = BASE_RE.sub('<base href="./">', html)
    if HTML_LANG_RE.search(html):
        html = HTML_LANG_RE.sub(r"\1 lang=\"ru\"", html, count=1)
    for link in FONT_LINKS:
        if link not in html:
            html = re.sub(r"</head>", f"{link}</head>", html, flags=re.I, count=1)
    if OVERRIDE_LINK not in html:
        html = re.sub(r"</head>", f"{OVERRIDE_LINK}</head>", html, flags=re.I, count=1)
    if TRANSLATE_SCRIPT not in html:
        html = re.sub(r"</body>", f"{TRANSLATE_SCRIPT}</body>", html, flags=re.I, count=1)
    return html


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch MITRE ATT&CK Navigator static build into site/navigator.")
    parser.add_argument("--out-dir", default="site/navigator", help="Output directory for navigator files")
    parser.add_argument("--data-dir", default="data/raw", help="Directory with <domain>.stix.json files")
    parser.add_argument("--site-data-dir", default="site/data", help="Directory with <domain>.<lang>.json translations")
    parser.add_argument("--lang", default="ru", help="Localization language for navigator data/UI")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    data_dir = Path(args.data_dir)
    site_data_dir = Path(args.site_data_dir)
    lang = (args.lang or "").strip().lower()
    html = _read_url(BASE_URL).decode("utf-8", errors="ignore")
    html = _sanitize_index(html)
    _write_bytes(out_dir / "index.html", html.encode("utf-8"))
    _write_text(out_dir / "override.css", OVERRIDE_CSS)
    _write_text(out_dir / "translate.js", TRANSLATE_JS)

    # Initial assets from index.html
    asset_paths = _extract_asset_paths(html)
    downloaded = _download_assets(BASE_URL, out_dir, asset_paths)

    # Scan downloaded JS/CSS for nested assets.
    nested_paths: Set[str] = set()
    for path in downloaded:
        if path.suffix not in (".js", ".css"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        nested_paths |= _extract_asset_paths(text)

    if nested_paths:
        _download_assets(BASE_URL, out_dir, nested_paths)

    assets_dir = out_dir / "assets"
    fonts_dir = assets_dir / "fonts"
    for file_name, url in FONT_CSS_URLS.items():
        try:
            _download_font_css(url, fonts_dir, file_name)
        except Exception:
            continue
    localization: Dict[str, Dict[str, Any]] = {}
    if lang and lang != "en":
        for domain in ("enterprise", "mobile", "ics"):
            patch_path = site_data_dir / f"{domain}.{lang}.json"
            if patch_path.exists():
                localization[domain] = _load_json(patch_path)
    out_paths = _prepare_local_stix(data_dir=data_dir, assets_dir=assets_dir, localization=localization)
    index = _build_index(out_paths)
    _write_json(assets_dir / "index.json", index)

    config_path = assets_dir / "config.json"
    if config_path.exists():
        _update_config(config_path)

    print(f"[navigator] wrote {out_dir / 'index.html'} and assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
