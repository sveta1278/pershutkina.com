// Переключение EN/RU без перезагрузки страницы.
// Скрипт загружает страницу на другом языке, подменяет шапку, <main> и подвал
// и меняет адрес через History API. Позиция прокрутки сохраняется по ближайшему
// разделу с тем же id. Без JS (или при ошибке) ссылка работает как обычная.
(() => {
  if (!window.fetch || !window.DOMParser || !history.pushState) return;

  const cache = new Map();
  let current = location.pathname;

  const load = (href) => {
    const key = new URL(href, location.href).pathname;
    if (!cache.has(key)) {
      const p = fetch(key, { credentials: 'same-origin' })
        .then((r) => {
          if (!r.ok) throw new Error(r.status);
          return r.text();
        })
        .then((html) => new DOMParser().parseFromString(html, 'text/html'));
      p.catch(() => cache.delete(key));
      cache.set(key, p);
    }
    return cache.get(key);
  };

  // Раздел или кейс, который читают сейчас (последний, чей верх в верхней
  // четверти экрана), и его смещение от верха окна.
  const anchor = () => {
    if (window.scrollY < 10) return null;
    const limit = window.innerHeight / 4;
    let best = null;
    for (const el of document.querySelectorAll('main section[id], main article[id]')) {
      const y = el.getBoundingClientRect().top;
      if (y <= limit) best = { id: el.id, offset: y };
      else break;
    }
    return best;
  };

  const swap = (doc, a) => {
    document.documentElement.lang = doc.documentElement.lang;
    document.title = doc.title;
    for (const sel of ['meta[name="description"]', 'link[rel="canonical"]']) {
      const from = doc.querySelector(sel);
      const to = document.querySelector(sel);
      if (from && to) to.replaceWith(document.importNode(from, true));
    }
    for (const sel of ['.skip-link', '.topbar', 'main', 'footer']) {
      const from = doc.querySelector(sel);
      const to = document.querySelector(sel);
      if (from && to) to.replaceWith(document.importNode(from, true));
    }
    if (a) {
      const el = document.getElementById(a.id);
      if (el) window.scrollBy(0, el.getBoundingClientRect().top - a.offset);
    } else {
      window.scrollTo(0, 0);
    }
  };

  const go = (href, push) => {
    const target = new URL(href, location.href);
    const a = anchor();
    return load(target.pathname)
      .then((doc) => {
        if (push) history.pushState({ lang: true }, '', target.pathname + location.hash);
        current = location.pathname;
        swap(doc, a);
        load(location.pathname); // кэшируем текущую страницу для «Назад»
        prefetch();
      })
      .catch(() => {
        location.href = target.pathname + location.hash;
      });
  };

  const prefetch = () => {
    const link = document.querySelector('.lang a[hreflang]');
    if (link) load(link.getAttribute('href'));
  };

  document.addEventListener('click', (e) => {
    const link = e.target.closest && e.target.closest('.lang a[hreflang]');
    if (!link || e.defaultPrevented || e.button !== 0) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    go(link.getAttribute('href'), true).then(() => {
      // Фокус остаётся на переключателе языка, а не прыгает в начало страницы.
      const next = document.querySelector('.lang a[hreflang]');
      if (next) next.focus({ preventScroll: true });
    });
  });

  window.addEventListener('popstate', () => {
    if (location.pathname !== current) go(location.href, false);
  });

  const idle = window.requestIdleCallback || ((fn) => setTimeout(fn, 1500));
  idle(prefetch);
})();
