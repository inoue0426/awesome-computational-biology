const DATA_URL = "data/resources.json";

const state = {
  resources: [],
  query: "",
  type: "",
  task: "",
  modality: "",
  organism: "",
  tag: "",
  sort: "name",
};

const els = {
  search: document.querySelector("#search"),
  clear: document.querySelector("#clear"),
  type: document.querySelector("#type-filter"),
  task: document.querySelector("#task-filter"),
  modality: document.querySelector("#modality-filter"),
  organism: document.querySelector("#organism-filter"),
  tag: document.querySelector("#tag-filter"),
  sort: document.querySelector("#sort"),
  results: document.querySelector("#results"),
  count: document.querySelector("#result-count"),
  active: document.querySelector("#active-filters"),
  bars: document.querySelector("#facet-bars"),
  statResources: document.querySelector("#stat-resources"),
  statTasks: document.querySelector("#stat-tasks"),
  statModalities: document.querySelector("#stat-modalities"),
  statTags: document.querySelector("#stat-tags"),
};

const arr = value => Array.isArray(value) ? value.filter(Boolean) : [];
const norm = value => String(value || "").trim().toLowerCase();
const uniqSorted = values => [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b));

function collect(field) {
  return uniqSorted(state.resources.flatMap(resource => arr(resource[field])));
}

function populate(select, values) {
  const first = select.firstElementChild;
  select.replaceChildren(first);
  for (const value of values) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    select.append(option);
  }
}

function searchableText(resource) {
  return [
    resource.name,
    resource.description,
    resource.type,
    ...arr(resource.tasks),
    ...arr(resource.modalities),
    ...arr(resource.organism),
    ...arr(resource.tags),
  ].map(norm).join(" ");
}

function includesFacet(resource, field, selected) {
  if (!selected) return true;
  return arr(resource[field]).includes(selected);
}

function filteredResources() {
  const query = norm(state.query);
  return state.resources.filter(resource => {
    if (query && !searchableText(resource).includes(query)) return false;
    if (state.type && resource.type !== state.type) return false;
    if (!includesFacet(resource, "tasks", state.task)) return false;
    if (!includesFacet(resource, "modalities", state.modality)) return false;
    if (!includesFacet(resource, "organism", state.organism)) return false;
    if (!includesFacet(resource, "tags", state.tag)) return false;
    return true;
  }).sort((a, b) => {
    if (state.sort === "type") {
      return String(a.type).localeCompare(String(b.type)) || String(a.name).localeCompare(String(b.name));
    }
    return String(a.name).localeCompare(String(b.name));
  });
}

function badge(label, className = "") {
  const span = document.createElement("span");
  span.className = `badge ${className}`.trim();
  span.textContent = label;
  return span;
}

function renderCard(resource) {
  const card = document.createElement("article");
  card.className = "resource-card";

  const top = document.createElement("div");
  top.className = "card-top";
  const title = document.createElement("h3");
  const link = document.createElement("a");
  link.href = resource.url;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.textContent = resource.name;
  title.append(link);
  top.append(title, badge(resource.type || "resource", "type-badge"));

  const description = document.createElement("p");
  description.className = "description";
  description.textContent = resource.description || "No description available.";

  const metadata = document.createElement("div");
  metadata.className = "metadata";
  for (const item of arr(resource.tasks).slice(0, 3)) metadata.append(badge(item));
  for (const item of arr(resource.modalities).slice(0, 2)) metadata.append(badge(item, "modality-badge"));
  for (const item of arr(resource.tags).slice(0, 3)) metadata.append(badge(item, "tag-badge"));

  const links = document.createElement("div");
  links.className = "card-links";
  if (resource.paper) {
    const paper = document.createElement("a");
    paper.href = resource.paper;
    paper.target = "_blank";
    paper.rel = "noopener noreferrer";
    paper.textContent = "Paper ↗";
    links.append(paper);
  }
  if (resource.api) links.append(badge("API", "api-badge"));
  if (resource.license) links.append(badge(resource.license, "license-badge"));

  card.append(top, description, metadata, links);
  return card;
}

