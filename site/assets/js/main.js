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

// Gallery lightbox: previous / next, keyboard arrows, swipe, captions
(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox]'));
  if (!links.length || typeof HTMLDialogElement !== 'function') return;
  var dlg = document.createElement('dialog');
  dlg.className = 'lightbox';
  dlg.setAttribute('aria-label', 'Photo viewer');
  dlg.innerHTML = '<button type="button" class="lb-close" aria-label="Close">×</button>' +
    '<button type="button" class="lb-prev" aria-label="Previous photo">‹</button>' +
    '<figure><img alt=""><figcaption></figcaption></figure>' +
    '<button type="button" class="lb-next" aria-label="Next photo">›</button>';
  document.body.appendChild(dlg);
  var img = dlg.querySelector('img'), cap = dlg.querySelector('figcaption');
  var group = [], index = 0;
  function show(i) {
    index = (i + group.length) % group.length;
    var a = group[index], t = a.querySelector('img');
    img.src = a.getAttribute('href');
    img.alt = t ? t.alt : '';
    var text = a.getAttribute('data-caption') || '';
    cap.textContent = (text ? text + '  ·  ' : '') + (index + 1) + ' / ' + group.length;
    dlg.classList.toggle('single', group.length < 2);
  }
  links.forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var key = a.getAttribute('data-lightbox') || '';
      group = links.filter(function (l) { return (l.getAttribute('data-lightbox') || '') === key && l.offsetParent !== null; });
      if (group.indexOf(a) < 0) group = [a];
      show(group.indexOf(a));
      dlg.showModal();
    });
  });
  dlg.querySelector('.lb-close').addEventListener('click', function () { dlg.close(); });
  dlg.querySelector('.lb-prev').addEventListener('click', function () { show(index - 1); });
  dlg.querySelector('.lb-next').addEventListener('click', function () { show(index + 1); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg || e.target.tagName === 'FIGURE') dlg.close(); });
  dlg.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') show(index - 1);
    if (e.key === 'ArrowRight') show(index + 1);
  });
  var x0 = null;
  dlg.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  dlg.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) show(index + (dx < 0 ? 1 : -1));
    x0 = null;
  });
})();

// Gallery album filter
(function () {
  var chips = document.querySelectorAll('.chip[data-gal]');
  if (!chips.length) return;
  var albums = document.querySelectorAll('.album[data-cat]');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var f = chip.getAttribute('data-gal');
      chips.forEach(function (c) { c.classList.toggle('is-active', c === chip); c.setAttribute('aria-pressed', c === chip); });
      albums.forEach(function (a) { a.hidden = !(f === 'all' || a.getAttribute('data-cat') === f); });
    });
  });
})();

// Home hero: typewriter rotator + background video (larger screens only, saves mobile data)
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var rot = document.querySelector('.rotator[data-rotate]');
  if (rot && !reduce) {
    var phrases; try { phrases = JSON.parse(rot.getAttribute('data-rotate')); } catch (e) { phrases = []; }
    var out = rot.querySelector('.rot-text');
    if (phrases.length > 1 && out) {
      var i = 0, pos = phrases[0].length, deleting = false;
      var tick = function () {
        var word = phrases[i];
        if (!deleting) {
          pos++;
          out.textContent = word.slice(0, pos);
          if (pos >= word.length) { deleting = true; return setTimeout(tick, 2600); }
          return setTimeout(tick, 55);
        }
        pos--;
        out.textContent = word.slice(0, Math.max(pos, 0));
        if (pos <= 0) { deleting = false; i = (i + 1) % phrases.length; return setTimeout(tick, 350); }
        setTimeout(tick, 28);
      };
      pos = phrases[0].length; deleting = true;
      setTimeout(tick, 3400);
    }
  }

  var video = document.querySelector('.hero-bg-video[data-sources]');
  if (video) {
    var conn = navigator.connection || {};
    var bigScreen = window.matchMedia('(min-width: 768px)').matches;
    if (bigScreen && !conn.saveData && !reduce) {
      try {
        JSON.parse(video.getAttribute('data-sources')).forEach(function (s) {
          var el = document.createElement('source'); el.src = s.src; el.type = s.type; video.appendChild(el);
        });
        video.load();
        video.addEventListener('playing', function () { video.classList.add('is-playing'); });
        var p = video.play(); if (p && p.catch) p.catch(function () {});
      } catch (e) {}
    }
  }
})();
