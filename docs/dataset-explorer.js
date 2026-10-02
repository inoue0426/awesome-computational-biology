(function () {
  'use strict';

  var DATA_URL = 'data/resources.json';
  var rows = [];
  var sortKey = 'name';
  var sortDirection = 'asc';

  var search = document.getElementById('dataset-search');
  var sampleType = document.getElementById('sample-type');
  var readout = document.getElementById('readout');
  var clinicalOutcome = document.getElementById('clinical-outcome');
  var prePost = document.getElementById('pre-post');
  var smiles = document.getElementById('smiles');
  var clear = document.getElementById('dataset-clear');
  var body = document.getElementById('dataset-body');
  var count = document.getElementById('dataset-count');
  var headers = Array.prototype.slice.call(document.querySelectorAll('th[data-sort-key]'));

  fetch(DATA_URL)
    .then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    })
    .then(function (data) {
      rows = (Array.isArray(data) ? data : []).filter(function (r) {
        return r.dataset_profile && typeof r.dataset_profile === 'object';
      });
      populateSelect(sampleType, 'sample_type');
      populateSelect(readout, 'readout');
      bindSorting();
      render();
    })
    .catch(function (err) {
      count.textContent = 'Failed to load dataset metadata.';
      body.innerHTML = '<tr><td colspan="16">Could not load resources.json: ' + escapeHtml(err.message) + '</td></tr>';
    });

  function populateSelect(select, field) {
    var values = {};
    rows.forEach(function (r) {
      var value = r.dataset_profile[field];
      if (value) values[value] = true;
    });
    Object.keys(values).sort().forEach(function (value) {
      var option = document.createElement('option');
      option.value = value;
      option.textContent = humanize(value);
      select.appendChild(option);
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
      sortDirection = 'asc';
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
      var p = r.dataset_profile || {};
      if (sampleType.value && p.sample_type !== sampleType.value) return false;
      if (readout.value && p.readout !== readout.value) return false;
      if (clinicalOutcome.value && String(Boolean(p.clinical_outcome)) !== clinicalOutcome.value) return false;
      if (prePost.value && String(Boolean(p.pre_post)) !== prePost.value) return false;
      if (smiles.value && String(p.smiles) !== smiles.value) return false;
      if (query) {
        var haystack = [
          r.name, r.description, p.sample_type, p.biological_context, p.readout,
          (p.perturbation_type || []).join(' '), p.n_samples, p.gene_panel, p.access
        ].join(' ').toLowerCase();
        if (haystack.indexOf(query) === -1) return false;
      }
      return true;
    });

    filtered.sort(compareRows);

    count.textContent = filtered.length + ' curated dataset profile' + (filtered.length === 1 ? '' : 's');
    body.innerHTML = '';
    if (!filtered.length) {
      body.innerHTML = '<tr><td colspan="16" class="empty-state">No datasets match these filters.</td></tr>';
      return;
    }

    filtered.forEach(function (r) {
      var p = r.dataset_profile;
      var tr = document.createElement('tr');
      tr.innerHTML =
        '<td class="dataset-name"><a href="' + escapeAttr(r.url || '#') + '" target="_blank" rel="noopener noreferrer">' + escapeHtml(r.name) + '</a></td>' +
        '<td>' + escapeHtml(humanize(p.sample_type)) + '</td>' +
        '<td>' + escapeHtml(humanize(p.biological_context)) + '</td>' +
        '<td>' + escapeHtml(humanize(p.readout)) + '</td>' +
        '<td>' + escapeHtml((p.perturbation_type || []).map(humanize).join(', ') || '—') + '</td>' +
        '<td class="num">' + displayNumber(p.n_profiles) + '</td>' +
        '<td class="num">' + displayNumber(p.n_compounds) + '</td>' +
        '<td class="num">' + displayNumber(p.n_contexts) + '</td>' +
        '<td>' + escapeHtml(p.gene_panel || '—') + '</td>' +
        '<td>' + boolMark(p.paired) + '</td>' +
        '<td>' + boolMark(p.pre_post) + '</td>' +
        '<td>' + boolMark(p.dose) + '</td>' +
        '<td>' + boolMark(p.time) + '</td>' +
        '<td>' + stateMark(p.smiles) + '</td>' +
        '<td>' + boolMark(p.clinical_outcome) + '</td>' +
        '<td>' + escapeHtml(humanize(p.access)) + '</td>';
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
    var p = row.dataset_profile || {};
    var value = key === 'name' ? row.name : p[key];
    if (Array.isArray(value)) value = value.join(', ');
    if (value === null || value === undefined || value === '') return { missing: true, value: '' };

    if (typeof value === 'boolean') return { missing: false, value: value ? 2 : 0 };
    if (value === 'partial' || value === 'limited') return { missing: false, value: 1 };
    if (typeof value === 'number') return { missing: false, value: value };

    if (key === 'n_profiles' || key === 'n_compounds' || key === 'n_contexts' || key === 'n_cells') {
      var numeric = parseNumeric(value);
      return { missing: numeric === null, value: numeric === null ? 0 : numeric };
    }
    return { missing: false, value: String(value).toLowerCase() };
  }

  function parseNumeric(value) {
    if (typeof value === 'number') return value;
    var text = String(value).replace(/,/g, '');
    var match = text.match(/(?:>|~)?\s*(\d+(?:\.\d+)?)(?:\s*(million|m|k))?/i);
    if (!match) return null;
    var n = Number(match[1]);
    var suffix = (match[2] || '').toLowerCase();
    if (suffix === 'million' || suffix === 'm') n *= 1000000;
    if (suffix === 'k') n *= 1000;
    return n;
  }

  function displayNumber(value) {
    if (value === null || value === undefined || value === '') return '—';
    if (typeof value === 'number') return value.toLocaleString();
    return escapeHtml(value);
  }

  function boolMark(value) {
    return value ? '<span class="yes">✓ Yes</span>' : '<span class="no">—</span>';
  }

  function stateMark(value) {
    if (value === true || value === 'true') return '<span class="yes">✓ Yes</span>';
    if (value === 'partial' || value === 'limited') return '<span class="partial">◐ ' + escapeHtml(humanize(value)) + '</span>';
    return '<span class="no">—</span>';
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

  [search, sampleType, readout, clinicalOutcome, prePost, smiles].forEach(function (el) {
    el.addEventListener(el === search ? 'input' : 'change', render);
  });

  clear.addEventListener('click', function () {
    search.value = '';
    sampleType.value = '';
    readout.value = '';
    clinicalOutcome.value = '';
    prePost.value = '';
    smiles.value = '';
    sortKey = 'name';
    sortDirection = 'asc';
    updateSortIndicators();
    render();
  });
})();
