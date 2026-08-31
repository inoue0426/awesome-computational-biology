#!/usr/bin/env python3
"""Load modular AI4Bio enrichment YAML fragments."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable


def enrichment_files(data_dir: Path) -> list[Path]:
    primary = data_dir / "enrichment.yml"
    fragments = sorted(data_dir.glob("enrichment.*.yml"))
    return [primary, *fragments]


def load_enrichment(
    data_dir: Path,
    load_yaml: Callable[[Path], dict[str, Any]],
) -> dict[str, Any]:
    """Merge enrichment fragments and reject duplicate resource IDs."""
    merged: dict[str, Any] = {}
    owners: dict[str, str] = {}
    for path in enrichment_files(data_dir):
        resources = load_yaml(path).get("resources", {})
        if not isinstance(resources, dict):
            raise ValueError(f"{path}: 'resources' must be a mapping keyed by resource id")
        for resource_id, fields in resources.items():
            if resource_id in merged:
                raise ValueError(
                    f"duplicate enrichment id {resource_id!r} in {owners[resource_id]} and {path.name}"
                )
            merged[resource_id] = fields
            owners[resource_id] = path.name
    return merged
