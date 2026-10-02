#!/usr/bin/env python3
"""Validate AI4Bio resource YAML and modular enrichment metadata."""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

from enrichment_fragments import load_enrichment

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
BASE_FILE = DATA_DIR / "resources.yml"
VOCABULARY_FILE = DATA_DIR / "vocabulary.yml"

REQUIRED_FIELDS = ("id", "name", "type", "url", "description")
LIST_FIELDS = (
    "tags", "tasks", "modalities", "organism", "entities", "methods",
    "organizations", "metadata_sources",
)
CONTROLLED_FIELDS = ("entities", "methods", "modalities", "tasks")
ALLOWED_TYPES = {"api", "benchmark", "database", "model", "resource", "toolkit"}
ALLOWED_MAINTENANCE = {"active", "maintenance", "archived", "unknown"}
ALLOWED_ACCESS = {"open", "registration", "restricted", "commercial", "unknown"}
ALLOWED_FIELDS = set(REQUIRED_FIELDS) | set(LIST_FIELDS) | {
    "license", "api", "paper", "updated", "github", "documentation", "year",
    "maintenance_status", "access", "last_checked", "dataset_profile", "method_profile",
    "foundation_profile", "agent_profile",
}
ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
VOCAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
URL_FIELDS = ("url", "paper", "github", "documentation")
DATE_FIELDS = ("updated", "last_checked")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def valid_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_date(value: Any) -> bool:
    try:
        date.fromisoformat(str(value))
        return True
    except ValueError:
        return False


def load_vocabulary() -> tuple[dict[str, set[str]], list[str]]:
    errors: list[str] = []
    raw = load_yaml(VOCABULARY_FILE)
    controlled = raw.get("controlled_fields")
    if not isinstance(controlled, dict):
        return {}, ["data/vocabulary.yml: 'controlled_fields' must be a mapping"]

    unknown_fields = sorted(set(controlled) - set(CONTROLLED_FIELDS))
    if unknown_fields:
        errors.append(
            "data/vocabulary.yml: unknown controlled fields: " + ", ".join(unknown_fields)
        )

    vocabulary: dict[str, set[str]] = {}
    for field in CONTROLLED_FIELDS:
        values = controlled.get(field)
        if not isinstance(values, list) or not values:
            errors.append(f"data/vocabulary.yml: '{field}' must be a non-empty list")
            continue
        if any(not isinstance(value, str) or not value.strip() for value in values):
            errors.append(f"data/vocabulary.yml: '{field}' must contain non-empty strings")
            continue
        if len(values) != len(set(values)):
            errors.append(f"data/vocabulary.yml: '{field}' contains duplicate terms")
        invalid = sorted(value for value in values if not VOCAB_RE.fullmatch(value))
        if invalid:
            errors.append(
                f"data/vocabulary.yml: '{field}' terms must use lowercase kebab-case: "
                + ", ".join(invalid)
            )
        vocabulary[field] = set(values)

    return vocabulary, errors


def validate_enrichment_vocabulary(
    resource_id: str,
    fields: dict[str, Any],
    vocabulary: dict[str, set[str]],
) -> list[str]:
    errors: list[str] = []
    for field in CONTROLLED_FIELDS:
        if field not in fields:
            continue
        values = fields[field]
        if not isinstance(values, list):
            continue
        allowed = vocabulary.get(field, set())
        for value in values:
            if isinstance(value, str) and value not in allowed:
                errors.append(
                    f"enrichment [{resource_id}] '{field}' uses non-canonical term: {value!r}; "
                    "add a canonical term to data/vocabulary.yml or use an existing one"
                )
    return errors


def merge_resources() -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    base = load_yaml(BASE_FILE).get("resources", [])
    try:
        overlay = load_enrichment(DATA_DIR, load_yaml)
    except ValueError as exc:
        return [], [str(exc)]
    vocabulary, vocabulary_errors = load_vocabulary()
    errors.extend(vocabulary_errors)

    if not isinstance(base, list):
        return [], errors + ["data/resources.yml: 'resources' must be a list"]

    by_id: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(base, 1):
        if not isinstance(raw, dict):
            errors.append(f"base entry #{index} is not a mapping")
            continue
        resource_id = raw.get("id")
        if resource_id in by_id:
            errors.append(f"duplicate id: {resource_id}")
        if resource_id:
            by_id[resource_id] = dict(raw)

    for resource_id, fields in overlay.items():
        if resource_id not in by_id:
            errors.append(f"enrichment references unknown id: {resource_id}")
            continue
        if not isinstance(fields, dict):
            errors.append(f"enrichment [{resource_id}] must be a mapping")
            continue
        forbidden = set(REQUIRED_FIELDS) & set(fields)
        if forbidden:
            errors.append(f"enrichment [{resource_id}] cannot override identity fields: {', '.join(sorted(forbidden))}")
        errors.extend(validate_enrichment_vocabulary(resource_id, fields, vocabulary))
        by_id[resource_id].update(fields)

    return list(by_id.values()), errors


