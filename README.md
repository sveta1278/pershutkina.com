# pershutkina.com

Сайт-портфолио Светланы Першуткиной: аналитик данных. Статический HTML + CSS без сборки, фреймворков и JavaScript. Размещён на GitHub Pages с доменом `pershutkina.com`.

## Устройство

```
index.html          главная, английская версия
cv.html             скачивание CV под разные роли (EN)
ru/index.html       главная, русская версия
ru/cv.html          скачивание CV (RU)
404.html            страница «не найдено» (на двух языках)
assets/style.css    все стили; цвета заданы переменными в :root
assets/og.png       картинка для превью ссылок
cv/*.pdf            PDF-резюме под роли
favicon.svg, favicon.ico, assets/apple-touch-icon.png
robots.txt, sitemap.xml, CNAME
content/profile.md  черновик всех фактов с источниками (в вёрстку не подключается)
scripts/check_links.sh  проверка ссылок
```

## Как обновить раздел

Тексты лежат прямо в HTML. Английская версия в `index.html`, русская в `ru/index.html`. Правьте обе. Разделы находятся по `id`: `skills`, `education`, `experience`, `about`.

- Новое место работы: скопируйте блок `<div class="entry">…</div>` в разделе `experience` и поставьте его первым.
- Новое CV: положите PDF в `cv/` и добавьте пункт `<li>` в `cv.html` и `ru/cv.html`.
- После правок обновите `<lastmod>` в `sitemap.xml`.

## Локальный запуск

```bash
python3 -m http.server 8000
```

Затем откройте http://localhost:8000.

## Проверки

```bash
bash scripts/check_links.sh
```

Скрипт проходит по всем ссылкам `<a href>` во всех HTML-файлах. Внешние ссылки он проверяет по коду ответа, внутренние по наличию файла и якоря. LinkedIn отвечает ботам кодом 999, его проверяйте вручную.

```bash
npx html-validate index.html cv.html ru/index.html ru/cv.html 404.html
```

```bash
npx lighthouse http://localhost:8000/ --view
```
