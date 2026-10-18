#!/usr/bin/env python3
"""Собирает страницы ролей, банк кейсов, страницы CV и sitemap.xml из content/*.toml.

Запуск из любого места: python3 scripts/build.py
Нужен Python 3.11+ (tomllib), сторонних библиотек нет.

Генерирует (руками не править, перезапишутся):
  <slug>/index.html, ru/<slug>/index.html   страницы ролей
  cases/index.html, ru/cases/index.html     все кейсы
  pet-projects/index.html, ru/pet-projects/index.html  пет-проекты из content/pet-projects.toml
  cv.html, ru/cv.html                       список CV
  sitemap.xml
Главные страницы index.html и ru/index.html пишутся руками.
"""

import datetime
import tomllib
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://pershutkina.com"
LANGS = ("en", "ru")

# Сколько первых кейсов роли показывать целиком; остальные идут коротким списком.
FEATURED = 3

UI = {
    "en": {
        "name": "Svetlana Pershutkina",
        "skip": "Skip to content",
        "sections": "Sections",
        "language": "Language",
        "other_title": "Русская версия",
        "home": "/",
        "cases": "Work cases",
        "pet": "Pet projects",
        "skills": "Skills",
        "experience": "Experience",
        "education": "Education",
        "about": "About",
        "profile": "Full profile",
        "cv": "CV",
        "download_cv": "Download CV (PDF)",
        "selected_cases": "Selected cases",
        "more_cases": "More cases",
        "recognition": "Selected recognition",
        "location": "Moscow, Russia · Open to relocation · Remote worldwide",
        "skills_h": "Core skills",
        "experience_h": "Experience",
        "education_h": "Education",
        "full_profile_note": 'Full experience, education, publications and courses are on the <a href="/">main page</a>.',
        "task": "Task",
        "did": "What I did",
        "result": "Result",
        "stack": "Stack",
        "for_roles": "Relevant for",
        "cases_title": "Work cases",
        "cases_lede": "Projects from Whoosh, T-Bank, the Moscow Department of Transport and Harvard’s Spatial Data Lab: the task, what I did and what changed. Each role page below shows the cases that matter most for that role.",
        "by_role": "Cases by role",
        "all_cases": "All cases",
        "cv_title": "CV by role",
        "cv_lede": "One-page PDFs with the same facts, each with a different focus. Every role also has its own page with selected cases. The <a href=\"/\">main page</a> has the full version.",
        "cv_download": "Download",
        "role_page": "Role page with cases",
        "kb": "KB",
        "footer_main": "Main page",
        "desc_role": "Svetlana Pershutkina, {title}: {focus}. Selected cases with results.",
        "desc_cases": "Case studies by Svetlana Pershutkina: analytics in micromobility, fintech and transport planning, with task, approach and results.",
        "pet_title": "Pet projects",
        "pet_lede": "Projects I do outside work: to try new tools, data and ideas.",
        "pet_empty": "Projects will appear here soon.",
        "desc_pet": "Pet projects by Svetlana Pershutkina: data and analytics projects outside work.",
        "desc_cv": "Download Svetlana Pershutkina’s CV in PDF, tailored to six roles: data, product and operations analytics.",
        "og_locale": "en_GB",
    },
    "ru": {
        "name": "Светлана Першуткина",
        "skip": "Перейти к содержанию",
        "sections": "Разделы",
        "language": "Язык",
        "other_title": "English version",
        "home": "/ru/",
        "cases": "Рабочие кейсы",
        "pet": "Пет-проекты",
        "skills": "Навыки",
        "experience": "Опыт",
        "education": "Образование",
        "about": "Обо мне",
        "profile": "Полный профиль",
        "cv": "CV",
        "download_cv": "Скачать CV (PDF)",
        "selected_cases": "Кейсы",
        "more_cases": "Ещё кейсы",
        "recognition": "Признание",
        "location": "Москва · готова к переезду · удалённо из любой страны",
        "skills_h": "Ключевые навыки",
        "experience_h": "Опыт работы",
        "education_h": "Образование",
        "full_profile_note": 'Полный опыт, образование, публикации и курсы на <a href="/ru/">главной странице</a>.',
        "task": "Задача",
        "did": "Что сделала",
        "result": "Результат",
        "stack": "Стек",
        "for_roles": "Подходит для ролей",
        "cases_title": "Рабочие кейсы",
        "cases_lede": "Проекты в Whoosh, Т-Банке, Департаменте транспорта Москвы и гарвардской Spatial Data Lab: задача, что я сделала и что изменилось. На странице каждой роли собраны самые подходящие для неё кейсы.",
        "by_role": "Кейсы по ролям",
        "all_cases": "Все кейсы",
        "cv_title": "CV под разные роли",
        "cv_lede": "Одностраничные PDF с одними и теми же фактами, но с разным фокусом. Все резюме на английском. У каждой роли есть своя страница с подобранными кейсами, полная версия на русском на <a href=\"/ru/\">главной странице</a>.",
        "cv_download": "Скачать",
        "role_page": "Страница роли с кейсами",
        "kb": "КБ",
        "footer_main": "Главная",
        "desc_role": "Светлана Першуткина, {title}: {focus}. Подобранные кейсы с результатами.",
        "desc_cases": "Кейсы Светланы Першуткиной: аналитика в микромобильности, финтехе и транспортном планировании. Задача, подход и результат.",
        "pet_title": "Пет-проекты",
        "pet_lede": "Проекты, которые я делаю вне работы: пробую новые инструменты, данные и идеи.",
        "pet_empty": "Скоро здесь появятся проекты.",
        "desc_pet": "Пет-проекты Светланы Першуткиной: проекты по данным и аналитике вне работы.",
        "desc_cv": "Резюме Светланы Першуткиной в PDF под шесть ролей: аналитика данных, продукта и операций.",
        "og_locale": "ru_RU",
    },
}

