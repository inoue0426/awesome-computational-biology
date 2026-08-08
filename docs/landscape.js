const DATA_URL = "data/resources.json";

const state = {
  resources: [],
  query: "",
  type: "",
  task: "",
  modality: "",
  organism: "",
  tag: "",
  entity: "",
  method: "",
  organization: "",
  year: "",
  maintenance: "",
  enrichedOnly: false,
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
  entity: document.querySelector("#entity-filter"),
  method: document.querySelector("#method-filter"),
  organization: document.querySelector("#organization-filter"),
  year: document.querySelector("#year-filter"),
  maintenance: document.querySelector("#maintenance-filter"),
  enrichedOnly: document.querySelector("#enriched-only"),
  sort: document.querySelector("#sort"),
  results: document.querySelector("#results"),
  count: document.querySelector("#result-count"),
  active: document.querySelector("#active-filters"),
  bars: document.querySelector("#facet-bars"),
  statResources: document.querySelector("#stat-resources"),
  statEnriched: document.querySelector("#stat-enriched"),
  statCoverage: document.querySelector("#stat-coverage"),
  statEntities: document.querySelector("#stat-entities"),
  statMethods: document.querySelector("#stat-methods"),
  statProvenance: document.querySelector("#stat-provenance"),
};

const arr = value => Array.isArray(value) ? value.filter(Boolean) : [];
const norm = value => String(value || "").trim().toLowerCase();
const uniqSorted = values => [...new Set(values.filter(Boolean))].sort((a, b) => String(a).localeCompare(String(b)));
const ENRICHMENT_FIELDS = [
  "entities", "methods", "organizations", "github", "documentation", "year",
  "access", "maintenance_status", "last_checked", "metadata_sources",
];

function collect(field) {
  return uniqSorted(state.resources.flatMap(resource => arr(resource[field])));
}

function collectScalar(field) {
  return uniqSorted(state.resources.map(resource => resource[field]));
}

function populate(select, values, formatter = value => value) {
  if (!select) return;
  const first = select.firstElementChild;
  select.replaceChildren(first);
  for (const value of values) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = formatter(value);
    select.append(option);
  }
}

function isEnriched(resource) {
  return ENRICHMENT_FIELDS.some(field => {
    const value = resource[field];
    return Array.isArray(value) ? value.length > 0 : value !== undefined && value !== null && value !== "";
  });
}

function hasProvenance(resource) {
  return arr(resource.metadata_sources).length > 0 || Boolean(resource.paper);
}

function searchableText(resource) {
  return [
    resource.name,
    resource.description,
    resource.type,
    resource.year,
    resource.maintenance_status,
    ...arr(resource.tasks),
    ...arr(resource.modalities),
    ...arr(resource.organism),
    ...arr(resource.tags),
    ...arr(resource.entities),
    ...arr(resource.methods),
    ...arr(resource.organizations),
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
    if (state.enrichedOnly && !isEnriched(resource)) return false;
    if (state.type && resource.type !== state.type) return false;
    if (!includesFacet(resource, "tasks", state.task)) return false;
    if (!includesFacet(resource, "modalities", state.modality)) return false;
    if (!includesFacet(resource, "organism", state.organism)) return false;
    if (!includesFacet(resource, "tags", state.tag)) return false;
    if (!includesFacet(resource, "entities", state.entity)) return false;
    if (!includesFacet(resource, "methods", state.method)) return false;
    if (!includesFacet(resource, "organizations", state.organization)) return false;
    if (state.year && String(resource.year || "") !== state.year) return false;
    if (state.maintenance && resource.maintenance_status !== state.maintenance) return false;
    return true;
  }).sort((a, b) => {
    if (state.sort === "type") {
      return String(a.type).localeCompare(String(b.type)) || String(a.name).localeCompare(String(b.name));
    }
    if (state.sort === "year") {
      return Number(b.year || 0) - Number(a.year || 0) || String(a.name).localeCompare(String(b.name));
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

function externalLink(label, href) {
  const link = document.createElement("a");
  link.href = href;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.textContent = `${label} ↗`;
  return link;
}

function renderCard(resource) {
  const card = document.createElement("article");
  card.className = `resource-card${isEnriched(resource) ? " enriched-card" : ""}`;

  const top = document.createElement("div");
  top.className = "card-top";
  const title = document.createElement("h3");
  const link = externalLink(resource.name, resource.url);
  link.textContent = resource.name;
  title.append(link);
  const topBadges = document.createElement("div");
  topBadges.className = "top-badges";
  topBadges.append(badge(resource.type || "resource", "type-badge"));
  if (isEnriched(resource)) topBadges.append(badge("enriched", "enriched-badge"));
  top.append(title, topBadges);

  const description = document.createElement("p");
  description.className = "description";
  description.textContent = resource.description || "No description available.";

  const metadata = document.createElement("div");
  metadata.className = "metadata";
  for (const item of arr(resource.entities).slice(0, 3)) metadata.append(badge(item, "entity-badge"));
  for (const item of arr(resource.methods).slice(0, 3)) metadata.append(badge(item, "method-badge"));
  for (const item of arr(resource.tasks).slice(0, 3)) metadata.append(badge(item));
  for (const item of arr(resource.modalities).slice(0, 2)) metadata.append(badge(item, "modality-badge"));
  if (!arr(resource.entities).length && !arr(resource.methods).length) {
    for (const item of arr(resource.tags).slice(0, 3)) metadata.append(badge(item, "tag-badge"));
  }

  const facts = document.createElement("div");
  facts.className = "card-facts";
  if (resource.year) facts.append(badge(`Year ${resource.year}`, "year-badge"));
  for (const item of arr(resource.organizations).slice(0, 2)) facts.append(badge(item, "organization-badge"));
  if (resource.maintenance_status) facts.append(badge(resource.maintenance_status, "maintenance-badge"));
  if (resource.last_checked) facts.append(badge(`checked ${resource.last_checked}`, "checked-badge"));

  const links = document.createElement("div");
  links.className = "card-links";
  if (resource.paper) links.append(externalLink("Paper", resource.paper));
  if (resource.github && resource.github !== resource.url) links.append(externalLink("GitHub", resource.github));
  if (resource.documentation) links.append(externalLink("Docs", resource.documentation));
  if (hasProvenance(resource)) links.append(badge("provenance", "provenance-badge"));
  if (resource.api) links.append(badge("API", "api-badge"));
  if (resource.license) links.append(badge(resource.license, "license-badge"));

  card.append(top, description, metadata);
  if (facts.childElementCount) card.append(facts);
  if (links.childElementCount) card.append(links);
  return card;
}

function frequency(field, resources = state.resources) {
  const counts = new Map();
  for (const resource of resources) {
    const values = field === "type" ? [resource.type] : arr(resource[field]);
    for (const value of values.filter(Boolean)) counts.set(value, (counts.get(value) || 0) + 1);
  }
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0])));
}

