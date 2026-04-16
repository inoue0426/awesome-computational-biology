# Resource Data Schema (`docs/data/resources.json`)

This document describes the JSON schema used by the GitHub Pages UI.

## Source of truth and generation flow

- **Canonical list source:** `README.md` (curated resource bullets)
- Generated from README to YAML: `scripts/sync_resources_from_readme.py` → `data/resources.yml`
- Built artifacts from YAML: `scripts/build_resources.py` → `data/resources.json`, `data/resources.csv`, and `docs/data/resources.json`

When contributing new resources, update `README.md` first, then regenerate artifacts.

## Top-level structure

- `resources.json` is a JSON array.
- Each array item is one resource object.

## Fields

### Required fields

| Field | Type | Notes |
|---|---|---|
| `id` | string | Unique slug. Use lowercase `snake_case`, stable over time. |
| `name` | string | Display name shown in README/UI. |
| `type` | string | Resource category. Current values: `api`, `benchmark`, `database`, `model`, `toolkit`. |
| `url` | string | Canonical landing page URL. |
| `description` | string | One-line, factual summary. |

### Optional fields

| Field | Type | Notes |
|---|---|---|
| `tags` | array of strings | Free-form tags. |
| `tasks` | array of strings | Task labels used by Task filter. |
| `modalities` | array of strings | Data modality labels used by Modality filter. |
| `organism` | array of strings | Organism labels. |
| `license` | string | SPDX identifier preferred when known. |
| `api` | boolean | Whether programmatic API access is available. Defaults to `false`. |
| `paper` | string | DOI or URL to preprint/peer-reviewed publication. |
| `updated` | string | Last-known update date, recommended `YYYY-MM-DD`. |

## Naming and consistency guidance

- `id` must be globally unique across all resources.
- Prefer concise, stable IDs (e.g., `open_targets_platform`, `alphafold3`).
- Keep `name` aligned with official project/database naming.
- Use short, objective descriptions (avoid marketing language).

## Example object

```json
{
  "id": "open_targets_platform",
  "name": "Open Targets Platform",
  "type": "database",
  "url": "https://platform.opentargets.org/",
  "description": "Target identification platform integrating genetics, genomics, and drug evidence.",
  "tags": ["disease", "drug-discovery"],
  "tasks": ["target-identification"],
  "modalities": ["genomics"],
  "organism": ["human"],
  "license": "CC-BY-4.0",
  "api": true,
  "paper": "https://doi.org/10.1093/nar/gkac1045",
  "updated": "2026-01-15"
}
```
