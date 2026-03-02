/* app.js — no external frameworks */
(function () {
  'use strict';

  const DATA_URL = 'data/resources.json';

  // ── DOM refs ──────────────────────────────────────────────────
  const searchInput    = document.getElementById('search');
  const filterTask     = document.getElementById('filter-task');
  const filterModality = document.getElementById('filter-modality');
  const filterType     = document.getElementById('filter-type');
  const clearBtn       = document.getElementById('clear-btn');
  const resultsEl      = document.getElementById('results');
  const countEl        = document.getElementById('result-count');
  const loadTimeEl     = document.getElementById('load-time');

  let allResources = [];

  // ── Fetch data ────────────────────────────────────────────────
  fetch(DATA_URL)
    .then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    })
    .then(function (data) {
      allResources = Array.isArray(data) ? data : [];
      const ts = new Date().toLocaleString();
      loadTimeEl.textContent = 'Loaded ' + ts;
      populateDropdowns(allResources);
      render();
    })
    .catch(function (err) {
      countEl.textContent = 'Failed to load data.';
      resultsEl.innerHTML =
        '<p class="empty-state">Could not load resources.json: ' +
        escapeHtml(err.message) + '</p>';
    });

  // ── Populate dropdowns ────────────────────────────────────────
  function populateDropdowns(resources) {
    var tasks      = new Set();
    var modalities = new Set();
    var types      = new Set();

    resources.forEach(function (r) {
      if (r.type) types.add(r.type);
      (r.tasks      || []).forEach(function (t) { tasks.add(t); });
      (r.modalities || []).forEach(function (m) { modalities.add(m); });
    });

    appendOptions(filterTask,     Array.from(tasks).sort());
    appendOptions(filterModality, Array.from(modalities).sort());
    appendOptions(filterType,     Array.from(types).sort());
  }

  function appendOptions(select, values) {
    values.forEach(function (v) {
      var opt = document.createElement('option');
      opt.value = v;
      opt.textContent = v;
      select.appendChild(opt);
    });
  }

  // ── Filter & render ───────────────────────────────────────────
  function render() {
    var query    = (searchInput.value    || '').trim().toLowerCase();
    var taskVal  = (filterTask.value     || '').toLowerCase();
    var modalVal = (filterModality.value || '').toLowerCase();
    var typeVal  = (filterType.value     || '').toLowerCase();

    var filtered = allResources.filter(function (r) {
      // Type filter
      if (typeVal && (r.type || '').toLowerCase() !== typeVal) return false;

      // Task filter
      if (taskVal) {
        var tasks = (r.tasks || []).map(function (t) { return t.toLowerCase(); });
        if (!tasks.some(function (t) { return t === taskVal; })) return false;
      }

      // Modality filter
      if (modalVal) {
        var mods = (r.modalities || []).map(function (m) { return m.toLowerCase(); });
        if (!mods.some(function (m) { return m === modalVal; })) return false;
      }

      // Full-text search over name, description, and tags
      if (query) {
        var haystack = [
          r.name        || '',
          r.description || '',
          (r.tasks      || []).join(' '),
          (r.modalities || []).join(' '),
          (r.tags       || []).join(' ')
        ].join(' ').toLowerCase();
        if (haystack.indexOf(query) === -1) return false;
      }

      return true;
    });

    countEl.textContent = filtered.length + ' result' + (filtered.length !== 1 ? 's' : '');

    if (filtered.length === 0) {
      resultsEl.innerHTML = '<p class="empty-state">No resources match your filters. Try broadening your search.</p>';
      return;
    }

    var fragment = document.createDocumentFragment();
    filtered.forEach(function (r) {
      fragment.appendChild(buildCard(r));
    });
    resultsEl.innerHTML = '';
    resultsEl.appendChild(fragment);
  }

  // ── Build a card element ──────────────────────────────────────
  function buildCard(r) {
    var card = document.createElement('article');
    card.className = 'card';

    // Header: name link + type pill
    var header = document.createElement('div');
    header.className = 'card-header';

    var nameLink = document.createElement('a');
    nameLink.className = 'card-name';
    nameLink.href = r.url || '#';
    nameLink.target = '_blank';
    nameLink.rel = 'noopener noreferrer';
    nameLink.textContent = r.name || '(unnamed)';
    header.appendChild(nameLink);

    if (r.type) {
      var typePill = document.createElement('span');
      var typeClass = 'type-' + (r.type || '').toLowerCase().replace(/[^a-z]/g, '');
      typePill.className = 'card-type ' + typeClass;
      typePill.textContent = r.type;
      header.appendChild(typePill);
    }
    card.appendChild(header);

    // Description
    if (r.description) {
      var desc = document.createElement('p');
      desc.className = 'card-description';
      desc.textContent = r.description;
      card.appendChild(desc);
    }

    // Badges: tasks, modalities, tags
    var badges = buildBadges(r);
    if (badges.childElementCount > 0) card.appendChild(badges);

    // Paper link
    if (r.paper) {
      var paperDiv = document.createElement('div');
      paperDiv.className = 'card-paper';
      var paperLink = document.createElement('a');
      paperLink.href = r.paper;
      paperLink.target = '_blank';
      paperLink.rel = 'noopener noreferrer';
      paperLink.textContent = '📄 Paper';
      paperDiv.appendChild(paperLink);
      card.appendChild(paperDiv);
    }

    return card;
  }

  function buildBadges(r) {
    var wrap = document.createElement('div');
    wrap.className = 'card-badges';

    (r.tasks || []).forEach(function (t) {
      wrap.appendChild(makeBadge(t, 'badge-task'));
    });
    (r.modalities || []).forEach(function (m) {
      wrap.appendChild(makeBadge(m, 'badge-modality'));
    });
    (r.tags || []).forEach(function (tag) {
      wrap.appendChild(makeBadge(tag, 'badge-tag'));
    });

    return wrap;
  }

  function makeBadge(text, cls) {
    var span = document.createElement('span');
    span.className = 'badge ' + cls;
    span.textContent = text;
    return span;
  }

  // ── Event listeners ───────────────────────────────────────────
  searchInput.addEventListener('input', render);
  filterTask.addEventListener('change', render);
  filterModality.addEventListener('change', render);
  filterType.addEventListener('change', render);

  clearBtn.addEventListener('click', function () {
    searchInput.value    = '';
    filterTask.value     = '';
    filterModality.value = '';
    filterType.value     = '';
    render();
  });

  // ── Utility ───────────────────────────────────────────────────
  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
})();
