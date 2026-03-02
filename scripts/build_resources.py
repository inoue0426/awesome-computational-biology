#!/usr/bin/env python3
"""Build resources.json and resources.csv from data/resources.yaml."""

import csv
import json
import pathlib

import yaml

ROOT = pathlib.Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
SRC = DATA_DIR / "resources.yaml"
DST_JSON = DATA_DIR / "resources.json"
DST_CSV = DATA_DIR / "resources.csv"


def main() -> None:
    with SRC.open(encoding="utf-8") as fh:
        resources = yaml.safe_load(fh)

    if not isinstance(resources, list):
        raise ValueError(
            "resources.yaml must be a YAML list of resource objects, "
            "each with at least 'name', 'category', and 'url' fields"
        )

    # Normalise tags to a list of strings
    for resource in resources:
        tags = resource.get("tags", [])
        resource["tags"] = tags if isinstance(tags, list) else []

    # Write JSON
    DST_JSON.write_text(json.dumps(resources, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {DST_JSON}")

    # Write CSV
    fieldnames = ["name", "category", "subcategory", "url", "description", "tags"]
    with DST_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for resource in resources:
            row = dict(resource)
            row["tags"] = ",".join(resource.get("tags", []))
            writer.writerow(row)
    print(f"Wrote {DST_CSV}")


if __name__ == "__main__":
    main()
