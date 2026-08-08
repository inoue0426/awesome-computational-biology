const COVERAGE_DATA_URL = "data/resources.json";
const COVERAGE_ENRICHMENT_FIELDS = [
  "entities", "methods", "organizations", "github", "documentation", "year",
  "access", "maintenance_status", "last_checked", "metadata_sources",
];

function coverageIsEnriched(resource) {
  return COVERAGE_ENRICHMENT_FIELDS.some(field => {
    const value = resource[field];
    return Array.isArray(value) ? value.length > 0 : value !== undefined && value !== null && value !== "";
  });
}

function formatTypeLabel(type) {
  return String(type || "unknown").replace(/(^|-)([a-z])/g, (_, prefix, letter) => `${prefix ? " " : ""}${letter.toUpperCase()}`);
}

async function renderTypeCoverage() {
  const summary = document.querySelector(".stats");
  if (!summary || document.querySelector("#type-coverage")) return;

  const response = await fetch(COVERAGE_DATA_URL);
  if (!response.ok) return;
  const resources = await response.json();
  const totals = new Map();
  const enriched = new Map();

  for (const resource of resources) {
    const type = resource.type || "unknown";
    totals.set(type, (totals.get(type) || 0) + 1);
    if (coverageIsEnriched(resource)) enriched.set(type, (enriched.get(type) || 0) + 1);
  }

  const section = document.createElement("section");
  section.id = "type-coverage";
  section.className = "stats";
  section.setAttribute("aria-label", "Enrichment coverage by resource type");

  const heading = document.createElement("h2");
  heading.textContent = "Coverage by resource type";
  heading.style.gridColumn = "1 / -1";
  heading.style.margin = ".25rem 0 0";
  heading.style.fontSize = "1rem";
  section.append(heading);

  [...totals.keys()].sort().forEach(type => {
    const total = totals.get(type) || 0;
    const count = enriched.get(type) || 0;
    const pct = total ? (count / total) * 100 : 0;
    const article = document.createElement("article");
    const strong = document.createElement("strong");
    const label = document.createElement("span");
    strong.textContent = `${pct.toFixed(1)}%`;
    label.textContent = `${formatTypeLabel(type)} · ${count}/${total} enriched`;
    article.append(strong, label);
    section.append(article);
  });

  summary.insertAdjacentElement("afterend", section);
}

renderTypeCoverage().catch(() => {});
