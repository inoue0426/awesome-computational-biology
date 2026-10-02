(function () {
  'use strict';

  var DATA_URL = 'data/resources.json';
  var rows = [];
  var sortKey = 'name';
  var sortDirection = 'asc';

  var search = document.getElementById('foundation-search');
  var modality = document.getElementById('fm-modality');
  var recentOnly = document.getElementById('foundation-recent');
  var year = document.getElementById('fm-year');
  var weights = document.getElementById('fm-weights');
  var perturbation = document.getElementById('fm-perturbation');
  var spatial = document.getElementById('fm-spatial');
  var clear = document.getElementById('foundation-clear');
  var body = document.getElementById('foundation-body');
  var count = document.getElementById('foundation-count');
  var headers = Array.prototype.slice.call(document.querySelectorAll('th[data-sort-key]'));

  fetch(DATA_URL)
    .then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    })
    .then(function (data) {
      rows = (Array.isArray(data) ? data : []).filter(function (r) {
        return r.foundation_profile && typeof r.foundation_profile === 'object';
      });
      populateArrayFilter(modality, 'modalities');
      populateYears();
      bindSorting();
      render();
    })
    .catch(function (err) {
      count.textContent = 'Failed to load foundation model metadata.';
      body.innerHTML = '<tr><td colspan="12">Could not load resources.json: ' + escapeHtml(err.message) + '</td></tr>';
    });

  function populateArrayFilter(select, field) {
    var values = {};
    rows.forEach(function (r) {
      var items = r.foundation_profile[field] || [];
      if (!Array.isArray(items)) items = [items];
      items.forEach(function (value) {
        if (value) values[value] = true;
      });
    });
    Object.keys(values).sort().forEach(function (value) {
      var option = document.createElement('option');
      option.value = value;
      option.textContent = modalityLabel(value);
      select.appendChild(option);
    });
  }

  function populateYears() {
    var values = {};
    rows.forEach(function (r) {
      var value = r.foundation_profile.year;
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
      sortDirection = (key === 'year' || key === 'params_millions') ? 'desc' : 'asc';
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
      var p = r.foundation_profile || {};
      if (recentOnly.checked && Number(p.year || 0) < 2025) return false;
      if (modality.value && (p.modalities || []).indexOf(modality.value) === -1) return false;
      if (year.value && String(p.year || '') !== year.value) return false;
      if (weights.value && normalizeState(p.weights) !== weights.value) return false;
      if (perturbation.value && normalizeState(p.perturbation) !== perturbation.value) return false;
      if (spatial.value && normalizeState(p.spatial) !== spatial.value) return false;
      if (query) {
        var haystack = [
          r.name, r.description, (p.modalities || []).join(' '), p.params,
          p.pretraining_scale, (p.species || []).join(' ')
        ].join(' ').toLowerCase();
        if (haystack.indexOf(query) === -1) return false;
      }
      return true;
    });

    filtered.sort(compareRows);
    count.textContent = filtered.length + ' curated foundation model profile' + (filtered.length === 1 ? '' : 's');
    body.innerHTML = '';

    if (!filtered.length) {
      body.innerHTML = '<tr><td colspan="12" class="empty-state">No foundation models match these filters.</td></tr>';
      return;
    }

    filtered.forEach(function (r) {
      var p = r.foundation_profile;
      var tr = document.createElement('tr');
      tr.innerHTML =
        '<td class="foundation-name"><a href="' + escapeAttr(r.url || '#') + '" target="_blank" rel="noopener noreferrer">' + escapeHtml(r.name) + '</a></td>' +
        '<td class="num">' + escapeHtml(p.year || '—') + '</td>' +
        '<td>' + modalityBadges(p.modalities || []) + '</td>' +
        '<td class="num">' + escapeHtml(p.params || '—') + '</td>' +
        '<td class="scale-cell">' + escapeHtml(p.pretraining_scale || '—') + '</td>' +
        '<td>' + escapeHtml((p.species || []).map(humanize).join(', ') || '—') + '</td>' +
        '<td>' + stateMark(p.zero_shot) + '</td>' +
        '<td>' + stateMark(p.finetunable) + '</td>' +
        '<td>' + stateMark(p.weights) + '</td>' +
        '<td>' + stateMark(p.code) + '</td>' +
        '<td>' + stateMark(p.perturbation) + '</td>' +
        '<td>' + stateMark(p.spatial) + '</td>';
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
    var p = row.foundation_profile || {};
    var value = key === 'name' ? row.name : p[key];
    if (Array.isArray(value)) value = value.join(', ');
    if (value === null || value === undefined || value === '') return { missing: true, value: '' };
    if (key === 'year' || key === 'params_millions') return { missing: false, value: Number(value) || 0 };
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

  function modalityBadges(values) {
    if (!values.length) return '—';
    return values.map(function (value) {
      return '<span class="modality-badge">' + escapeHtml(modalityLabel(value)) + '</span>';
    }).join(' ');
  }

  function modalityLabel(value) {
    var labels = {
      'scrna': 'scRNA',
      'bulk-rna': 'Bulk RNA',
      'proteomics': 'Proteomics',
      'mutation': 'Mutation',
      'methylation': 'Methylation',
      'atac': 'ATAC',
      'spatial': 'Spatial',
      'pathology': 'Pathology',
      'dna': 'DNA',
      'rna': 'RNA',
      'chemical': 'Chemical',
      'protein': 'Protein',
      'multi-omics': 'Multi-omics'
    };
    return labels[value] || humanize(value);
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

  [search, modality, year, weights, perturbation, spatial, recentOnly].forEach(function (el) {
    el.addEventListener(el === search ? 'input' : 'change', render);
  });

  clear.addEventListener('click', function () {
    search.value = '';
    modality.value = '';
    recentOnly.checked = false;
    year.value = '';
    weights.value = '';
    perturbation.value = '';
    spatial.value = '';
    sortKey = 'name';
    sortDirection = 'asc';
    updateSortIndicators();
    render();
  });
})();
