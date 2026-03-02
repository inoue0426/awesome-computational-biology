#!/usr/bin/env python3
"""Build script: reads data/resources.yml → data/resources.json + data/resources.csv.

Usage:
    python scripts/build_resources.py

Requirements:
    pip install pyyaml          # or: pip install -r scripts/requirements.txt
"""

import csv
import json
import sys
from pathlib import Path

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
INPUT_FILE = DATA_DIR / "resources.yml"
JSON_OUTPUT = DATA_DIR / "resources.json"
CSV_OUTPUT = DATA_DIR / "resources.csv"

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
    "license",
    "api",
    "updated",
    "tasks",
    "modalities",
    "tags",
    "organism",
    "paper",
]


# ---------------------------------------------------------------------------
# Validation & normalisation
# ---------------------------------------------------------------------------

def validate_and_normalise(raw_entries: list) -> list:
    """Validate required fields and normalise optional fields.

    Returns the normalised list.  Exits with code 1 on any validation error.
    """
    errors: list[str] = []
    normalised: list[dict] = []

    for idx, entry in enumerate(raw_entries):
        if not isinstance(entry, dict):
            errors.append(f"Entry #{idx + 1} is not a mapping.")
            continue

        entry_id = entry.get("id", f"<entry #{idx + 1}>")

        # --- Required fields ---
        for field in REQUIRED_FIELDS:
            if not entry.get(field):
                errors.append(f"[{entry_id}] missing required field: '{field}'")

        # --- Normalise list fields ---
        for field in LIST_FIELDS:
            value = entry.get(field)
            if value is None:
                entry[field] = []
            elif not isinstance(value, list):
                entry[field] = [value]

        # --- Normalise api ---
        entry["api"] = bool(entry.get("api", False))

        # --- Normalise updated ---
        if "updated" in entry:
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

def write_json(entries: list, path: Path) -> None:
    path.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(entries)} entries → {path}")


def write_csv(entries: list, path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for entry in entries:
            row = dict(entry)
            # Join list fields with semicolons
            for field in LIST_FIELDS:
                row[field] = ";".join(str(v) for v in row.get(field, []))
            writer.writerow(row)
    print(f"Wrote {len(entries)} entries → {path}")


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
    write_json(entries, JSON_OUTPUT)
    write_csv(entries, CSV_OUTPUT)


if __name__ == "__main__":
    main()