CONTACTS = [
    ("mailto:pershutkina2000@gmail.com", "pershutkina2000@gmail.com", False),
    ("https://www.linkedin.com/in/svetlana-p-6a78ba103/", "LinkedIn", True),
    ("https://t.me/svetlanapallna", "Telegram", True),
]
EXT = 'target="_blank" rel="noopener noreferrer"'


def load(name):
    with open(ROOT / "content" / name, "rb") as f:
        return tomllib.load(f)


def url(lang, path):
    """path без языкового префикса: '/', '/cases/', '/cv.html'."""
    return path if lang == "en" else "/ru" + path


def other(lang):
    return "ru" if lang == "en" else "en"


def contact_link(href, text, external):
    return f'<a href="{href}" {EXT}>{text}</a>' if external else f'<a href="{href}">{text}</a>'


def page(lang, path, title, description, nav, body, og_type="website"):
    t = UI[lang]
    alt = other(lang)
    en_url, ru_url = SITE + url("en", path), SITE + url("ru", path)
    cur = ' aria-current="page"'
    nav_html = "\n".join(
        f'        <a href="{href}"{cur if current else ""}>{label}</a>'
        for href, label, current in nav
    )
    if lang == "en":
        lang_html = (f'        <span aria-current="true">EN</span>\n'
                     f'        <a href="{url(alt, path)}" hreflang="ru" lang="ru" title="{t["other_title"]}">RU</a>')
    else:
        lang_html = (f'        <a href="{url(alt, path)}" hreflang="en" lang="en" title="{t["other_title"]}">EN</a>\n'
                     f'        <span aria-current="true">RU</span>')
    footer_links = "\n".join(f"        <li>{contact_link(*c)}</li>" for c in CONTACTS)
    alt_locale = UI[alt]["og_locale"]
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{escape(description)}">
  <link rel="canonical" href="{SITE + url(lang, path)}">
  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="ru" href="{ru_url}">
  <link rel="alternate" hreflang="x-default" href="{en_url}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:url" content="{SITE + url(lang, path)}">
  <meta property="og:image" content="{SITE}/assets/og.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="{t["og_locale"]}">
  <meta property="og:locale:alternate" content="{alt_locale}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#1f5135">
  <link rel="icon" href="/favicon.svg?v=2" type="image/svg+xml">
  <link rel="icon" href="/favicon.ico?v=2" sizes="32x32">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png?v=2">
  <link rel="stylesheet" href="/assets/style.css">
  <script src="/assets/lang.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">{t["skip"]}</a>

  <header class="topbar">
    <div class="wrap">
      <a class="topbar__name" href="{t["home"]}">{t["name"]}</a>
      <nav class="nav" aria-label="{t["sections"]}">
{nav_html}
      </nav>
      <div class="lang" role="group" aria-label="{t["language"]}">
{lang_html}
      </div>
    </div>
  </header>

  <main id="main">
    <div class="wrap">
{body}
    </div>
  </main>

  <footer>
    <div class="wrap">
      <ul>
{footer_links}
        <li><a href="{t["home"]}">{t["footer_main"]}</a></li>
      </ul>
      <p>© {datetime.date.today().year} {t["name"]}</p>
    </div>
  </footer>
