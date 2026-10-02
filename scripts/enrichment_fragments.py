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
    """Merge enrichment fragments, allowing disjoint field overlays per resource."""
    merged: dict[str, Any] = {}
    owners: dict[str, dict[str, str]] = {}
    for path in enrichment_files(data_dir):
        resources = load_yaml(path).get("resources", {})
        if not isinstance(resources, dict):
            raise ValueError(f"{path}: 'resources' must be a mapping keyed by resource id")
        for resource_id, fields in resources.items():
            if not isinstance(fields, dict):
                raise ValueError(
                    f"{path.name}: enrichment [{resource_id}] must be a mapping"
                )
            if resource_id not in merged:
                merged[resource_id] = dict(fields)
                owners[resource_id] = {field: path.name for field in fields}
                continue

            overlap = sorted(set(merged[resource_id]) & set(fields))
            if overlap:
                details = ", ".join(
                    f"{field!r} ({owners[resource_id][field]} vs {path.name})"
                    for field in overlap
                )
                raise ValueError(
                    f"duplicate enrichment fields for {resource_id!r}: {details}"
                )

            merged[resource_id].update(fields)
            owners[resource_id].update({field: path.name for field in fields})
    return merged
