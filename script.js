/* Sundus Afreen — Portfolio interactions */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------- Mobile nav ---------------- */
  var navToggle = document.querySelector('.nav-toggle');
  var navLinks = document.querySelector('.nav-links');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      var open = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', String(!open));
      navLinks.classList.toggle('open', !open);
    });
    navLinks.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        navToggle.setAttribute('aria-expanded', 'false');
        navLinks.classList.remove('open');
      });
    });
  }

  /* ---------------- Active nav + thread rail ---------------- */
  var sections = Array.prototype.slice.call(document.querySelectorAll('main > section[id]'));
  var navAnchors = Array.prototype.slice.call(document.querySelectorAll('.nav-links a[href^="#"]'));
  var railFill = document.querySelector('#thread-rail .fill');
  var railNodes = Array.prototype.slice.call(document.querySelectorAll('#thread-rail .node'));

  function positionRailNodes() {
    var docH = document.documentElement.scrollHeight - window.innerHeight;
    if (docH <= 0) return;
    railNodes.forEach(function (n) {
      var sec = document.getElementById(n.dataset.section);
      if (!sec) return;
      var pct = Math.min(98, Math.max(0, (sec.offsetTop / docH) * 100));
      n.style.top = pct + '%';
    });
  }
  positionRailNodes();
  window.addEventListener('resize', positionRailNodes);
  window.addEventListener('load', positionRailNodes);

  function onScroll() {
    var scrollY = window.scrollY;
    var docH = document.documentElement.scrollHeight - window.innerHeight;
    var pct = docH > 0 ? Math.min(100, Math.max(0, (scrollY / docH) * 100)) : 0;
    if (railFill) railFill.style.height = pct + '%';

    var viewMid = scrollY + window.innerHeight * 0.35;
    var current = null;
    sections.forEach(function (sec) {
      if (sec.offsetTop <= viewMid) current = sec;
    });
    if (current) {
      var id = current.id;
      navAnchors.forEach(function (a) {
        a.classList.toggle('active', a.getAttribute('href') === '#' + id);
      });
      railNodes.forEach(function (n) {
        n.classList.toggle('lit', n.dataset.section === id);
      });
    }
  }
  document.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------------- Reveal on scroll ---------------- */
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------------- Hero word rotator ---------------- */
  var rotatorWords = ['business problems.', 'data.', 'systems.', 'people.', 'ideas.'];
  var rotatorEl = document.getElementById('rotator');
  if (rotatorEl) {
    rotatorEl.innerHTML = rotatorWords.map(function (w, i) {
      return '<span' + (i === 0 ? ' class="show"' : '') + '>' + w + '</span>';
    }).join('');
    if (!reduceMotion) {
      var idx = 0;
      var spans = rotatorEl.querySelectorAll('span');
      setInterval(function () {
        spans[idx].classList.remove('show');
        idx = (idx + 1) % spans.length;
        spans[idx].classList.add('show');
      }, 2200);
    }
  }

  /* ---------------- Hero cursor chain ---------------- */
  var hero = document.getElementById('hero');
  var chain = document.querySelector('.chain');
  if (hero && chain) {
    var chainNodes = Array.prototype.slice.call(chain.querySelectorAll('.node'));
    var litUpTo = -1;
    function lightChain(x, width) {
      var ratio = Math.min(1, Math.max(0, x / width));
      var target = Math.floor(ratio * chainNodes.length);
      if (target === litUpTo) return;
      litUpTo = target;
      chainNodes.forEach(function (n, i) { n.classList.toggle('on', i <= target); });
    }
    hero.addEventListener('mousemove', function (e) {
      var rect = hero.getBoundingClientRect();
      lightChain(e.clientX - rect.left, rect.width);
    });
    hero.addEventListener('mouseleave', function () {
      litUpTo = -1;
      chainNodes.forEach(function (n) { n.classList.remove('on'); });
    });
    hero.addEventListener('touchstart', function () {
      chainNodes.forEach(function (n) { n.classList.add('on'); });
    }, { passive: true });
  }

  /* ---------------- Timeline accordion ---------------- */
  document.querySelectorAll('.tl-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.tl-item');
      var isOpen = item.getAttribute('data-open') === 'true';
      document.querySelectorAll('.tl-item').forEach(function (i) { i.setAttribute('data-open', 'false'); });
      document.querySelectorAll('.tl-toggle').forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
      if (!isOpen) {
        item.setAttribute('data-open', 'true');
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });

  /* ---------------- Think steps ---------------- */
  document.querySelectorAll('.think-step').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var targetId = btn.getAttribute('aria-controls');
      var panel = document.getElementById(targetId);
      var isOpen = btn.getAttribute('aria-expanded') === 'true';
      document.querySelectorAll('.think-step').forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
      document.querySelectorAll('.think-detail').forEach(function (p) { p.classList.remove('open'); });
      if (!isOpen) {
        btn.setAttribute('aria-expanded', 'true');
        panel.classList.add('open');
      }
    });
  });

  /* ---------------- Chaos -> Clarity ---------------- */
  var chaosStage = document.querySelector('.chaos-stage');
  var chaosBtn = document.querySelector('.chaos-btn');
  var chaosWordsData = ['Revenue', 'Churn', 'Customers', 'Complaints', 'Cost', 'Growth', 'Data', 'Process', 'People'];
  var chaosAssign = { 'Complaints': 0, 'Customers': 0, 'Churn': 1, 'Data': 1, 'Cost': 2, 'Process': 2, 'Revenue': 3, 'Growth': 3, 'People': 4 };
  // columns: 0 Question 1 Data 2 Pattern 3 Insight 4 Decision
  if (chaosStage) {
    var wordEls = [];
    chaosWordsData.forEach(function (w) {
      var el = document.createElement('span');
      el.className = 'chaos-word';
      el.textContent = w;
      chaosStage.querySelector('.chaos-words').appendChild(el);
      wordEls.push(el);
    });
    function scatter() {
      wordEls.forEach(function (el) {
        el.style.left = (Math.random() * 72) + '%';
        el.style.top = (Math.random() * 78) + '%';
      });
    }
    function sort() {
      var counts = [0, 0, 0, 0, 0];
      wordEls.forEach(function (el) {
        var col = chaosAssign[el.textContent];
        var row = counts[col]++;
        el.style.left = (col * 20 + 2) + '%';
        el.style.top = (20 + row * 46) + '%';
      });
    }
    scatter();
    chaosStage.classList.remove('sorted');
    if (chaosBtn) {
      chaosBtn.addEventListener('click', function () {
        var sorted = chaosStage.classList.toggle('sorted');
        chaosBtn.setAttribute('aria-pressed', String(sorted));
        chaosBtn.textContent = sorted ? 'Scatter it again ↺' : 'Make sense of it →';
        if (sorted) { sort(); } else { scatter(); }
      });
    }
    window.addEventListener('resize', function () {
      if (chaosStage.classList.contains('sorted')) sort(); else scatter();
    });
  }

  /* ---------------- Number count-up (proof section) ---------------- */
  var counters = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window && counters.length) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        cio.unobserve(entry.target);
        var el = entry.target;
        var end = parseFloat(el.dataset.count);
        var suffix = el.dataset.suffix || '';
        var prefix = el.dataset.prefix || '';
        var decimals = el.dataset.decimals ? parseInt(el.dataset.decimals, 10) : 0;
        if (reduceMotion) {
          el.textContent = prefix + end.toFixed(decimals) + suffix;
          return;
        }
        var start = 0;
        var duration = 1100;
        var t0 = performance.now();
        function tick(now) {
          var p = Math.min(1, (now - t0) / duration);
          var eased = 1 - Math.pow(1 - p, 3);
          var val = start + (end - start) * eased;
          el.textContent = prefix + val.toFixed(decimals) + suffix;
          if (p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { cio.observe(el); });
  }

  /* ---------------- Project case-study modal ---------------- */
  var PROJECTS = window.PROJECTS || [];
  var modalOverlay = document.getElementById('modal-overlay');
  var modalBody = document.getElementById('modal-body');
  var lastFocused = null;

  function typeLabel(p) {
    if (p.typeLabelOverride) return p.typeLabelOverride;
    return {
      professional: 'Professional Experience · Schneider Electric',
      academic: 'Academic Project · Trinity College Dublin',
      personal: 'Personal Project',
      simulated: 'Strategic Case Study · Simulated / Projected'
    }[p.type] || p.type;
  }

  function renderModal(p) {
    var techId = 'tech-' + p.id;
    var html = '';
    html += '<div class="modal-kicker">';
    html += '<span class="work-type ' + p.type + '">' + typeLabel(p) + '</span>';
    html += '<span class="work-cat">' + p.category + '</span>';
    html += '</div>';
    html += '<h2 id="modal-heading">“' + p.question + '”</h2>';
    html += '<p class="modal-subtitle">' + p.title + '</p>';

    if (p.approach && p.approach.length) {
      html += '<div class="cs-block"><div class="lbl">The Approach</div><div class="cs-flow">' +
        p.approach.map(function (s, i) {
          return '<span class="step">' + s + '</span>' + (i < p.approach.length - 1 ? '<span class="arrow">→</span>' : '');
        }).join('') + '</div></div>';
    }

    if (p.data) {
      html += '<div class="cs-block"><div class="lbl">The Data</div><p>' + p.data + '</p></div>';
    }

    if (p.insight && p.insight.length) {
      html += '<div class="cs-block"><div class="lbl">The Insight</div><ul class="cs-findings">' +
        p.insight.map(function (f) { return '<li>' + f + '</li>'; }).join('') + '</ul></div>';
    }

    if (p.impact) {
      html += '<div class="cs-impact"><span class="n">' + p.impact.num + '</span><span class="d">' + p.impact.desc + '</span></div>';
      if (p.impact.projected) html += '<p class="cs-note">Figure is a modelled / projected estimate, not a realised business outcome.</p>';
    }

    if (p.businessValue) {
      html += '<div class="cs-block"><div class="lbl">The Business Value</div><p>' + p.businessValue + '</p></div>';
    }

    if (p.tech && p.tech.length) {
      html += '<button class="cs-tech-toggle" aria-expanded="false" aria-controls="' + techId + '">Tech stack ›</button>';
      html += '<div class="cs-tech-list" id="' + techId + '">' + p.tech.map(function (t) { return '<span>' + t + '</span>'; }).join('') + '</div>';
    }

    html += '<div class="cs-links">';
    if (p.github) {
      html += '<a class="btn btn-primary" href="' + p.github + '" target="_blank" rel="noopener">GitHub repository ↗</a>';
    } else {
      html += '<span class="work-private">' + (p.type === 'professional' ? 'Private · Professional Project, no public repo' : 'Private · Academic Project, no public repo') + '</span>';
    }
    if (p.liveDemo) {
      html += '<a class="btn btn-ghost" href="' + p.liveDemo + '" target="_blank" rel="noopener">Live demo ↗</a>';
    }
    html += '</div>';

    modalBody.innerHTML = html;

    var techToggle = modalBody.querySelector('.cs-tech-toggle');
    var techList = modalBody.querySelector('.cs-tech-list');
    if (techToggle && techList) {
      techToggle.addEventListener('click', function () {
        var open = techToggle.getAttribute('aria-expanded') === 'true';
        techToggle.setAttribute('aria-expanded', String(!open));
        techList.classList.toggle('open', !open);
      });
    }
  }

  function openModal(p) {
    lastFocused = document.activeElement;
    renderModal(p);
    modalOverlay.classList.add('open');
    modalOverlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    var closeBtn = modalOverlay.querySelector('.modal-close');
    if (closeBtn) closeBtn.focus();
  }
  function closeModal() {
    modalOverlay.classList.remove('open');
    modalOverlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (lastFocused) lastFocused.focus();
  }
  if (modalOverlay) {
    modalOverlay.addEventListener('click', function (e) {
      if (e.target === modalOverlay || e.target.closest('.modal-close')) closeModal();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modalOverlay.classList.contains('open')) closeModal();
      if (e.key === 'Tab' && modalOverlay.classList.contains('open')) {
        var focusables = modalOverlay.querySelectorAll('button, a[href]');
        if (!focusables.length) return;
        var first = focusables[0], last = focusables[focusables.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }

  var activeFilter = 'all';

  function renderFilters() {
    var wrap = document.getElementById('work-filters');
    if (!wrap) return;
    var categories = [];
    PROJECTS.forEach(function (p) { if (categories.indexOf(p.category) === -1) categories.push(p.category); });
    var pills = ['all'].concat(categories);
    wrap.innerHTML = pills.map(function (c) {
      var label = c === 'all' ? 'All work' : c;
      return '<button class="filter-pill' + (c === activeFilter ? ' active' : '') + '" data-filter="' + c + '" aria-pressed="' + (c === activeFilter) + '">' + label + '</button>';
    }).join('');
    wrap.querySelectorAll('.filter-pill').forEach(function (btn) {
      btn.addEventListener('click', function () {
        activeFilter = btn.dataset.filter;
        renderFilters();
        renderWorkCards();
      });
    });
  }

  function renderWorkCards() {
    var list = document.getElementById('work-list');
    if (!list) return;
    var visible = activeFilter === 'all' ? PROJECTS : PROJECTS.filter(function (p) { return p.category === activeFilter; });

    list.innerHTML = visible.map(function (p, i) {
      var githubBtn = p.github
        ? '<a class="work-github" href="' + p.github + '" target="_blank" rel="noopener" data-stop>View on GitHub <span aria-hidden="true">↗</span></a>'
        : '<span class="work-private">' + (p.type === 'professional' ? 'Private · Professional Project' : 'Private · Academic Project') + '</span>';
      return '<article class="work-card reveal" data-id="' + p.id + '">' +
        '<div class="work-top">' +
          '<span class="work-number">' + String(i + 1).padStart(2, '0') + ' / ' + String(visible.length).padStart(2, '0') + '</span>' +
          '<span class="work-badges">' +
            '<span class="work-cat">' + p.category + '</span>' +
            '<span class="work-type ' + p.type + '">' + typeLabel(p) + '</span>' +
          '</span>' +
        '</div>' +
        '<div class="work-question">“' + p.question + '”</div>' +
        '<div class="work-title">' + p.title + '</div>' +
        '<div class="work-tags">' + p.tags.map(function (t) { return '<span class="work-tag">' + t + '</span>'; }).join('') + '</div>' +
        '<div class="work-actions">' +
          '<button class="work-cta" data-action="case-study">View case study <span aria-hidden="true">→</span></button>' +
          githubBtn +
        '</div>' +
      '</article>';
    }).join('');

    list.querySelectorAll('.work-card').forEach(function (card) {
      var openThisModal = function () {
        var p = PROJECTS.find(function (x) { return x.id === card.dataset.id; });
        if (p) openModal(p);
      };
      var ctaBtn = card.querySelector('[data-action="case-study"]');
      if (ctaBtn) ctaBtn.addEventListener('click', openThisModal);
      var titleEl = card.querySelector('.work-question');
      if (titleEl) { titleEl.style.cursor = 'pointer'; titleEl.addEventListener('click', openThisModal); }

      if ('IntersectionObserver' in window && !reduceMotion) {
        io.observe(card);
      } else {
        card.classList.add('in');
      }
    });
  }
  renderFilters();
  renderWorkCards();

})();
