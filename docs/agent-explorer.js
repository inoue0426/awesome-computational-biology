(function () {
  'use strict';

  var DATA_URL = 'data/resources.json';
  var rows = [];
  var sortKey = 'name';
  var sortDirection = 'asc';

  var search = document.getElementById('agent-search');
  var domain = document.getElementById('agent-domain');
  var architecture = document.getElementById('agent-architecture');
  var omics = document.getElementById('agent-omics');
  var code = document.getElementById('agent-code');
  var year = document.getElementById('agent-year');
  var clear = document.getElementById('agent-clear');
  var body = document.getElementById('agent-body');
  var count = document.getElementById('agent-count');
  var headers = Array.prototype.slice.call(document.querySelectorAll('th[data-sort-key]'));

  fetch(DATA_URL)
    .then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    })
    .then(function (data) {
      rows = (Array.isArray(data) ? data : []).filter(function (r) {
        return r.agent_profile && typeof r.agent_profile === 'object';
      });
      populateArrayFilter(domain, 'domains');
      populateYears();
      bindSorting();
      render();
    })
    .catch(function (err) {
      count.textContent = 'Failed to load agent metadata.';
      body.innerHTML = '<tr><td colspan="13">Could not load resources.json: ' + escapeHtml(err.message) + '</td></tr>';
    });

  function populateArrayFilter(select, field) {
    var values = {};
    rows.forEach(function (r) {
      var items = r.agent_profile[field] || [];
      if (!Array.isArray(items)) items = [items];
      items.forEach(function (value) {
        if (value) values[value] = true;
      });
    });
    Object.keys(values).sort().forEach(function (value) {
      var option = document.createElement('option');
      option.value = value;
      option.textContent = humanize(value);
      select.appendChild(option);
    });
  }

  function populateYears() {
    var values = {};
    rows.forEach(function (r) {
      var value = r.agent_profile.year;
      if (value) values[value] = true;
    });
    Object.keys(values).sort().reverse().forEach(function (value) {
      var option = document.createElement('option');
      option.value = value;
      option.textContent = value;
      year.appendChild(option);
    });
  }

  function bindSorting() {
    headers.forEach(function (header) {
      header.tabIndex = 0;
      header.setAttribute('role', 'button');
      header.addEventListener('click', function () {
        setSort(header.getAttribute('data-sort-key'));
      });
      header.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          setSort(header.getAttribute('data-sort-key'));
        }
      });
    });
  }

  function setSort(key) {
    if (sortKey === key) {
      sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      sortKey = key;
      sortDirection = key === 'year' ? 'desc' : 'asc';
    }
    updateSortIndicators();
    render();
  }

  function updateSortIndicators() {
    headers.forEach(function (header) {
      var active = header.getAttribute('data-sort-key') === sortKey;
      var indicator = header.querySelector('.sort-indicator');
      header.setAttribute('aria-sort', active ? (sortDirection === 'asc' ? 'ascending' : 'descending') : 'none');
      if (indicator) indicator.textContent = active ? (sortDirection === 'asc' ? '▲' : '▼') : '';
    });
  }

  function render() {
    var query = (search.value || '').trim().toLowerCase();
    var filtered = rows.filter(function (r) {
      var p = r.agent_profile || {};
      if (domain.value && (p.domains || []).indexOf(domain.value) === -1) return false;
      if (architecture.value && p.architecture !== architecture.value) return false;
      if (omics.value && normalizeState(p.omics) !== omics.value) return false;
      if (code.value && normalizeState(p.code_execution) !== code.value) return false;
      if (year.value && String(p.year || '') !== year.value) return false;
      if (query) {
        var haystack = [
          r.name, r.description, (p.domains || []).join(' '), p.architecture
        ].join(' ').toLowerCase();
        if (haystack.indexOf(query) === -1) return false;
      }
      return true;
    });

    filtered.sort(compareRows);
    count.textContent = filtered.length + ' curated agent profile' + (filtered.length === 1 ? '' : 's');
    body.innerHTML = '';

    if (!filtered.length) {
      body.innerHTML = '<tr><td colspan="13" class="empty-state">No agents match these filters.</td></tr>';
      return;
    }

    filtered.forEach(function (r) {
      var p = r.agent_profile;
      var tr = document.createElement('tr');
      tr.innerHTML =
        '<td class="agent-name"><a href="' + escapeAttr(r.url || '#') + '" target="_blank" rel="noopener noreferrer">' + escapeHtml(r.name) + '</a></td>' +
        '<td class="num">' + escapeHtml(p.year || '—') + '</td>' +
        '<td>' + domainBadges(p.domains || []) + '</td>' +
        '<td>' + escapeHtml(humanize(p.architecture)) + '</td>' +
        '<td>' + stateMark(p.tool_use) + '</td>' +
        '<td>' + stateMark(p.code_execution) + '</td>' +
        '<td>' + stateMark(p.web_retrieval) + '</td>' +
        '<td>' + stateMark(p.literature) + '</td>' +
        '<td>' + stateMark(p.omics) + '</td>' +
        '<td>' + stateMark(p.wet_lab) + '</td>' +
        '<td>' + stateMark(p.autonomous_experiment) + '</td>' +
        '<td>' + stateMark(p.human_in_loop) + '</td>' +
        '<td>' + stateMark(p.open_source) + '</td>';
      body.appendChild(tr);
    });
  }

  function compareRows(a, b) {
    var av = sortValue(a, sortKey);
    var bv = sortValue(b, sortKey);
    var direction = sortDirection === 'asc' ? 1 : -1;
    if (av.missing !== bv.missing) return av.missing ? 1 : -1;
    if (av.value < bv.value) return -1 * direction;
    if (av.value > bv.value) return 1 * direction;
    return String(a.name || '').localeCompare(String(b.name || ''));
  }

  function sortValue(row, key) {
    var p = row.agent_profile || {};
    var value = key === 'name' ? row.name : p[key];
    if (Array.isArray(value)) value = value.join(', ');
    if (value === null || value === undefined || value === '') return { missing: true, value: '' };
    if (key === 'year') return { missing: false, value: Number(value) || 0 };
    var state = normalizeState(value);
    if (state === 'yes') return { missing: false, value: 3 };
    if (state === 'limited') return { missing: false, value: 2 };
    if (state === 'unknown') return { missing: false, value: 1 };
    if (state === 'no') return { missing: false, value: 0 };
    return { missing: false, value: String(value).toLowerCase() };
  }

  function normalizeState(value) {
    if (value === true || value === 'yes' || value === 'true') return 'yes';
    if (value === 'limited') return 'limited';
    if (value === 'unknown' || value === null || value === undefined || value === '') return 'unknown';
    if (value === false || value === 'no' || value === 'false') return 'no';
    return String(value).toLowerCase();
  }

  function stateMark(value) {
    var state = normalizeState(value);
    if (state === 'yes') return '<span class="yes">✓ Yes</span>';
    if (state === 'limited') return '<span class="partial">◐ Limited</span>';
    if (state === 'no') return '<span class="no">—</span>';
    return '<span class="unknown">?</span>';
  }

  function domainBadges(values) {
    if (!values.length) return '—';
    return values.map(function (value) {
      return '<span class="domain-badge">' + escapeHtml(humanize(value)) + '</span>';
    }).join(' ');
  }

  function humanize(value) {
    if (value === null || value === undefined || value === '') return '—';
    return String(value).replace(/[-_]/g, ' ').replace(/\b\w/g, function (m) { return m.toUpperCase(); });
  }

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function escapeAttr(value) {
    return escapeHtml(value).replace(/'/g, '&#39;');
  }

  [search, domain, architecture, omics, code, year].forEach(function (el) {
    el.addEventListener(el === search ? 'input' : 'change', render);
  });

  clear.addEventListener('click', function () {
    search.value = '';
    domain.value = '';
    architecture.value = '';
    omics.value = '';
    code.value = '';
    year.value = '';
    sortKey = 'name';
    sortDirection = 'asc';
    updateSortIndicators();
    render();
  });
})();
