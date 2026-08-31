#!/usr/bin/env python3
"""Sync data/resources.yml from the curated README list.

Parses the README resource lists and writes a normalized YAML file that
feeds the build pipeline for JSON/CSV and the generated README section.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

README_DEFAULT = Path("README.md")
OUTPUT_DEFAULT = Path("data/resources.yml")

SECTION_TYPE = {
    "Databases": "database",
    "Benchmarks & Datasets": "benchmark",
    "API": "api",
    "Preprocessing Tools": "toolkit",
    "Machine Learning Tasks and Models": "model",
}

HEADER = (
    "# Awesome Computational Biology - machine-readable resource list\n"
    "# Fields\n"
    "#   id          : unique slug (required)\n"
    "#   name        : display name (required)\n"
    "#   type        : category, e.g. database | tool | model | benchmark | api (required)\n"
    "#   url         : canonical URL (required)\n"
    "#   description : one-line description (required)\n"
    "#   license     : SPDX identifier or free-text (optional)\n"
    "#   api         : true | false - whether a programmatic API is available (default: false)\n"
    "#   updated     : last-known update date as string YYYY-MM-DD (optional)\n"
    "#   tasks       : list of ML/bio tasks (optional)\n"
    "#   modalities  : list of data modalities (optional)\n"
    "#   tags        : additional free-form tags (optional)\n"
    "#   organism    : list of organisms covered (optional)\n"
    "#   paper       : DOI or URL to primary publication (optional)\n"
    "\n"
    "resources:\n"
)

HEADING_RE = re.compile(r"^(#{2,5})\s+(.*)")
BULLET_RE = re.compile(r"^- \[(.+?)\]\((.+?)\)\s+\u2014\s+(.*)")

TAG_TO_TASKS: dict[str, list[str]] = {
    "drug-response-prediction": ["Drug Response Prediction"],
    "drug-perturbation": ["Drug Perturbation"],
    "drug-repurposing": ["Drug Repurposing"],
    "drug-target-interaction": ["Drug Target Interaction"],
    "compound-protein-interaction": ["Compound-Protein Interaction"],
    "molecular-generation": ["Molecular Generation"],
    "drug-discovery": ["Drug Discovery"],
    "protein-property-prediction": ["Protein Property Prediction"],
    "llm-for-biology": ["Language Modeling"],
    "single-cell-foundation-models": ["Foundation Model"],
    "protein-foundation-models": ["Foundation Model"],
    "multi-modal-foundation-models": ["Foundation Model"],
    "genomics-foundation-models": ["Foundation Model"],
    "foundation-models": ["Foundation Model"],
    "preprocessing-tools": ["Preprocessing"],
    "transcriptomics-foundation-models": ["Foundation Model"],
    "spatial-foundation-models": ["Foundation Model"],
    "multi-omics-foundation-models": ["Foundation Model"],
    "domain-alignment": ["Domain Alignment"],
    "compound-foundation-models": ["Foundation Model"],
    "compound-embedding": ["Foundation Model"],
    "pre-trained-embedding": ["Foundation Model"],
    "protein-structure-prediction-and-design": ["Protein Structure Prediction"],
}

TAG_TO_MODALITIES: dict[str, list[str]] = {
    "scrna": ["Single Cell"],
    "compound": ["Small Molecule"],
    "pathway": ["Pathway"],
    "mass-spectra": ["Mass Spectra"],
    "protein": ["Protein"],
    "genome": ["Genomics"],
    "disease": ["Disease"],
    "drug-gene-interaction": ["Small Molecule", "Gene"],
    "drug-cell-line-response": ["Small Molecule", "Gene Expression"],
    "chemical-protein-interaction": ["Small Molecule", "Protein"],
    "protein-protein-interaction": ["Protein"],
    "knowledge-graph": ["Knowledge Graph"],
    "gene-regulatory-network": ["Gene Expression"],
    "clinical-trial": ["Clinical"],
    "drug-response-prediction": ["Small Molecule"],
    "drug-perturbation": ["Small Molecule"],
    "drug-repurposing": ["Small Molecule"],
    "drug-target-interaction": ["Small Molecule", "Protein"],
    "compound-protein-interaction": ["Small Molecule", "Protein"],
    "molecular-generation": ["Small Molecule"],
    "drug-discovery": ["Small Molecule"],
    "protein-property-prediction": ["Protein"],
    "llm-for-biology": ["Text"],
    "single-cell-foundation-models": ["Single Cell"],
    "protein-foundation-models": ["Protein"],
    "multi-modal-foundation-models": ["Multi-Modal"],
    "genomics-foundation-models": ["Genomics"],
    "transcriptomics-foundation-models": ["Single Cell", "Transcriptomics"],
    "spatial-foundation-models": ["Spatial Transcriptomics"],
    "multi-omics-foundation-models": ["Multi-Omics"],
    "pre-trained-embedding": ["Protein"],
    "compound-foundation-models": ["Small Molecule"],
    "compound-embedding": ["Small Molecule"],
    "protein-structure-prediction-and-design": ["Protein"],
    "domain-alignment": ["Single Cell"],
}


def tagify(value: str) -> str:
    value = value.lower().strip()
    value = value.replace("&", "and")
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_") or "resource"


def parse_readme(readme_text: str) -> list[dict[str, Any]]:
    section = None
    subsection = None
    subsub = None
    subsubsub = None
    entries: list[dict[str, Any]] = []

    for line in readme_text.splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            if level == 2:
                section = title
                subsection = None
                subsub = None
                subsubsub = None
            elif level == 3:
                subsection = title
                subsub = None
                subsubsub = None
            elif level == 4:
                subsub = title
                subsubsub = None
            elif level == 5:
                subsubsub = title
            continue

        bullet = BULLET_RE.match(line.strip())
        if not bullet:
            continue

        name, url, description = (part.strip() for part in bullet.groups())
        entries.append(
            {
                "section": section,
                "subsection": subsection,
                "subsub": subsub,
                "subsubsub": subsubsub,
                "name": name,
                "url": url,
                "description": description,
            }
        )

    return entries


def _derive_from_tags(tags: list[str], mapping: dict[str, list[str]]) -> list[str]:
    result: set[str] = set()
    for tag in tags:
        for val in mapping.get(tag, []):
            result.add(val)
    return sorted(result)


def merge_entries(raw_entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[tuple[str, str], dict[str, Any]] = {}

    for entry in raw_entries:
        if entry.get("section") == "Auto-Generated Resources":
            continue

        section = entry.get("section") or "Other"
        res_type = SECTION_TYPE.get(section, "resource")

        tags = []
        if entry.get("subsection"):
            tags.append(tagify(entry["subsection"]))
        if entry.get("subsub"):
            tags.append(tagify(entry["subsub"]))
        if entry.get("subsubsub"):
            tags.append(tagify(entry["subsubsub"]))
        if not tags:
            tags.append(tagify(section))
        tags = [tag for tag in tags if tag]

        tasks = _derive_from_tags(tags, TAG_TO_TASKS)
        modalities = _derive_from_tags(tags, TAG_TO_MODALITIES)

        key = (entry["name"], entry["url"])
        if key not in merged:
            merged[key] = {
                "id": slugify(entry["name"]),
                "name": entry["name"],
                "type": res_type,
                "url": entry["url"],
                "description": entry["description"],
                "tags": sorted(set(tags)),
                "tasks": tasks,
                "modalities": modalities,
                "organism": [],
                "api": res_type == "api",
            }
        else:
            existing = merged[key]
            existing["tags"] = sorted(set(existing["tags"]).union(tags))
            existing["tasks"] = sorted(set(existing["tasks"]).union(tasks))
            existing["modalities"] = sorted(set(existing["modalities"]).union(modalities))
            if existing["type"] == "resource" and res_type != "resource":
                existing["type"] = res_type
            if res_type == "api":
                existing["api"] = True

    seen_ids: dict[str, int] = {}
    for entry in merged.values():
        base = entry["id"]
        if base in seen_ids:
            seen_ids[base] += 1
            entry["id"] = f"{base}_{seen_ids[base]}"
        else:
            seen_ids[base] = 1

    return sorted(merged.values(), key=lambda item: (item["type"], item["name"].lower()))


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f"\"{escaped}\""


def format_entry(entry: dict[str, Any]) -> str:
    lines = [f"  - id: {entry['id']}"]
    lines.append(f"    name: {yaml_quote(entry['name'])}")
    lines.append(f"    type: {entry['type']}")
    lines.append(f"    url: {entry['url']}")
    lines.append(f"    description: {yaml_quote(entry['description'])}")
    tags = entry.get("tags", [])
    lines.append(f"    tags: [{', '.join(tags)}]" if tags else "    tags: []")
    tasks = entry.get("tasks", [])
    lines.append(f"    tasks: [{', '.join(tasks)}]" if tasks else "    tasks: []")
    modalities = entry.get("modalities", [])
    lines.append(f"    modalities: [{', '.join(modalities)}]" if modalities else "    modalities: []")
    lines.append("    organism: []")
    lines.append(f"    api: {'true' if entry.get('api') else 'false'}")
    return "\n".join(lines)


def write_yaml(entries: list[dict[str, Any]], output_path: Path) -> None:
    body = "\n\n".join(format_entry(entry) for entry in entries)
    output_path.write_text(HEADER + body + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readme", type=Path, default=README_DEFAULT)
    parser.add_argument("--output", type=Path, default=OUTPUT_DEFAULT)
    args = parser.parse_args()

    readme_text = args.readme.read_text(encoding="utf-8")
    raw_entries = parse_readme(readme_text)
    entries = merge_entries(raw_entries)
    write_yaml(entries, args.output)
    print(f"Wrote {len(entries)} entries to {args.output}")


if __name__ == "__main__":
    main()