def validate_entry(entry: dict[str, Any]) -> list[str]:
    rid = str(entry.get("id") or "<missing-id>")
    errors: list[str] = []
    unknown = sorted(set(entry) - ALLOWED_FIELDS)
    if unknown:
        errors.append(f"[{rid}] unknown fields: {', '.join(unknown)}")
    for field in REQUIRED_FIELDS:
        if not isinstance(entry.get(field), str) or not entry[field].strip():
            errors.append(f"[{rid}] '{field}' must be a non-empty string")
    if isinstance(entry.get("id"), str) and not ID_RE.fullmatch(entry["id"]):
        errors.append(f"[{rid}] id must use lowercase snake_case")
    if entry.get("type") not in ALLOWED_TYPES:
        errors.append(f"[{rid}] invalid type: {entry.get('type')}")
    for field in LIST_FIELDS:
        value = entry.get(field, [])
        if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
            errors.append(f"[{rid}] '{field}' must be a list of non-empty strings")
        elif len(value) != len(set(value)):
            errors.append(f"[{rid}] '{field}' contains duplicates")
    for field in URL_FIELDS:
        value = entry.get(field)
        if value and (not isinstance(value, str) or not valid_http_url(value)):
            errors.append(f"[{rid}] '{field}' must be an http(s) URL")
    if entry.get("github") and not str(entry["github"]).startswith("https://github.com/"):
        errors.append(f"[{rid}] 'github' must be a github.com URL")
    sources = entry.get("metadata_sources", [])
    for value in sources if isinstance(sources, list) else []:
        if not valid_http_url(value):
            errors.append(f"[{rid}] metadata source must be an http(s) URL: {value}")
    for field in DATE_FIELDS:
        if entry.get(field) is not None and not validate_date(entry[field]):
            errors.append(f"[{rid}] '{field}' must be YYYY-MM-DD")
    year = entry.get("year")
    if year is not None and (not isinstance(year, int) or isinstance(year, bool) or not 1900 <= year <= 2100):
        errors.append(f"[{rid}] 'year' must be an integer from 1900 to 2100")
    if entry.get("maintenance_status") not in ALLOWED_MAINTENANCE | {None}:
        errors.append(f"[{rid}] invalid maintenance_status: {entry.get('maintenance_status')}")
    if entry.get("access") not in ALLOWED_ACCESS | {None}:
        errors.append(f"[{rid}] invalid access: {entry.get('access')}")
    if "api" in entry and not isinstance(entry["api"], bool):
        errors.append(f"[{rid}] 'api' must be boolean")

    profile = entry.get("dataset_profile")
    if profile is not None:
        if not isinstance(profile, dict):
            errors.append(f"[{rid}] 'dataset_profile' must be a mapping")
        else:
            allowed_profile_fields = {
                "year", "species", "sample_type", "biological_context", "perturbation_type", "genetic_modes",
                "paired", "pre_post", "longitudinal", "drug_identity", "dose",
                "smiles", "clinical_outcome", "n_samples", "n_cells", "access",
                "readout", "gene_panel", "n_profiles", "n_perturbations", "n_compounds", "n_contexts", "time", "view_scope",
            }
            unknown_profile = sorted(set(profile) - allowed_profile_fields)
            if unknown_profile:
                errors.append(
                    f"[{rid}] dataset_profile unknown fields: {', '.join(unknown_profile)}"
                )
            for field in ("species", "perturbation_type", "genetic_modes"):
                value = profile.get(field, [])
                if not isinstance(value, list) or any(
                    not isinstance(item, str) or not item.strip() for item in value
                ):
                    errors.append(
                        f"[{rid}] dataset_profile.{field} must be a list of non-empty strings"
                    )
            if "year" in profile and (
                not isinstance(profile["year"], int)
                or isinstance(profile["year"], bool)
                or not 1900 <= profile["year"] <= 2100
            ):
                errors.append(
                    f"[{rid}] dataset_profile.year must be an integer from 1900 to 2100"
                )
            for field in ("paired", "pre_post", "longitudinal", "dose", "time", "clinical_outcome"):
                if field in profile and not isinstance(profile[field], bool):
                    errors.append(f"[{rid}] dataset_profile.{field} must be boolean")
            if "drug_identity" in profile and not isinstance(profile["drug_identity"], (bool, str)):
                errors.append(f"[{rid}] dataset_profile.drug_identity must be boolean or string")
            if "smiles" in profile and profile["smiles"] not in {True, False, "partial", "limited"}:
                errors.append(
                    f"[{rid}] dataset_profile.smiles must be true, false, partial, or limited"
                )
            for field in ("sample_type", "biological_context", "n_samples", "access", "readout", "gene_panel", "view_scope"):
                if field in profile and profile[field] is not None and not isinstance(profile[field], str):
                    errors.append(f"[{rid}] dataset_profile.{field} must be a string")
            for field in ("n_cells", "n_profiles", "n_perturbations", "n_compounds", "n_contexts"):
                if field in profile and profile[field] is not None and not isinstance(
                    profile[field], (int, str)
                ):
                    errors.append(
                        f"[{rid}] dataset_profile.{field} must be integer, string, or null"
                    )
    foundation_profile = entry.get("foundation_profile")
    if foundation_profile is not None:
        if not isinstance(foundation_profile, dict):
            errors.append(f"[{rid}] 'foundation_profile' must be a mapping")
        else:
            allowed_foundation_fields = {
                "year", "modalities", "params", "params_millions",
                "pretraining_scale", "species", "zero_shot", "finetunable",
                "weights", "code", "perturbation", "spatial",
            }
            unknown_foundation = sorted(
                set(foundation_profile) - allowed_foundation_fields
            )
            if unknown_foundation:
                errors.append(
                    f"[{rid}] foundation_profile unknown fields: "
                    + ", ".join(unknown_foundation)
                )
            for field in ("modalities", "species"):
                value = foundation_profile.get(field, [])
                if not isinstance(value, list) or any(
                    not isinstance(item, str) or not item.strip() for item in value
                ):
                    errors.append(
                        f"[{rid}] foundation_profile.{field} must be a list of non-empty strings"
                    )
            if "year" in foundation_profile and (
                not isinstance(foundation_profile["year"], int)
                or isinstance(foundation_profile["year"], bool)
                or not 1900 <= foundation_profile["year"] <= 2100
            ):
                errors.append(
                    f"[{rid}] foundation_profile.year must be an integer from 1900 to 2100"
                )
            if "params_millions" in foundation_profile and (
                not isinstance(foundation_profile["params_millions"], (int, float))
                or isinstance(foundation_profile["params_millions"], bool)
                or foundation_profile["params_millions"] < 0
            ):
                errors.append(
                    f"[{rid}] foundation_profile.params_millions must be a non-negative number"
                )
            for field in ("params", "pretraining_scale"):
                if (
                    field in foundation_profile
                    and foundation_profile[field] is not None
                    and not isinstance(foundation_profile[field], str)
                ):
                    errors.append(
                        f"[{rid}] foundation_profile.{field} must be a string or null"
                    )
            allowed_states = {True, False, "yes", "no", "limited", "unknown"}
            for field in (
                "zero_shot", "finetunable", "weights", "code",
                "perturbation", "spatial",
            ):
                if (
                    field in foundation_profile
                    and foundation_profile[field] not in allowed_states
                ):
                    errors.append(
                        f"[{rid}] foundation_profile.{field} must be boolean or "
                        "yes/no/limited/unknown"
                    )
    agent_profile = entry.get("agent_profile")
    if agent_profile is not None:
        if not isinstance(agent_profile, dict):
            errors.append(f"[{rid}] 'agent_profile' must be a mapping")
        else:
            allowed_agent_fields = {
                "year", "domains", "architecture", "tool_use", "code_execution",
                "web_retrieval", "literature", "omics", "wet_lab",
                "autonomous_experiment", "human_in_loop", "open_source",
            }
            unknown_agent = sorted(set(agent_profile) - allowed_agent_fields)
            if unknown_agent:
                errors.append(
                    f"[{rid}] agent_profile unknown fields: "
                    + ", ".join(unknown_agent)
                )
            if "domains" in agent_profile:
                value = agent_profile["domains"]
                if not isinstance(value, list) or any(
                    not isinstance(item, str) or not item.strip() for item in value
                ):
                    errors.append(
                        f"[{rid}] agent_profile.domains must be a list of non-empty strings"
                    )
            if "architecture" in agent_profile and agent_profile["architecture"] not in {
                "single-agent", "multi-agent", "agent-ecosystem"
            }:
                errors.append(
                    f"[{rid}] agent_profile.architecture must be single-agent, "
                    "multi-agent, or agent-ecosystem"
                )
            if "year" in agent_profile and (
                not isinstance(agent_profile["year"], int)
                or isinstance(agent_profile["year"], bool)
                or not 1900 <= agent_profile["year"] <= 2100
            ):
                errors.append(
                    f"[{rid}] agent_profile.year must be an integer from 1900 to 2100"
                )
            allowed_states = {True, False, "yes", "no", "limited", "unknown"}
            for field in (
                "tool_use", "code_execution", "web_retrieval", "literature",
                "omics", "wet_lab", "autonomous_experiment", "human_in_loop",
                "open_source",
            ):
                if field in agent_profile and agent_profile[field] not in allowed_states:
                    errors.append(
                        f"[{rid}] agent_profile.{field} must be boolean or "
                        "yes/no/limited/unknown"
                    )
    return errors


def main() -> None:
    entries, errors = merge_resources()
    for entry in entries:
        errors.extend(validate_entry(entry))
    if errors:
        print(f"Validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)
    print(f"Validated {len(entries)} resources, enrichment fragments, and controlled vocabulary.")


if __name__ == "__main__":
    main()
