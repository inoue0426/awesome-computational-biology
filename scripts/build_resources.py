#!/usr/bin/env python3
"""Build artifacts from data/resources.yml.

Usage:
    python scripts/build_resources.py

Requirements:
    pip install pyyaml          # or: pip install -r scripts/requirements.txt
"""

import csv
import json
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
DOCS_DATA_DIR = REPO_ROOT / "docs" / "data"
INPUT_FILE = DATA_DIR / "resources.yml"
JSON_OUTPUT = DATA_DIR / "resources.json"
CSV_OUTPUT = DATA_DIR / "resources.csv"
DOCS_JSON_OUTPUT = DOCS_DATA_DIR / "resources.json"
README_PATH = REPO_ROOT / "README.md"
README_MARKER_START = "<!-- RESOURCES:START -->"
README_MARKER_END = "<!-- RESOURCES:END -->"

# Required fields every entry must have
REQUIRED_FIELDS = ("id", "name", "type", "url", "description")

# Fields that must always be lists
LIST_FIELDS = ("tasks", "modalities", "tags", "organism")

# CSV column order
CSV_COLUMNS = [
    "id",
    "name",
    "type",
    "url",
    "description",
    "tags",
    "tasks",
    "modalities",
    "organism",
    "license",
    "api",
    "paper",
    "updated",
]

TYPE_LABELS = {
    "api": "API",
}


# ---------------------------------------------------------------------------
# Validation & normalisation
# ---------------------------------------------------------------------------

def validate_and_normalise(raw_entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate required fields and normalize optional fields.

    Args:
        raw_entries: Raw resource entries from YAML.

    Returns:
        A list of normalized resource entries.
    """
    errors: list[str] = []
    normalised: list[dict[str, Any]] = []

    for idx, entry in enumerate(raw_entries):
        if not isinstance(entry, dict):
            errors.append(f"Entry #{idx + 1} is not a mapping.")
            continue

        entry_id = entry.get("id", f"<entry #{idx + 1}>")

        # Required fields.
        for field in REQUIRED_FIELDS:
            if not entry.get(field):
                errors.append(f"[{entry_id}] missing required field: '{field}'")

        # Normalize list fields.
        for field in LIST_FIELDS:
            value = entry.get(field)
            if value is None:
                entry[field] = []
            elif not isinstance(value, list):
                entry[field] = [value]

        # Normalize api.
        entry["api"] = bool(entry.get("api", False))

        # Normalize updated.
        if "updated" in entry and entry["updated"] is not None:
            entry["updated"] = str(entry["updated"])

        normalised.append(entry)

    if errors:
        print("Validation failed with the following errors:", file=sys.stderr)
        for err in errors:
            print(f"  • {err}", file=sys.stderr)
        sys.exit(1)

    return normalised


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------

def write_json(entries: Iterable[dict[str, Any]], path: Path) -> None:
    """Write resources to a JSON file.

    Args:
        entries: Normalized resource entries.
        path: Output JSON path.
    """
    path.write_text(json.dumps(list(entries), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote JSON → {path}")


def write_csv(entries: Iterable[dict[str, Any]], path: Path) -> None:
    """Write resources to a CSV file.

    Args:
        entries: Normalized resource entries.
        path: Output CSV path.
    """
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for entry in entries:
            row = dict(entry)
            # Join list fields with pipes for CSV exports.
            for field in LIST_FIELDS:
                row[field] = "|".join(str(v) for v in row.get(field, []))
            writer.writerow(row)
    print(f"Wrote CSV → {path}")


def format_type_label(type_key: str) -> str:
    """Return a readable label for a resource type.

    Args:
        type_key: Raw type key from the YAML.

    Returns:
        A title-cased label suitable for Markdown headings.
    """
    if not type_key:
        return "Other"
    lowered = type_key.strip().lower()
    return TYPE_LABELS.get(lowered, lowered.replace("_", " ").title())


def build_markdown(entries: list[dict[str, Any]]) -> str:
    """Build a Markdown section from normalized resources.

    Args:
        entries: Normalized resource entries.

    Returns:
        Markdown content without the surrounding markers.
    """
    grouped: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        type_key = str(entry.get("type") or "other").lower()
        grouped.setdefault(type_key, []).append(entry)

    lines: list[str] = [
        "Generated from `data/resources.yml`.",
        "",
    ]
    for type_key in sorted(grouped):
        label = format_type_label(type_key)
        lines.append(f"### {label}")
        for entry in sorted(grouped[type_key], key=lambda item: str(item.get("name", "")).lower()):
            name = entry.get("name") or "Untitled"
            url = entry.get("url") or "#"
            description = entry.get("description") or ""
            lines.append(f"- [{name}]({url}) — {description}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def update_readme(path: Path, generated_markdown: str) -> None:
    """Replace the README auto-generated section between markers.

    Args:
        path: README path.
        generated_markdown: Markdown content to insert.
    """
    text = path.read_text(encoding="utf-8")
    if README_MARKER_START not in text or README_MARKER_END not in text:
        print("ERROR: README markers not found.", file=sys.stderr)
        sys.exit(1)

    before, _ = text.split(README_MARKER_START, 1)
    _, after = text.split(README_MARKER_END, 1)
    updated = (
        before
        + README_MARKER_START
        + "\n"
        + generated_markdown
        + README_MARKER_END
        + after
    )
    path.write_text(updated, encoding="utf-8")
    print(f"Updated README section → {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not INPUT_FILE.exists():
        print(f"ERROR: Input file not found: {INPUT_FILE}", file=sys.stderr)
        sys.exit(1)

    raw = yaml.safe_load(INPUT_FILE.read_text(encoding="utf-8"))

    if not isinstance(raw, dict) or "resources" not in raw:
        print(
            f"ERROR: {INPUT_FILE} must be a YAML mapping with a top-level 'resources' list.",
            file=sys.stderr,
        )
        sys.exit(1)

    raw_entries = raw["resources"]
    if not isinstance(raw_entries, list):
        print("ERROR: 'resources' must be a YAML list.", file=sys.stderr)
        sys.exit(1)

    entries = validate_and_normalise(raw_entries)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    write_json(entries, JSON_OUTPUT)
    write_json(entries, DOCS_JSON_OUTPUT)
    write_csv(entries, CSV_OUTPUT)

    markdown = build_markdown(entries)
    update_readme(README_PATH, markdown)


if __name__ == "__main__":
    main()
