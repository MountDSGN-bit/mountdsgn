(() => {
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');

  /* ---------- Page transitions ---------- */
  const LEAVE_MS = 230;
  addEventListener('pageshow', e => { if (e.persisted) root.classList.remove('is-leaving'); });
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]');
    if (!a) return;
    if (a.matches('.is-soon, [data-soon]')) { e.preventDefault(); return; }
    if (e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (a.target && a.target !== '_self' || a.hasAttribute('download')) return;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin) return;
    const samePage = url.pathname === location.pathname;
    if (samePage && url.hash) return;           // in-page anchor: native smooth scroll
    if (samePage && !url.hash && url.search === location.search) { e.preventDefault(); scrollTo({ top: 0, behavior: reduce.matches ? 'auto' : 'smooth' }); return; }
    if (reduce.matches) return;
    e.preventDefault();
    root.classList.add('is-leaving');
    setTimeout(() => { location.href = url.href; }, LEAVE_MS);
  });

  /* ---------- Reveal on scroll ---------- */
  const targets = [...document.querySelectorAll('[data-reveal]')];
  if ('IntersectionObserver' in window && !reduce.matches) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
    targets.forEach(t => io.observe(t));
  } else targets.forEach(t => t.classList.add('is-in'));

  /* ---------- Scroll progress (case pages) ---------- */
  const bar = document.querySelector('.progress');
  if (bar) {
    let tick = false;
    const upd = () => {
      const h = root.scrollHeight - innerHeight;
      bar.style.transform = `scaleX(${h > 0 ? Math.min(1, scrollY / h) : 0})`;
      tick = false;
    };
    addEventListener('scroll', () => { if (!tick) { tick = true; requestAnimationFrame(upd); } }, { passive: true });
    upd();
  }

  /* ---------- Accordion (experience) ---------- */
  document.querySelectorAll('.job-btn, .fx-job .name').forEach(btn => {
    const body = document.getElementById(btn.getAttribute('aria-controls'));
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      body.hidden = open;
    });
  });

  /* ---------- Dock active state on home ---------- */
  const dock = document.querySelector('.dock, .fx-nav');
  if (dock && document.body.classList.contains('home') && 'IntersectionObserver' in window) {
    const map = { top: 'home', cases: 'cases', work: 'work' };
    const links = {};
    dock.querySelectorAll('a[data-sec]').forEach(a => links[a.dataset.sec] = a);
    const setActive = key => Object.entries(links).forEach(([k, a]) => k === key ? a.setAttribute('aria-current', 'page') : a.removeAttribute('aria-current'));
    const seen = new Map();
    const so = new IntersectionObserver(es => {
      es.forEach(en => seen.set(en.target.id, en.isIntersecting ? en.intersectionRatio : 0));
      let best = 'top', max = 0;
      seen.forEach((r, id) => { if (r > max) { max = r; best = id; } });
      setActive(map[best] || 'home');
    }, { threshold: [0, .15, .35, .6] });
    ['top', 'cases', 'work'].forEach(id => { const el = document.getElementById(id); if (el) so.observe(el); });
  }

  /* ---------- Lightbox for screens ---------- */
  const lb = document.createElement('div');
  lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Просмотр изображения');
  lb.innerHTML = '<div class="lb-scroll"><img alt=""></div><button type="button" aria-label="Закрыть">×</button>';
  document.body.appendChild(lb);
  const lbImg = lb.querySelector('img'), lbBtn = lb.querySelector('button');
  let lastFocus = null;
  const close = () => { lb.classList.remove('on'); document.body.style.overflow = ''; lastFocus && lastFocus.focus({ preventScroll: true }); };
  const open = fr => {
    const img = fr.querySelector('img'); if (!img) return;
    lastFocus = fr; lbImg.src = img.currentSrc || img.src; lbImg.alt = img.alt;
    lb.classList.add('on'); document.body.style.overflow = 'hidden'; lbBtn.focus({ preventScroll: true });
  };
  document.querySelectorAll('.shot .fr').forEach(fr => {
    fr.tabIndex = 0; fr.setAttribute('role', 'button'); fr.setAttribute('aria-label', 'Открыть: ' + (fr.querySelector('img')?.alt || 'изображение'));
    fr.addEventListener('click', () => open(fr));
    fr.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(fr); } });
  });
  lb.addEventListener('click', e => { if (e.target === lb || e.target === lbBtn || e.target.classList.contains('lb-scroll')) close(); });
  addEventListener('keydown', e => { if (e.key === 'Escape' && lb.classList.contains('on')) close(); });
})();