</body>
</html>
"""


def facts_html(facts, lang):
    items = "\n".join(
        f"          <div>\n            <dt>{f['value']}</dt>\n            <dd>{f[lang]}</dd>\n          </div>"
        for f in facts
    )
    return f'        <dl class="facts">\n{items}\n        </dl>'


def case_html(case, lang, roles_by_case=None):
    t = UI[lang]
    c = case[lang]
    org = case.get("org_ru", case["org"]) if lang == "ru" else case["org"]
    metrics = ""
    if case["metrics"]:
        items = "\n".join(
            f"            <div><dt>{m['value']}</dt><dd>{m[lang]}</dd></div>" for m in case["metrics"]
        )
        metrics = f'\n          <dl class="case__metrics">\n{items}\n          </dl>'
    actions = "\n".join(f"            <li>{a}</li>" for a in c["actions"])
    roles = ""
    if roles_by_case:
        links = ", ".join(
            # якорь только если кейс показан на странице роли целиком
            f'<a href="{url(lang, "/" + r["slug"] + "/")}'
            f'{"#" + case["id"] if case["id"] in r["cases"][:FEATURED] else "#cases"}">{r["title"]}</a>'
            for r in roles_by_case.get(case["id"], [])
        )
        if links:
            roles = f'\n          <p class="case__roles">{t["for_roles"]}: {links}</p>'
    return f"""        <article class="case" id="{case["id"]}" aria-labelledby="{case["id"]}-h">
          <p class="case__org">{org} · {case["when"][lang]}</p>
          <h3 id="{case["id"]}-h">{c["title"]}</h3>{metrics}
          <p><b>{t["task"]}.</b> {c["problem"]}</p>
          <p class="case__label"><b>{t["did"]}</b></p>
          <ul>
{actions}
          </ul>
          <p><b>{t["result"]}.</b> {c["result"]}</p>
          <p class="stack"><b>{t["stack"]}:</b> {case["stack"]}</p>{roles}
        </article>"""


def role_page(role, cases, exp, lang):
    t = UI[lang]
    r = role[lang]
    pdf = f"/cv/{role['pdf']}"
    contacts = "\n".join(f"          <li>{contact_link(*c)}</li>" for c in CONTACTS)
    featured, rest = role["cases"][:FEATURED], role["cases"][FEATURED:]
    case_blocks = "\n\n".join(case_html(cases[cid], lang) for cid in featured)
    more = ""
    if rest:
        items = []
        for cid in rest:
            c = cases[cid]
            m = c["metrics"][0] if c["metrics"] else None
            note = f" · {m['value']} {m[lang]}" if m else ""
            org = c.get("org_ru", c["org"]) if lang == "ru" else c["org"]
            items.append(f'          <li><a href="{url(lang, "/cases/")}#{cid}">{c[lang]["title"]}</a> '
                         f'<span>{org}{note}</span></li>')
        more = (f'\n\n        <h3 class="intro__h">{t["more_cases"]}</h3>\n'
                f'        <ul class="more-cases">\n' + "\n".join(items) + "\n        </ul>")
    recognition = ""
    if role.get("recognition"):
        items = "\n".join(f"          <li>{x[lang]}</li>" for x in role["recognition"])
        recognition = f"""

      <section id="recognition" aria-labelledby="recognition-h">
        <h2 id="recognition-h">{t["recognition"]}</h2>
        <ul class="plain recognition">
{items}
        </ul>
      </section>"""
    skills = "\n".join(
        f"          <div>\n            <dt>{name}</dt>\n            <dd>{text}</dd>\n          </div>"
        for name, text in r["skills"]
    )
    jobs = "\n".join(
        f"""        <div class="entry">
          <div class="entry__date">{j[lang]["when"]}</div>
          <div>
            <h3>{j[lang]["title"]}</h3>
            <p class="entry__org"><a href="{j["url"]}" {EXT}>{j[lang]["org"]}</a> · {j[lang]["note"]}</p>
          </div>
        </div>"""
        for j in exp["jobs"]
    )
    edu = "\n".join(
        f"""        <div class="entry">
          <div class="entry__date">{e[lang]["when"]}</div>
          <div>
            <h3>{e[lang]["title"]}</h3>
            <p class="entry__org">{e[lang]["org"]}</p>
          </div>
        </div>"""
        for e in exp["education"]
    )
    body = f"""      <div class="intro">
        <h1>{t["name"]}</h1>
        <p class="role">{role["title"]}</p>
        <p class="focus">{r["focus"]}</p>
        <p class="lede">{r["lede"]}</p>
        <p class="location">{t["location"]}</p>
        <ul class="contacts">
          <li><a class="button" href="{pdf}" download>{t["download_cv"]}</a></li>
{contacts}
        </ul>

