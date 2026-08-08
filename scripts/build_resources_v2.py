#!/usr/bin/env python3
"""Build enriched AI4Bio artifacts from data/resources.yml + data/enrichment.yml."""

from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
DOCS_DATA_DIR = REPO_ROOT / "docs" / "data"
BASE_FILE = DATA_DIR / "resources.yml"
ENRICHMENT_FILE = DATA_DIR / "enrichment.yml"
JSON_OUTPUT = DATA_DIR / "resources.json"
CSV_OUTPUT = DATA_DIR / "resources.csv"
DOCS_JSON_OUTPUT = DOCS_DATA_DIR / "resources.json"

BASE_LIST_FIELDS = ("tags", "tasks", "modalities", "organism")
ENRICHMENT_LIST_FIELDS = ("entities", "methods", "organizations", "metadata_sources")
ALL_LIST_FIELDS = BASE_LIST_FIELDS + ENRICHMENT_LIST_FIELDS
LEGACY_CSV_COLUMNS = [
    "id", "name", "type", "url", "description", "tags", "tasks", "modalities",
    "organism", "license", "api", "paper", "updated",
]
ENRICHMENT_CSV_COLUMNS = [
    "entities", "methods", "organizations", "github", "documentation", "year",
    "maintenance_status", "access", "last_checked", "metadata_sources",
]
IDENTITY_FIELDS = {"id", "name", "type", "url", "description"}


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def merge_entries() -> list[dict[str, Any]]:
    base = load_yaml(BASE_FILE).get("resources", [])
    overlay = load_yaml(ENRICHMENT_FILE).get("resources", {})
    if not isinstance(base, list):
        raise ValueError("data/resources.yml 'resources' must be a list")
    if not isinstance(overlay, dict):
        raise ValueError("data/enrichment.yml 'resources' must be a mapping keyed by resource id")

    entries: list[dict[str, Any]] = []
    known_ids = {entry.get("id") for entry in base if isinstance(entry, dict)}
    unknown_ids = sorted(set(overlay) - known_ids)
    if unknown_ids:
        raise ValueError(f"enrichment references unknown ids: {', '.join(unknown_ids)}")

    for raw in base:
        entry = dict(raw)
        resource_id = entry.get("id")
        extra = overlay.get(resource_id, {})
        if not isinstance(extra, dict):
            raise ValueError(f"enrichment [{resource_id}] must be a mapping")
        forbidden = IDENTITY_FIELDS & set(extra)
        if forbidden:
            raise ValueError(
                f"enrichment [{resource_id}] cannot override identity fields: "
                + ", ".join(sorted(forbidden))
            )
        entry.update(extra)

        # Preserve the legacy artifact shape when no enrichment is present.
        # Base list fields have always been normalized to arrays, but v2-only
        # list fields are normalized only when explicitly supplied.
        for field in BASE_LIST_FIELDS:
            value = entry.get(field)
            if value is None:
                entry[field] = []
            elif not isinstance(value, list):
                entry[field] = [value]
        for field in ENRICHMENT_LIST_FIELDS:
            if field not in entry:
                continue
            value = entry[field]
            if value is None:
                entry.pop(field)
            elif not isinstance(value, list):
                entry[field] = [value]

        entry["api"] = bool(entry.get("api", False))
        for field in ("updated", "last_checked"):
            if field in entry and entry[field] is not None:
                entry[field] = str(entry[field])
        entries.append(entry)
    return entries


def csv_columns(entries: list[dict[str, Any]]) -> list[str]:
    """Return legacy columns unless at least one v2 enrichment field is present."""
    has_enrichment = any(
        any(field in entry for field in ENRICHMENT_CSV_COLUMNS)
        for entry in entries
    )
    if not has_enrichment:
        return LEGACY_CSV_COLUMNS
    return LEGACY_CSV_COLUMNS + ENRICHMENT_CSV_COLUMNS


def write_json(entries: Iterable[dict[str, Any]], path: Path) -> None:
    path.write_text(json.dumps(list(entries), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote JSON -> {path}")


def write_csv(entries: list[dict[str, Any]], path: Path) -> None:
    columns = csv_columns(entries)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for entry in entries:
            row = dict(entry)
            for field in ALL_LIST_FIELDS:
                if field in row:
                    row[field] = "|".join(str(value) for value in row.get(field, []))
            writer.writerow(row)
    print(f"Wrote CSV -> {path}")


def running_in_pr_ci() -> bool:
    return (
        os.environ.get("GITHUB_ACTIONS", "").lower() == "true"
        and os.environ.get("GITHUB_EVENT_NAME") == "pull_request"
    )


def write_outputs(entries: list[dict[str, Any]]) -> None:
    # Pull-request CI is validation-only. Build into a temporary directory so
    # the workflow can verify that generation succeeds without requiring every
    # enrichment PR to commit large derived artifacts. On main/push, outputs
    # are materialized normally and Sync Resources commits any resulting diff.
    if running_in_pr_ci():
        with tempfile.TemporaryDirectory(prefix="ai4bio-build-") as tmp:
            tmp_dir = Path(tmp)
            write_json(entries, tmp_dir / "resources.json")
            write_json(entries, tmp_dir / "docs-resources.json")
            write_csv(entries, tmp_dir / "resources.csv")
        print("PR validation build completed without modifying tracked artifacts.")
        return

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    write_json(entries, JSON_OUTPUT)
    write_json(entries, DOCS_JSON_OUTPUT)
    write_csv(entries, CSV_OUTPUT)


def main() -> None:
    validation = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_resources.py")],
        check=False,
    )
    if validation.returncode:
        sys.exit(validation.returncode)
    entries = merge_entries()
    write_outputs(entries)


if __name__ == "__main__":
    main()
