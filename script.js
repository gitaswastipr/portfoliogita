(function () {
  const root = document.documentElement;
  root.classList.add('js');

  // Theme: saved choice, else system preference
  const toggle = document.querySelector('.theme-toggle');
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  let saved = null;
  try { saved = localStorage.getItem('theme'); } catch (e) {}
  const applyTheme = (theme) => root.setAttribute('data-theme', theme);
  applyTheme(saved || (media.matches ? 'dark' : 'light'));

  toggle.addEventListener('click', () => {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });
  media.addEventListener('change', (e) => {
    let stored = null;
    try { stored = localStorage.getItem('theme'); } catch (err) {}
    if (!stored) applyTheme(e.matches ? 'dark' : 'light');
  });

  // Mobile menu
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.getElementById('nav-links');
  const closeMenu = () => {
    navLinks.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
    navToggle.setAttribute('aria-label', 'Open menu');
  };
  navToggle.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(open));
    navToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });
  navLinks.querySelectorAll('a').forEach((a) => a.addEventListener('click', closeMenu));

  // Header border on scroll
  const header = document.querySelector('.site-header');
  const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 8);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Reveal on scroll + count-up stats
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const countUp = (el) => {
    const target = Number(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    if (reduceMotion) { el.textContent = target + suffix; return; }
    const start = performance.now();
    const duration = 1200;
    const tick = (now) => {
      const t = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (t < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };

  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('visible');
        const num = entry.target.querySelector('[data-count]');
        if (num) countUp(num);
        io.unobserve(entry.target);
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('visible'));
  }

  // Active nav link
  const sections = document.querySelectorAll('main section[id]');
  const links = navLinks.querySelectorAll('a[href^="#"]');
  if ('IntersectionObserver' in window) {
    const navIO = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((l) => l.classList.toggle('active', l.getAttribute('href') === '#' + entry.target.id));
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach((s) => navIO.observe(s));
  }

  // Photo lightbox
  const lightbox = document.querySelector('.lightbox');
  if (lightbox && typeof lightbox.showModal === 'function') {
    const lbImg = lightbox.querySelector('img');
    document.querySelectorAll('a.zoom').forEach((link) => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const img = link.querySelector('img');
        lbImg.src = link.getAttribute('href');
        lbImg.alt = img ? img.alt : '';
        lightbox.showModal();
      });
    });
    lightbox.querySelector('.lightbox-close').addEventListener('click', () => lightbox.close());
    lightbox.addEventListener('click', (e) => { if (e.target === lightbox) lightbox.close(); });
  }

  document.getElementById('year').textContent = new Date().getFullYear();
})();
