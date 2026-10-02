(function () {
  'use strict';

  var DATA_URL = 'data/resources.json';
  var rows = [];
  var sortKey = 'name';
  var sortDirection = 'asc';

  var search = document.getElementById('method-search');
  var taskFamily = document.getElementById('task-family');
  var patientTransfer = document.getElementById('patient-transfer');
  var unseenDrug = document.getElementById('unseen-drug');
  var year = document.getElementById('method-year');
  var clear = document.getElementById('method-clear');
  var body = document.getElementById('method-body');
  var count = document.getElementById('method-count');
  var headers = Array.prototype.slice.call(document.querySelectorAll('th[data-sort-key]'));

  fetch(DATA_URL)
    .then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    })
    .then(function (data) {
      rows = (Array.isArray(data) ? data : []).filter(function (r) {
        return r.method_profile && typeof r.method_profile === 'object';
      });
      populateYears();
      bindSorting();
      render();
    })
    .catch(function (err) {
      count.textContent = 'Failed to load method metadata.';
      body.innerHTML = '<tr><td colspan="13">Could not load resources.json: ' + escapeHtml(err.message) + '</td></tr>';
    });

  function populateYears() {
    var values = {};
    rows.forEach(function (r) {
      if (r.method_profile.year) values[r.method_profile.year] = true;
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
    if (sortKey === key) sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    else {
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
      var p = r.method_profile || {};
      if (taskFamily.value && p.task_family !== taskFamily.value) return false;
      if (patientTransfer.value && String(Boolean(p.patient_transfer)) !== patientTransfer.value) return false;
      if (unseenDrug.value && normalizeState(p.unseen_drug) !== unseenDrug.value) return false;
      if (year.value && String(p.year) !== year.value) return false;
      if (query) {
        var haystack = [
          r.name, r.description, p.task_family, p.input, p.drug_representation,
          p.context_representation, p.output
        ].join(' ').toLowerCase();
        if (haystack.indexOf(query) === -1) return false;
      }
      return true;
    });

    filtered.sort(compareRows);
    count.textContent = filtered.length + ' curated method profile' + (filtered.length === 1 ? '' : 's');
    body.innerHTML = '';

    if (!filtered.length) {
      body.innerHTML = '<tr><td colspan="13" class="empty-state">No methods match these filters.</td></tr>';
      return;
    }

    filtered.forEach(function (r) {
      var p = r.method_profile;
      var tr = document.createElement('tr');
      tr.innerHTML =
        '<td class="method-name"><a href="' + escapeAttr(r.url || '#') + '" target="_blank" rel="noopener noreferrer">' + escapeHtml(r.name) + '</a></td>' +
        '<td>' + escapeHtml(humanize(p.task_family)) + '</td>' +
        '<td class="num">' + escapeHtml(p.year || '—') + '</td>' +
        '<td>' + escapeHtml(p.input || '—') + '</td>' +
        '<td>' + escapeHtml(p.drug_representation || '—') + '</td>' +
        '<td>' + escapeHtml(p.context_representation || '—') + '</td>' +
        '<td>' + escapeHtml(p.output || '—') + '</td>' +
        '<td>' + stateMark(p.unseen_drug) + '</td>' +
        '<td>' + stateMark(p.unseen_context) + '</td>' +
        '<td>' + stateMark(p.dose) + '</td>' +
        '<td>' + stateMark(p.time) + '</td>' +
        '<td>' + stateMark(p.patient_transfer) + '</td>' +
        '<td>' + stateMark(p.code) + '</td>';
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
    var p = row.method_profile || {};
    var value = key === 'name' ? row.name : p[key];
    if (value === null || value === undefined || value === '') return { missing: true, value: '' };
    if (key === 'year') return { missing: false, value: Number(value) || 0 };
    if (typeof value === 'boolean') return { missing: false, value: value ? 3 : 0 };
    var state = normalizeState(value);
    if (state === 'yes') return { missing: false, value: 3 };
    if (state === 'limited') return { missing: false, value: 2 };
    if (state === 'no') return { missing: false, value: 0 };
    return { missing: false, value: String(value).toLowerCase() };
  }

  function normalizeState(value) {
    if (value === true || value === 'yes' || value === 'true') return 'yes';
    if (value === 'limited' || value === 'adapted') return 'limited';
    if (value === false || value === 'no' || value === 'false') return 'no';
    return String(value || '').toLowerCase();
  }

  function stateMark(value) {
    var state = normalizeState(value);
    if (state === 'yes') return '<span class="yes">✓ Yes</span>';
    if (state === 'limited') return '<span class="partial">◐ Limited</span>';
    if (state === 'no') return '<span class="no">—</span>';
    return escapeHtml(humanize(value));
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

  [search, taskFamily, patientTransfer, unseenDrug, year].forEach(function (el) {
    el.addEventListener(el === search ? 'input' : 'change', render);
  });

  clear.addEventListener('click', function () {
    search.value = '';
    taskFamily.value = '';
    patientTransfer.value = '';
    unseenDrug.value = '';
    year.value = '';
    sortKey = 'name';
    sortDirection = 'asc';
    updateSortIndicators();
    render();
  });
})();