function frequency(field, resources = state.resources) {
  const counts = new Map();
  for (const resource of resources) {
    const values = field === "type" ? [resource.type] : arr(resource[field]);
    for (const value of values.filter(Boolean)) counts.set(value, (counts.get(value) || 0) + 1);
  }
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
}

function renderFacetBars(resources) {
  const groups = [
    ["Tasks", "tasks"],
    ["Modalities", "modalities"],
    ["Types", "type"],
  ];
  els.bars.replaceChildren();
  for (const [label, field] of groups) {
    const section = document.createElement("section");
    section.className = "bar-group";
    const heading = document.createElement("h3");
    heading.textContent = label;
    section.append(heading);
    const top = frequency(field, resources).slice(0, 5);
    const max = Math.max(1, ...top.map(([, count]) => count));
    for (const [name, count] of top) {
      const row = document.createElement("div");
      row.className = "bar-row";
      row.innerHTML = `<div class="bar-label"><span></span><strong></strong></div><div class="bar-track"><div class="bar-fill"></div></div>`;
      row.querySelector("span").textContent = name;
      row.querySelector("strong").textContent = count;
      row.querySelector(".bar-fill").style.width = `${Math.max(5, (count / max) * 100)}%`;
      section.append(row);
    }
    els.bars.append(section);
  }
}

function renderActiveFilters() {
  const values = [state.type, state.task, state.modality, state.organism, state.tag].filter(Boolean);
  els.active.replaceChildren();
  if (!state.query && !values.length) return;
  const label = document.createElement("span");
  label.textContent = "Active:";
  els.active.append(label);
  if (state.query) els.active.append(badge(`search: ${state.query}`));
  values.forEach(value => els.active.append(badge(value)));
}

function render() {
  const resources = filteredResources();
  els.count.textContent = `${resources.length.toLocaleString()} of ${state.resources.length.toLocaleString()} resources`;
  els.results.replaceChildren(...resources.map(renderCard));
  if (!resources.length) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent = "No resources match the current filters.";
    els.results.append(empty);
  }
  renderActiveFilters();
  renderFacetBars(resources);
}

function bind() {
  els.search.addEventListener("input", event => { state.query = event.target.value; render(); });
  els.type.addEventListener("change", event => { state.type = event.target.value; render(); });
  els.task.addEventListener("change", event => { state.task = event.target.value; render(); });
  els.modality.addEventListener("change", event => { state.modality = event.target.value; render(); });
  els.organism.addEventListener("change", event => { state.organism = event.target.value; render(); });
  els.tag.addEventListener("change", event => { state.tag = event.target.value; render(); });
  els.sort.addEventListener("change", event => { state.sort = event.target.value; render(); });
  els.clear.addEventListener("click", () => {
    Object.assign(state, {query: "", type: "", task: "", modality: "", organism: "", tag: ""});
    els.search.value = "";
    [els.type, els.task, els.modality, els.organism, els.tag].forEach(select => { select.value = ""; });
    render();
  });
}

async function init() {
  try {
    const response = await fetch(DATA_URL);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.resources = await response.json();
    populate(els.type, uniqSorted(state.resources.map(resource => resource.type)));
    populate(els.task, collect("tasks"));
    populate(els.modality, collect("modalities"));
    populate(els.organism, collect("organism"));
    populate(els.tag, collect("tags"));
    els.statResources.textContent = state.resources.length.toLocaleString();
    els.statTasks.textContent = collect("tasks").length.toLocaleString();
    els.statModalities.textContent = collect("modalities").length.toLocaleString();
    els.statTags.textContent = collect("tags").length.toLocaleString();
    bind();
    render();
  } catch (error) {
    els.count.textContent = "Could not load landscape data.";
    els.results.textContent = `Data load failed: ${error.message}`;
  }
}

init();
