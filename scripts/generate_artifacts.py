#!/usr/bin/env python3
"""Generate data/resources.json and data/resources.csv from data/resources.yml."""

import csv
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).parent.parent
SRC = ROOT / "data" / "resources.yml"
OUT_JSON = ROOT / "data" / "resources.json"
OUT_CSV = ROOT / "data" / "resources.csv"

# Fields that contain lists — serialised as "|"-separated strings in CSV
LIST_FIELDS = {"tags", "tasks", "modalities", "organism"}

CSV_COLUMNS = [
    "id", "name", "type", "url", "description",
    "tags", "tasks", "modalities", "organism",
    "license", "api", "paper", "updated",
]


def load_resources(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return data.get("resources", [])


def write_json(resources: list[dict], path: Path) -> None:
    path.write_text(
        json.dumps(resources, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def flatten_row(resource: dict) -> dict:
    """Return a flat dict suitable for CSV output."""
    row: dict = {}
    for col in CSV_COLUMNS:
        value = resource.get(col)
        if isinstance(value, list):
            row[col] = "|".join(str(v) for v in value)
        elif value is None:
            row[col] = ""
        else:
            row[col] = str(value)
    return row


def write_csv(resources: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for resource in resources:
            writer.writerow(flatten_row(resource))


def main() -> None:
    if not SRC.exists():
        print(f"Source file not found: {SRC}", file=sys.stderr)
        sys.exit(1)

    resources = load_resources(SRC)
    print(f"Loaded {len(resources)} resources from {SRC}")

    write_json(resources, OUT_JSON)
    print(f"Wrote {OUT_JSON}")

    write_csv(resources, OUT_CSV)
    print(f"Wrote {OUT_CSV}")


if __name__ == "__main__":
    main()
