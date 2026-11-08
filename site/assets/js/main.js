(function () {
  // Sticky header shadow
  var header = document.querySelector('.site-header');
  var onScroll = function () { header && header.classList.toggle('scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Mobile menu
  var menuBtn = document.querySelector('.menu-btn');
  var nav = document.getElementById('main-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open);
      document.body.style.overflow = open ? 'hidden' : '';
      document.body.classList.toggle('menu-open', open);
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { nav.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; document.body.classList.remove('menu-open'); }
    });
  }

  // Services dropdown (click + hover on desktop)
  var dd = document.querySelector('.nav-dd');
  if (dd) {
    var toggle = dd.querySelector('.dd-toggle');
    var setOpen = function (o) { dd.classList.toggle('open', o); toggle.setAttribute('aria-expanded', o); };
    toggle.addEventListener('click', function (e) { e.stopPropagation(); setOpen(!dd.classList.contains('open')); });
    var desktop = window.matchMedia('(min-width: 961px) and (hover: hover)');
    var t;
    dd.addEventListener('mouseenter', function () { if (desktop.matches) { clearTimeout(t); setOpen(true); } });
    dd.addEventListener('mouseleave', function () { if (desktop.matches) { t = setTimeout(function () { setOpen(false); }, 150); } });
    document.addEventListener('click', function (e) { if (desktop.matches && !dd.contains(e.target)) setOpen(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
  }

  // Reveal on scroll
  var els = document.querySelectorAll('.section .card, .section h2, .why-item, .cta-band');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (el) { if (el.getBoundingClientRect().top < window.innerHeight) return; el.classList.add('reveal'); io.observe(el); });
  }

  // Year
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Quote form -> WhatsApp
  var form = document.getElementById('quote-form');
  if (form) {
    var params = new URLSearchParams(location.search);
    if (params.get('service')) form.service.value = params.get('service');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var err = form.querySelector('.form-error');
      var required = [form.name, form.phone, form.service];
      var ok = true;
      required.forEach(function (f) { var bad = !f.value.trim(); f.classList.toggle('invalid', bad); if (bad) ok = false; });
      err.hidden = ok;
      if (!ok) return;
      var svc = form.service.options[form.service.selectedIndex].text;
      var lines = [
        'Hello Omnitech Systems, I would like a quote.',
        '',
        'Name: ' + form.name.value.trim(),
        'Phone: ' + form.phone.value.trim(),
        form.email.value.trim() ? 'Email: ' + form.email.value.trim() : '',
        form.location.value.trim() ? 'Location: ' + form.location.value.trim() : '',
        'Service: ' + svc,
        form.message.value.trim() ? '\nDetails: ' + form.message.value.trim() : ''
      ].filter(Boolean);
      window.open('https://wa.me/' + form.dataset.wa + '?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
    });
  }
})();

// Blog category filter
(function () {
  var chips = document.querySelectorAll('.chip[data-filter]');
  if (!chips.length) return;
  var cards = document.querySelectorAll('.post-grid .post-card');
  var featured = document.querySelector('.featured-post');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var f = chip.getAttribute('data-filter');
      chips.forEach(function (c) { c.classList.toggle('is-active', c === chip); c.setAttribute('aria-pressed', c === chip); });
      cards.forEach(function (card) { card.hidden = !(f === 'all' || card.getAttribute('data-cat') === f); });
      if (featured) featured.hidden = !(f === 'all' || featured.getAttribute('data-cat') === f);
    });
  });
})();

// Portfolio service filter
(function () {
  var chips = document.querySelectorAll('.chip[data-pf]');
  if (!chips.length) return;
  var cards = document.querySelectorAll('.project-grid .project-card');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var f = chip.getAttribute('data-pf');
      chips.forEach(function (c) { c.classList.toggle('is-active', c === chip); c.setAttribute('aria-pressed', c === chip); });
      cards.forEach(function (card) { card.hidden = !(f === 'all' || (' ' + card.getAttribute('data-svc') + ' ').indexOf(' ' + f + ' ') > -1); });
    });
  });
})();

// Gallery lightbox
(function () {
  var links = document.querySelectorAll('[data-lightbox]');
  if (!links.length || typeof HTMLDialogElement !== 'function') return;
  var dlg = document.createElement('dialog');
  dlg.className = 'lightbox';
  dlg.innerHTML = '<button type="button" aria-label="Close">×</button><img alt="">';
  document.body.appendChild(dlg);
  var img = dlg.querySelector('img');
  dlg.querySelector('button').addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  links.forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      img.src = a.getAttribute('href');
      img.alt = (a.querySelector('img') || {}).alt || '';
      dlg.showModal();
    });
  });
})();
