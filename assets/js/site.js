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

  /* ---------- Back to top (case pages) ---------- */
  const up = document.querySelector('.totop');
  if (up) {
    const sync = () => up.classList.toggle('on', scrollY > innerHeight * 0.8);
    addEventListener('scroll', sync, { passive: true }); sync();
    up.addEventListener('click', () => scrollTo({ top: 0, behavior: reduce.matches ? 'auto' : 'smooth' }));
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

  /* ---------- Dock active state on home (sliding pill) ---------- */
  const dock = document.querySelector('.dock, .fx-nav');
  if (dock && document.body.classList.contains('home')) {
    const links = {};
    dock.querySelectorAll('a[data-sec]').forEach(a => links[a.dataset.sec] = a);
    const resumeLink = dock.querySelector('a[download]');
    if (resumeLink) links.resume = resumeLink;
    const pill = document.createElement('i');
    pill.className = 'pill'; pill.setAttribute('aria-hidden', 'true');
    dock.insertBefore(pill, dock.firstChild);
    let cur = null, first = true;
    const place = a => {
      pill.style.top = a.offsetTop + 'px'; pill.style.width = a.offsetWidth + 'px'; pill.style.height = a.offsetHeight + 'px';
      pill.style.transform = 'translateX(' + a.offsetLeft + 'px)';
    };
    const setActive = key => {
      const a = links[key]; if (!a || key === cur) return;
      cur = key;
      Object.values(links).forEach(l => l === a ? l.setAttribute('aria-current', 'page') : l.removeAttribute('aria-current'));
      if (first) { pill.style.transition = 'none'; place(a); pill.offsetWidth; pill.style.transition = ''; dock.classList.add('pl'); first = false; }
      else place(a);
    };
    const secTop = id => { const el = document.getElementById(id); return el ? el.getBoundingClientRect().top : Infinity; };
    const resumeEl = document.querySelector('.fx-resume');
    let tick = false;
    const calc = () => {
      tick = false;
      const vh = innerHeight;
      let key = 'home';
      if (secTop('work') < vh * 0.5) key = 'work';
      else if (secTop('cases') < vh * 0.5) key = 'cases';
      else if (resumeEl && resumeEl.getBoundingClientRect().top < vh * 0.7) key = 'resume';
      setActive(key);
    };
    const on = () => { if (!tick) { tick = true; requestAnimationFrame(calc); } };
    addEventListener('scroll', on, { passive: true }); addEventListener('resize', () => { on(); if (cur && links[cur]) { pill.style.transition = 'none'; place(links[cur]); pill.offsetWidth; pill.style.transition = ''; } });
    calc();
  }

  /* ---------- Hide dock at page bottom, show on scroll up ---------- */
  const fxNav = document.querySelector('.fx-nav');
  if (fxNav) {
    let last = scrollY;
    const chk = () => {
      const y = scrollY, atEnd = y + innerHeight >= root.scrollHeight - 8;
      if (atEnd) fxNav.classList.add('away');
      else if (y < last) fxNav.classList.remove('away');
      last = y;
    };
    addEventListener('scroll', chk, { passive: true });
    fxNav.addEventListener('focusin', () => fxNav.classList.remove('away'));
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
    lb.classList.toggle('big', fr.matches('.fgi, .sd'));
    lastFocus = fr; lbImg.src = img.currentSrc || img.src; lbImg.alt = img.alt;
    lb.classList.add('on'); document.body.style.overflow = 'hidden'; lbBtn.focus({ preventScroll: true });
  };
  document.querySelectorAll('.shot .fr, .cs-sol .rc, .cs-sol .sc, .cs-fig .fgi, .cs-arch .fgi, .cs-sol .rwx .fgi, .cs-ds .sd').forEach(fr => {
    fr.tabIndex = 0; fr.setAttribute('role', 'button'); fr.setAttribute('aria-label', 'Открыть: ' + (fr.querySelector('img')?.alt || 'изображение'));
    fr.addEventListener('click', () => open(fr));
    fr.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(fr); } });
  });
  lb.addEventListener('click', e => { if (e.target === lb || e.target === lbBtn || e.target.classList.contains('lb-scroll')) close(); });
  addEventListener('keydown', e => { if (e.key === 'Escape' && lb.classList.contains('on')) close(); });
})();
