(function () {
  'use strict';

  var allResources = [];

  var searchEl = document.getElementById('search');
  var filterType = document.getElementById('filter-type');
  var filterTask = document.getElementById('filter-task');
  var filterModality = document.getElementById('filter-modality');
  var clearBtn = document.getElementById('clear-filters');
  var resultsEl = document.getElementById('results');
  var countEl = document.getElementById('result-count');
  var timeEl = document.getElementById('loaded-time');

  function toArray(val) {
    if (Array.isArray(val)) return val;
    if (val && typeof val === 'string') return [val];
    return [];
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function populateDropdown(selectEl, values) {
    var sorted = Array.from(values).filter(Boolean).sort();
    sorted.forEach(function (val) {
      var opt = document.createElement('option');
      opt.value = val;
      opt.textContent = val;
      selectEl.appendChild(opt);
    });
  }

  function buildDropdowns(resources) {
    var types = new Set();
    var tasks = new Set();
    var modalities = new Set();

    resources.forEach(function (r) {
      if (r.type) types.add(r.type);
      toArray(r.task).forEach(function (t) { tasks.add(t); });
      toArray(r.modality).forEach(function (m) { modalities.add(m); });
    });

    populateDropdown(filterType, types);
    populateDropdown(filterTask, tasks);
    populateDropdown(filterModality, modalities);
  }

  function filterResources() {
    var query = searchEl.value.toLowerCase().trim();
    var type = filterType.value;
    var task = filterTask.value;
    var modality = filterModality.value;

    return allResources.filter(function (r) {
      if (query) {
        var searchable = [
          r.name || '',
          r.description || '',
          toArray(r.tags).join(' '),
          toArray(r.task).join(' '),
          toArray(r.modality).join(' ')
        ].join(' ').toLowerCase();
        if (searchable.indexOf(query) === -1) return false;
      }
      if (type && r.type !== type) return false;
      if (task && toArray(r.task).indexOf(task) === -1) return false;
      if (modality && toArray(r.modality).indexOf(modality) === -1) return false;
      return true;
    });
  }

  function renderBadges(items, cssClass) {
    return toArray(items).map(function (item) {
      return '<span class="badge ' + cssClass + '">' + escapeHtml(item) + '</span>';
    }).join('');
  }

  function renderCard(r) {
    var name = escapeHtml(r.name || 'Untitled');
    var url = escapeHtml(r.url || '#');
    var description = escapeHtml(r.description || '');
    var typeBadge = r.type
      ? '<span class="badge-type">' + escapeHtml(r.type) + '</span>'
      : '';
    var taskBadges = renderBadges(r.task, 'badge-task');
    var modalityBadges = renderBadges(r.modality, 'badge-modality');
    var tagBadges = renderBadges(r.tags, 'badge');
    var allBadges = taskBadges + modalityBadges + tagBadges;
    var paperHtml = r.paper
      ? '<div class="paper-link">\uD83D\uDCCE <a href="' + escapeHtml(r.paper) + '" target="_blank" rel="noopener noreferrer">Paper</a></div>'
      : '';

    return '<div class="card" role="listitem">'
      + '<div class="card-header">'
      + '<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + name + '</a>'
      + typeBadge
      + '</div>'
      + (description ? '<p class="card-description">' + description + '</p>' : '')
      + (allBadges ? '<div class="badges">' + allBadges + '</div>' : '')
      + paperHtml
      + '</div>';
  }

  function render() {
    var filtered = filterResources();
    var n = filtered.length;
    countEl.textContent = n + ' result' + (n !== 1 ? 's' : '');
    if (n === 0) {
      resultsEl.innerHTML = '<p class="no-results">No resources match your filters.</p>';
    } else {
      resultsEl.innerHTML = filtered.map(renderCard).join('');
    }
  }

  searchEl.addEventListener('input', render);
  filterType.addEventListener('change', render);
  filterTask.addEventListener('change', render);
  filterModality.addEventListener('change', render);

  clearBtn.addEventListener('click', function () {
    searchEl.value = '';
    filterType.value = '';
    filterTask.value = '';
    filterModality.value = '';
    render();
  });

  fetch('data/resources.json')
    .then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    })
    .then(function (data) {
      allResources = Array.isArray(data) ? data : [];
      var now = new Date();
      timeEl.textContent = 'Last loaded: ' + now.toLocaleString();
      buildDropdowns(allResources);
      render();
    })
    .catch(function (err) {
      resultsEl.innerHTML = '<p class="error-msg">Failed to load resources: ' + escapeHtml(err.message) + '</p>';
      countEl.textContent = '0 results';
    });
}());