{facts_html(role["facts"], lang)}
      </div>

      <section id="cases" aria-labelledby="cases-h">
        <h2 id="cases-h">{t["selected_cases"]}</h2>

{case_blocks}{more}
      </section>

      <section id="skills" aria-labelledby="skills-h">
        <h2 id="skills-h">{t["skills_h"]}</h2>
        <dl class="skills">
{skills}
        </dl>
      </section>

      <section id="experience" aria-labelledby="experience-h">
        <h2 id="experience-h">{t["experience_h"]}</h2>
{jobs}
      </section>{recognition}

      <section id="education" aria-labelledby="education-h">
        <h2 id="education-h">{t["education_h"]}</h2>
{edu}
        <p class="small muted note-after">{t["full_profile_note"]}</p>
      </section>"""
    nav = [
        ("#cases", t["cases"], False),
        ("#skills", t["skills"], False),
        ("#experience", t["experience"], False),
        (t["home"], t["profile"], False),
    ]
    title = f"{t['name']}, {role['title']}"
    desc = t["desc_role"].format(title=role["title"], focus=r["focus"].replace(" · ", ", "))
    return page(lang, f"/{role['slug']}/", title, desc, nav, body, og_type="profile")


def main_nav(lang, current):
    t = UI[lang]
    h = t["home"]
    return [
        (h + "#skills", t["skills"], False),
        (h + "#education", t["education"], False),
        (h + "#experience", t["experience"], False),
        (url(lang, "/cases/"), t["cases"], current == "cases"),
        (url(lang, "/pet-projects/"), t["pet"], current == "pet"),
        (h + "#about", t["about"], False),
        (url(lang, "/cv.html"), t["cv"], current == "cv"),
    ]


def cases_page(roles, cases, lang):
    t = UI[lang]
    roles_by_case = {}
    for r in roles:
        for cid in r["cases"]:
            roles_by_case.setdefault(cid, []).append(r)
    role_links = "\n".join(
        f'          <li><a href="{url(lang, "/" + r["slug"] + "/")}">{r["title"]}</a></li>' for r in roles
    )
    blocks = "\n\n".join(case_html(c, lang, roles_by_case) for c in cases.values())
    body = f"""      <div class="intro">
        <h1>{t["cases_title"]}</h1>
        <p class="lede">{t["cases_lede"]}</p>
        <h2 class="intro__h">{t["by_role"]}</h2>
        <ul class="role-links">
{role_links}
        </ul>
      </div>

      <section id="all" aria-labelledby="all-h">
        <h2 id="all-h">{t["all_cases"]}</h2>