function renderFacetBars(resources) {
  const groups = [
    ["Entities", "entities"],
    ["Methods", "methods"],
    ["Tasks", "tasks"],
    ["Modalities", "modalities"],
    ["Types", "type"],
  ];
  els.bars.replaceChildren();
  for (const [label, field] of groups) {
    const top = frequency(field, resources).slice(0, 5);
    if (!top.length) continue;
    const section = document.createElement("section");
    section.className = "bar-group";
    const heading = document.createElement("h3");
    heading.textContent = label;
    section.append(heading);
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
  const values = [
    state.type, state.task, state.modality, state.organism, state.tag,
    state.entity, state.method, state.organization, state.year, state.maintenance,
  ].filter(Boolean);
  els.active.replaceChildren();
  if (!state.query && !values.length && !state.enrichedOnly) return;
  const label = document.createElement("span");
  label.textContent = "Active:";
  els.active.append(label);
  if (state.query) els.active.append(badge(`search: ${state.query}`));
  if (state.enrichedOnly) els.active.append(badge("enriched only", "enriched-badge"));
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

function bindSelect(element, key) {
  if (!element) return;
  element.addEventListener("change", event => { state[key] = event.target.value; render(); });
}

function bind() {
  els.search.addEventListener("input", event => { state.query = event.target.value; render(); });
  bindSelect(els.type, "type");
  bindSelect(els.task, "task");
  bindSelect(els.modality, "modality");
  bindSelect(els.organism, "organism");
  bindSelect(els.tag, "tag");
  bindSelect(els.entity, "entity");
  bindSelect(els.method, "method");
  bindSelect(els.organization, "organization");
  bindSelect(els.year, "year");
  bindSelect(els.maintenance, "maintenance");
  bindSelect(els.sort, "sort");
  els.enrichedOnly.addEventListener("change", event => { state.enrichedOnly = event.target.checked; render(); });
  els.clear.addEventListener("click", () => {
    Object.assign(state, {
      query: "", type: "", task: "", modality: "", organism: "", tag: "",
      entity: "", method: "", organization: "", year: "", maintenance: "", enrichedOnly: false,
    });
    els.search.value = "";
    [
      els.type, els.task, els.modality, els.organism, els.tag, els.entity,
      els.method, els.organization, els.year, els.maintenance,
    ].forEach(select => { if (select) select.value = ""; });
    els.enrichedOnly.checked = false;
    render();
  });
}

function renderSummary() {
  const enriched = state.resources.filter(isEnriched);
  const provenance = enriched.filter(hasProvenance);
  const coverage = state.resources.length ? (enriched.length / state.resources.length) * 100 : 0;
  els.statResources.textContent = state.resources.length.toLocaleString();
  els.statEnriched.textContent = enriched.length.toLocaleString();
  els.statCoverage.textContent = `${coverage.toFixed(1)}%`;
  els.statEntities.textContent = collect("entities").length.toLocaleString();
  els.statMethods.textContent = collect("methods").length.toLocaleString();
  els.statProvenance.textContent = enriched.length ? `${Math.round((provenance.length / enriched.length) * 100)}%` : "0%";
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
    populate(els.entity, collect("entities"));
    populate(els.method, collect("methods"));
    populate(els.organization, collect("organizations"));
    populate(els.year, collectScalar("year").sort((a, b) => Number(b) - Number(a)));
    populate(els.maintenance, collectScalar("maintenance_status"));
    renderSummary();
    bind();
    render();
  } catch (error) {
    els.count.textContent = "Could not load landscape data.";
    els.results.textContent = `Data load failed: ${error.message}`;
  }
}

init();
