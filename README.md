# pershutkina.com

Сайт-портфолио Светланы Першуткиной: аналитик данных. Статический HTML + CSS без фреймворков. Страницы ролей, кейсов и CV собираются скриптом на Python из файлов `content/*.toml`. JavaScript два файла: переключение языка без перезагрузки и заставка с именем на главной. Размещён на GitHub Pages с доменом `pershutkina.com`.

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
scripts/build.py    сборка страниц ролей, кейсов, CV и sitemap.xml
assets/lang.js      переключение EN/RU без перезагрузки страницы
assets/hero.js      заставка на главной: имя собирается по буквам, при прокрутке уезжает
_config.yml         что GitHub Pages не публикует (content/, scripts/, README.md)
content/cases.toml      банк кейсов (EN + RU)
content/roles.toml      роли: тексты, цифры, навыки и список кейсов
content/experience.toml короткий опыт и образование для страниц ролей
content/pet-projects.toml  пет-проекты; материалы кладутся в pet-projects/files/

Генерируются build.py (руками не править):
<роль>/index.html, ru/<роль>/index.html   страницы ролей, например /senior-product-analyst/
cases/index.html, ru/cases/index.html     все кейсы
pet-projects/index.html, ru/pet-projects/index.html  пет-проекты
cv.html, ru/cv.html, sitemap.xml
```

## Роли и кейсы

У каждой роли своя страница: под ней свои описание, цифры, кейсы, навыки и PDF. Эту ссылку и прикладывайте к отклику, например `https://pershutkina.com/senior-product-analyst/` или `https://pershutkina.com/ru/analytics-lead/`. Ссылка на конкретный кейс: `…/senior-product-analyst/#ride-quality`.

- На странице роли первые три кейса из `cases = [...]` показываются целиком, остальные коротким списком «Ещё кейсы». Порядок в списке и есть приоритет.
- Блок признания на странице роли: массив `recognition` у роли в `roles.toml`, одна-три строки.
- Новый кейс: добавьте блок `[[cases]]` в `content/cases.toml` и впишите его `id` в `cases = [...]` нужных ролей в `content/roles.toml`.
- Новая роль: добавьте блок `[[roles]]` в `content/roles.toml` и положите её PDF в `cv/`.
- После любых правок в `content/*.toml` запустите `python3 scripts/build.py` (нужен Python 3.11+) и закоммитьте получившиеся HTML.

## Как обновить раздел

Тексты лежат прямо в HTML. Английская версия в `index.html`, русская в `ru/index.html`. Правьте обе. Разделы находятся по `id`: `skills`, `education`, `experience`, `about`. Заставка с именем стоит в блоке `<div class="hero">` перед `<main>`; анимация отключается, если в системе включено «уменьшить движение».

- Новое место работы: скопируйте блок `<div class="entry">…</div>` в разделе `experience` и поставьте его первым.
- Новое CV: см. «Роли и кейсы» выше, `cv.html` и `sitemap.xml` собираются скриптом.

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