{blocks}
      </section>"""
    title = f"{t['cases_title']}: {t['name']}"
    return page(lang, "/cases/", title, t["desc_cases"], main_nav(lang, "cases"), body)


def pet_page(pets, lang):
    t = UI[lang]
    items = []
    for p in pets:
        d = p[lang]
        link = f'\n          <p><a href="{p["href"]}">{d.get("link", "")}</a></p>' if p.get("href") else ""
        stack = f'\n          <p class="stack"><b>{t["stack"]}:</b> {p["stack"]}</p>' if p.get("stack") else ""
        items.append(f"""        <article class="case" id="{p["id"]}" aria-labelledby="{p["id"]}-h">
          <p class="case__org">{p.get("year", "")}</p>
          <h3 id="{p["id"]}-h">{d["title"]}</h3>
          <p>{d["summary"]}</p>{stack}{link}
        </article>""")
    content = "\n\n".join(items) if items else f'        <p class="muted">{t["pet_empty"]}</p>'
    body = f"""      <div class="intro">
        <h1>{t["pet_title"]}</h1>
        <p class="lede">{t["pet_lede"]}</p>
      </div>

      <section id="projects" aria-label="{t["pet_title"]}">
{content}
      </section>"""
    title = f"{t['pet_title']}: {t['name']}"
    return page(lang, "/pet-projects/", title, t["desc_pet"], main_nav(lang, "pet"), body)


def cv_page(roles, lang):
    t = UI[lang]
    items = []
    for r in roles:
        size = round((ROOT / "cv" / r["pdf"]).stat().st_size / 1024)
        items.append(f"""          <li>
            <div>
              <h3><a href="{url(lang, "/" + r["slug"] + "/")}">{r["title"]}</a></h3>
              <p>{r[lang]["summary"]} <a href="{url(lang, "/" + r["slug"] + "/")}">{t["role_page"]}</a></p>
            </div>
            <a class="dl" href="/cv/{r["pdf"]}" download>PDF, {size} {t["kb"]}</a>
          </li>""")
    body = f"""      <div class="intro">
        <h1>{t["cv_title"]}</h1>
        <p class="lede">{t["cv_lede"]}</p>
      </div>

      <section id="download" aria-labelledby="cv-h">
        <h2 id="cv-h">{t["cv_download"]}</h2>
        <ul class="cv-list">
{chr(10).join(items)}
        </ul>
      </section>"""
    title = f"{t['cv_title']}: {t['name']}"
    return page(lang, "/cv.html", title, t["desc_cv"], main_nav(lang, "cv"), body)


def sitemap(paths):
    today = datetime.date.today().isoformat()
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for path in paths:
        for lang in LANGS:
            out += [
                "  <url>",
                f"    <loc>{SITE + url(lang, path)}</loc>",
                f"    <lastmod>{today}</lastmod>",
                f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE + url("en", path)}"/>',
                f'    <xhtml:link rel="alternate" hreflang="ru" href="{SITE + url("ru", path)}"/>',
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE + url("en", path)}"/>',
                "  </url>",
            ]
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def write(rel, text):
    p = ROOT / rel.lstrip("/")
    if rel.endswith("/"):
        p = p / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print("wrote", p.relative_to(ROOT))


def check(roles, cases):
    ids = set(cases)
    for r in roles:
        for cid in r["cases"]:
            if cid not in ids:
                raise SystemExit(f"roles.toml: роль {r['slug']} ссылается на несуществующий кейс {cid!r}")
        if not (ROOT / "cv" / r["pdf"]).exists():
            raise SystemExit(f"roles.toml: нет файла cv/{r['pdf']}")
    used = {cid for r in roles for cid in r["cases"]}
    for cid in ids - used:
        print(f"note: кейс {cid!r} не входит ни в одну роль, он будет только на /cases/")


def main():
    cases = {c["id"]: c for c in load("cases.toml")["cases"]}
    roles = load("roles.toml")["roles"]
    exp = load("experience.toml")
    pets = load("pet-projects.toml").get("projects", [])
    check(roles, cases)
    for lang in LANGS:
        for role in roles:
            write(url(lang, f"/{role['slug']}/"), role_page(role, cases, exp, lang))
        write(url(lang, "/cases/"), cases_page(roles, cases, lang))
        write(url(lang, "/pet-projects/"), pet_page(pets, lang))
        write(url(lang, "/cv.html"), cv_page(roles, lang))
    paths = ["/", "/cv.html", "/cases/", "/pet-projects/"] + [f"/{r['slug']}/" for r in roles]
    write("/sitemap.xml", sitemap(paths))


if __name__ == "__main__":
    main()
