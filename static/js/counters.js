/* ============================================================
   Animated Counters — Hero Stats
   ============================================================ */

(function () {
  const counters = document.querySelectorAll('.stat-num[data-target]');
  if (!counters.length) return;

  const animateCounter = (el, target) => {
    let current = 0;
    const increment = Math.ceil(target / 60);
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) { current = target; clearInterval(timer); }
      el.textContent = current;
    }, 28);
  };

  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const target = parseInt(e.target.getAttribute('data-target'), 10);
        animateCounter(e.target, target);
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(c => observer.observe(c));
})();
