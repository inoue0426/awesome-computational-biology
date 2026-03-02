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

HEADING_RE = re.compile(r"^(#{2,4})\s+(.*)")
BULLET_RE = re.compile(r"^- \[(.+?)\]\((.+?)\)\s+\u2014\s+(.*)")


def tagify(value: str) -> str:
    """Normalize a heading into a tag.

    Args:
        value: Heading text.

    Returns:
        Normalized tag string.
    """
    value = value.lower().strip()
    value = value.replace("&", "and")
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value


def slugify(value: str) -> str:
    """Normalize a name into a slug id.

    Args:
        value: Resource name.

    Returns:
        Snake_case slug.
    """
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_") or "resource"


def parse_readme(readme_text: str) -> list[dict[str, Any]]:
    """Parse README list items into raw entry dictionaries.

    Args:
        readme_text: Full README content.

    Returns:
        List of raw entry dicts.
    """
    section = None
    subsection = None
    subsub = None
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
            elif level == 3:
                subsection = title
                subsub = None
            elif level == 4:
                subsub = title
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
                "name": name,
                "url": url,
                "description": description,
            }
        )

    return entries


def merge_entries(raw_entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge duplicate entries and map headings to resource fields.

    Args:
        raw_entries: Raw parsed entries from README.

    Returns:
        Normalized entries for YAML output.
    """
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
        if not tags:
            tags.append(tagify(section))
        tags = [tag for tag in tags if tag]

        key = (entry["name"], entry["url"])
        if key not in merged:
            merged[key] = {
                "id": slugify(entry["name"]),
                "name": entry["name"],
                "type": res_type,
                "url": entry["url"],
                "description": entry["description"],
                "tags": sorted(set(tags)),
                "tasks": [],
                "modalities": [],
                "organism": [],
                "api": res_type == "api",
            }
        else:
            existing = merged[key]
            existing["tags"] = sorted(set(existing["tags"]).union(tags))
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
    """Return a YAML-safe double-quoted string.

    Args:
        value: Input string.

    Returns:
        Quoted string with escapes.
    """
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f"\"{escaped}\""


def format_entry(entry: dict[str, Any]) -> str:
    """Format a resource entry into YAML lines.

    Args:
        entry: Normalized resource entry.

    Returns:
        YAML string for one entry.
    """
    lines = [f"  - id: {entry['id']}"]
    lines.append(f"    name: {yaml_quote(entry['name'])}")
    lines.append(f"    type: {entry['type']}")
    lines.append(f"    url: {entry['url']}")
    lines.append(f"    description: {yaml_quote(entry['description'])}")
    tags = entry.get("tags", [])
    if tags:
        lines.append(f"    tags: [{', '.join(tags)}]")
    else:
        lines.append("    tags: []")
    lines.append("    tasks: []")
    lines.append("    modalities: []")
    lines.append("    organism: []")
    lines.append(f"    api: {'true' if entry.get('api') else 'false'}")
    return "\n".join(lines)


def write_yaml(entries: list[dict[str, Any]], output_path: Path) -> None:
    """Write entries to data/resources.yml.

    Args:
        entries: Normalized entries.
        output_path: Output file path.
    """
    body = "\n\n".join(format_entry(entry) for entry in entries)
    output_path.write_text(HEADER + body + "\n", encoding="utf-8")


def main() -> None:
    """CLI entrypoint for syncing resources.yml from README."""
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
