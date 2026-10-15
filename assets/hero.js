// Заставка на главной: имя собирается по буквам, при прокрутке уезжает
// и уступает место содержанию. Без JS имя просто видно целиком.
// lang.js подменяет .hero при смене языка и шлёт событие page:swap,
// тогда заставка настраивается заново.
(() => {
  const root = document.documentElement;
  const still = window.matchMedia('(prefers-reduced-motion: reduce)');
  let hero = null;
  let ticking = false;

  // Каждая буква в своём span с номером --i: CSS по нему задаёт задержку.
  const split = (h) => {
    if (h.dataset.split) return;
    const lines = [...h.querySelectorAll('.hero__line')];
    const label = lines.map((l) => l.textContent.trim()).join(' ');
    let i = 0;
    for (const line of lines) {
      const text = line.textContent.trim();
      line.textContent = '';
      line.setAttribute('aria-hidden', 'true');
      for (const ch of text) {
        const s = document.createElement('span');
        s.className = 'hero__char';
        s.style.setProperty('--i', i++);
        s.textContent = ch;
        line.append(s);
      }
    }
    h.setAttribute('aria-label', label);
    h.dataset.split = '1';
  };

  const update = () => {
    ticking = false;
    if (!hero) return;
    const h = hero.offsetHeight || 1;
    const p = Math.min(Math.max(window.scrollY / h, 0), 1);
    hero.style.setProperty('--p', p.toFixed(3));
  };

  const onScroll = () => {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(update);
    }
  };

  const setup = () => {
    hero = document.querySelector('.hero');
    if (!hero) return;
    const name = hero.querySelector('.hero__name');
    if (name) split(name);
    const svg = hero.querySelector('svg');
    if (svg && svg.pauseAnimations && still.matches) svg.pauseAnimations();
    // Класс ставим кадром позже, чтобы браузер успел отрисовать исходное состояние.
    requestAnimationFrame(() => requestAnimationFrame(() => hero.classList.add('is-ready')));
    update();
  };

  root.classList.add('js-hero');
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  document.addEventListener('page:swap', setup);
  setup();
})();
