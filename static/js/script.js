// =============================================================
// PlacePro — Global Frontend Interactions
// =============================================================

document.addEventListener('DOMContentLoaded', function () {

  // ---------- 1. Loading Spinner ----------
  const loader = document.getElementById('pagePreloader');
  if (loader) {
    window.addEventListener('load', function () {
      setTimeout(() => {
        loader.style.opacity = '0';
        setTimeout(() => loader.remove(), 400);
      }, 200);
    });
  }

  // ---------- 2. Scroll Reveal ----------
  const revealEls = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  revealEls.forEach(el => revealObserver.observe(el));

  // ---------- 3. Animated Counters ----------
  const counters = document.querySelectorAll('.counter');
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach(el => counterObserver.observe(el));

  function animateCounter(el) {
    const target = parseInt(el.getAttribute('data-target'), 10) || 0;
    const suffix = el.getAttribute('data-suffix') || '';
    const duration = 1400;
    const start = performance.now();

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const value = Math.floor(progress * target);
      el.textContent = value + suffix;
      if (progress < 1) requestAnimationFrame(tick);
      else el.textContent = target + suffix;
    }
    requestAnimationFrame(tick);
  }

  // ---------- 4. Back To Top Button ----------
  const backToTop = document.getElementById('backToTop');
  if (backToTop) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 400) backToTop.classList.add('show');
      else backToTop.classList.remove('show');
    });
    backToTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ---------- 5. Navbar shrink-on-scroll (subtle) ----------
  const nav = document.querySelector('.navbar-glass');
  if (nav) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 40) {
        nav.style.boxShadow = '0 6px 28px rgba(79, 70, 229, 0.12)';
      } else {
        nav.style.boxShadow = '0 4px 24px rgba(79, 70, 229, 0.06)';
      }
    });
  }

  // ---------- 6. Bootstrap form validation styling ----------
  const forms = document.querySelectorAll('.needs-validation');
  forms.forEach(form => {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    });
  });

  // ---------- 7. Auto-dismiss alerts ----------
  document.querySelectorAll('.alert-auto-dismiss').forEach(alertEl => {
    setTimeout(() => {
      alertEl.classList.remove('show');
      setTimeout(() => alertEl.remove(), 300);
    }, 4500);
  });

});
