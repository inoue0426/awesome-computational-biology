(function () {
  'use strict';

  var DATA_URL = 'data/resources.json';
  var rows = [];
  var search = document.getElementById('dataset-search');
  var sampleType = document.getElementById('sample-type');
  var clinicalOutcome = document.getElementById('clinical-outcome');
  var prePost = document.getElementById('pre-post');
  var smiles = document.getElementById('smiles');
  var clear = document.getElementById('dataset-clear');
  var body = document.getElementById('dataset-body');
  var count = document.getElementById('dataset-count');

  fetch(DATA_URL)
    .then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    })
    .then(function (data) {
      rows = (Array.isArray(data) ? data : []).filter(function (r) {
        return r.dataset_profile && typeof r.dataset_profile === 'object';
      });
      populateSampleTypes();
      render();
    })
    .catch(function (err) {
      count.textContent = 'Failed to load dataset metadata.';
      body.innerHTML = '<tr><td colspan="11">Could not load resources.json: ' + escapeHtml(err.message) + '</td></tr>';
    });

  function populateSampleTypes() {
    var values = {};
    rows.forEach(function (r) {
      var value = r.dataset_profile.sample_type;
      if (value) values[value] = true;
    });
    Object.keys(values).sort().forEach(function (value) {
      var option = document.createElement('option');
      option.value = value;
      option.textContent = humanize(value);
      sampleType.appendChild(option);
    });
  }

  function render() {
    var query = (search.value || '').trim().toLowerCase();
    var filtered = rows.filter(function (r) {
      var p = r.dataset_profile || {};
      if (sampleType.value && p.sample_type !== sampleType.value) return false;
      if (clinicalOutcome.value && String(Boolean(p.clinical_outcome)) !== clinicalOutcome.value) return false;
      if (prePost.value && String(Boolean(p.pre_post)) !== prePost.value) return false;
      if (smiles.value && String(p.smiles) !== smiles.value) return false;
      if (query) {
        var haystack = [
          r.name, r.description, p.sample_type, p.biological_context,
          (p.perturbation_type || []).join(' '), p.n_samples, p.access
        ].join(' ').toLowerCase();
        if (haystack.indexOf(query) === -1) return false;
      }
      return true;
    });

    count.textContent = filtered.length + ' curated dataset profile' + (filtered.length === 1 ? '' : 's');
    body.innerHTML = '';
    if (!filtered.length) {
      body.innerHTML = '<tr><td colspan="11" class="empty-state">No datasets match these filters.</td></tr>';
      return;
    }

    filtered.forEach(function (r) {
      var p = r.dataset_profile;
      var tr = document.createElement('tr');
      tr.innerHTML =
        '<td class="dataset-name"><a href="' + escapeAttr(r.url || '#') + '" target="_blank" rel="noopener noreferrer">' + escapeHtml(r.name) + '</a></td>' +
        '<td>' + escapeHtml(humanize(p.sample_type)) + '</td>' +
        '<td>' + escapeHtml(humanize(p.biological_context)) + '</td>' +
        '<td>' + escapeHtml((p.perturbation_type || []).map(humanize).join(', ') || '—') + '</td>' +
        '<td>' + boolMark(p.paired) + '</td>' +
        '<td>' + boolMark(p.pre_post) + '</td>' +
        '<td>' + boolMark(p.dose) + '</td>' +
        '<td>' + stateMark(p.smiles) + '</td>' +
        '<td>' + boolMark(p.clinical_outcome) + '</td>' +
        '<td>' + escapeHtml(p.n_samples || '—') + '</td>' +
        '<td>' + escapeHtml(humanize(p.access)) + '</td>';
      body.appendChild(tr);
    });
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

  [search, sampleType, clinicalOutcome, prePost, smiles].forEach(function (el) {
    el.addEventListener(el === search ? 'input' : 'change', render);
  });

  clear.addEventListener('click', function () {
    search.value = '';
    sampleType.value = '';
    clinicalOutcome.value = '';
    prePost.value = '';
    smiles.value = '';
    render();
  });
})();
