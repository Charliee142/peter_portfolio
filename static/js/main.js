/* ================================================================
   Peter Charles Portfolio — Main JS
   Cybersecurity Engineer & Django Developer
   ================================================================ */
'use strict';

// ── AOS Init ─────────────────────────────────────────────────
function initAOS() {
  if (typeof AOS === 'undefined') return;
  AOS.init({
    duration: 650,
    easing: 'ease-out-cubic',
    once: true,
    offset: 50,
    disable: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
  });
}

// ── Premium Navbar ────────────────────────────────────────────
function initNavbar() {
  const nav      = document.getElementById('main-nav');
  const toggle   = document.getElementById('nav-toggle');
  const menu     = document.getElementById('mobile-menu');
  const overlay  = document.getElementById('menu-overlay');
  const closeBtn = document.getElementById('menu-close');

  if (!nav) return;

  // Scroll behaviour
  let ticking = false;
  function onScroll() {
    if (!ticking) {
      requestAnimationFrame(() => {
        nav.classList.toggle('scrolled', window.scrollY > 40);
        ticking = false;
      });
      ticking = true;
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile menu open
  function openMenu() {
    menu.removeAttribute('hidden');
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', 'Close navigation menu');
    document.body.style.overflow = 'hidden';
    // Focus first link for accessibility
    const firstLink = menu.querySelector('.mobile-nav-link');
    if (firstLink) requestAnimationFrame(() => firstLink.focus());
  }

  // Mobile menu close
  function closeMenu() {
    menu.setAttribute('hidden', '');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open navigation menu');
    document.body.style.overflow = '';
    toggle.focus();
  }

  if (toggle)   toggle.addEventListener('click', openMenu);
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  if (overlay)  overlay.addEventListener('click', closeMenu);

  // Keyboard: Escape closes menu
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && !menu.hasAttribute('hidden')) closeMenu();
  });

  // Trap focus inside mobile menu
  if (menu) {
    menu.addEventListener('keydown', e => {
      if (e.key !== 'Tab') return;
      const focusable = Array.from(
        menu.querySelectorAll('a, button, [tabindex]:not([tabindex="-1"])')
      ).filter(el => !el.disabled);
      if (!focusable.length) return;
      const first = focusable[0];
      const last  = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault(); last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault(); first.focus();
      }
    });
  }
}

// ── Animated Skill Bars ───────────────────────────────────────
function initSkillBars() {
  const bars = document.querySelectorAll('.skill-fill[data-width]');
  if (!bars.length) return;

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (prefersReduced) {
    bars.forEach(b => { b.style.width = b.dataset.width + '%'; });
    return;
  }

  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.width = e.target.dataset.width + '%';
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.3 });
  bars.forEach(b => obs.observe(b));
}

// ── Animated Counters ─────────────────────────────────────────
function initCounters() {
  const counters = document.querySelectorAll('.stat-num[data-target]');
  if (!counters.length) return;

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReduced) {
    counters.forEach(c => { c.textContent = c.dataset.target; });
    return;
  }

  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const target  = parseInt(e.target.dataset.target, 10);
      const el      = e.target;
      let current   = 0;
      const step    = Math.ceil(target / 55);
      const timer   = setInterval(() => {
        current += step;
        if (current >= target) { current = target; clearInterval(timer); }
        el.textContent = current;
      }, 22);
      obs.unobserve(el);
    });
  }, { threshold: 0.6 });
  counters.forEach(c => obs.observe(c));
}

// ── Tilt effect on project cards (subtle) ────────────────────
function initTilt() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (window.matchMedia('(max-width: 768px)').matches) return;

  document.querySelectorAll('.tilt-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const r  = card.getBoundingClientRect();
      const x  = ((e.clientX - r.left) / r.width  - 0.5) * 7;
      const y  = ((e.clientY - r.top)  / r.height - 0.5) * 7;
      card.style.transform = `perspective(700px) rotateX(${-y}deg) rotateY(${x}deg) translateZ(4px)`;
    });
    card.addEventListener('mouseleave', () => { card.style.transform = ''; });
  });
}

// ── Auto-dismiss alerts ──────────────────────────────────────
function initAlerts() {
  document.querySelectorAll('.alert-dismissible').forEach(alert => {
    setTimeout(() => {
      try {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
      } catch (_) {}
    }, 5500);
  });
}

// ── Smooth page transitions ───────────────────────────────────
function initTransitions() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.18s ease';

  window.addEventListener('pageshow', () => {
    document.body.style.opacity = '1';
  });

  document.querySelectorAll('a[href]').forEach(link => {
    if (
      !link.href.startsWith(window.location.origin) ||
      link.href.includes('#') ||
      link.target ||
      link.hasAttribute('data-no-transition')
    ) return;
    link.addEventListener('click', () => {
      document.body.style.opacity = '0';
    });
  });
}

// ── Lazy images ───────────────────────────────────────────────
function initLazyImages() {
  // Native lazy loading is set in HTML; this is a fallback polyfill
  if ('loading' in HTMLImageElement.prototype) return;
  const imgs = document.querySelectorAll('img[loading="lazy"]');
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const img = e.target;
        if (img.dataset.src) img.src = img.dataset.src;
        io.unobserve(img);
      }
    });
  });
  imgs.forEach(i => io.observe(i));
}

// ── Init on DOM ready ─────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initSkillBars();
  initCounters();
  initTilt();
  initAlerts();
  initLazyImages();
  if (typeof AOS !== 'undefined') initAOS();
  initTransitions();
});
