# ATT&CK на русском (неофициально)

Статический сайт, который отображает MITRE ATT&CK (Enterprise/Mobile/ICS) и поддерживает русскую локализацию через отдельные файлы перевода.

Разделы на сайте:
- Матрица техник
- Техники (список + карточка)
- Группы (карточка + связи)
- ПО (malware/tool) (карточка + связи)
- Митигации (карточка + связи)

## Быстрый старт

1) Сгенерировать данные (английская база) из официальных STIX JSON:

```bash
python3 scripts/fetch_attack.py --domain all
```

2) (Опционально) Сгенерировать русский перевод (патч-перевод поверх английской базы):

```bash
python3 -m pip install argostranslate
python3 scripts/translate_attack_ru.py --domain all
```

3) Запустить локальный статический сервер:

```bash
python3 -m http.server 8000 -d site
```

Если порт `8000` занят — используйте другой, например `8001`:

```bash
python3 -m http.server 8001 -d site
```

Открыть `http://localhost:8000` (или `http://localhost:8001`).

## Как устроены данные

- `site/data/<domain>.json` — английская база (упрощённая структура для сайта)
- `site/data/<domain>.ru.json` — русские строки (патч). Если файла нет, сайт показывает английский текст.

Домены:
- `enterprise`
- `mobile`
- `ics`

## Публикация на GitHub Pages

В репозитории уже добавлен workflow для деплоя Pages из папки `site/`: `.github/workflows/pages.yml`.

1) Закоммить и запушь изменения в `main`:

```bash
cd Mitre
git add .
git commit -m "Deploy GitHub Pages"
git push
```

2) На GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

3) Дождись завершения workflow **Deploy GitHub Pages** (Actions).

Сайт будет доступен по адресу вида:
- `https://<username>.github.io/<repo>/`

## Атрибуция и лицензия

ATT&CK® — торговая марка The MITRE Corporation. Этот сайт **не является** официальным продуктом MITRE.

Содержимое ATT&CK (английский исходник) распространяется по лицензии **CC BY 4.0**:
- MITRE ATT&CK: https://attack.mitre.org/
- Лицензия: https://creativecommons.org/licenses/by/4.0/

Русский перевод (если вы его генерируете) является производной работой и может содержать неточности — используйте как справочный материал, а не как единственный источник.
