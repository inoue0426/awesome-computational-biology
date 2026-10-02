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
| `dataset_profile` | object | Optional Dataset Explorer metadata for structured comparison of datasets/benchmarks. |

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

## Dataset Explorer profile

Resources that participate in the Dataset Explorer may define a `dataset_profile` object in a modular `data/enrichment.*.yml` file. This keeps README-derived identity fields separate from deeper dataset metadata.

Supported v1 fields:

| Field | Type | Meaning |
|---|---|---|
| `species` | array of strings | Species represented in the dataset. |
| `sample_type` | string | Primary unit, e.g. `patient` or `cell-line`. |
| `biological_context` | string | High-level context such as `cancer` or `perturbation-screen`. |
| `perturbation_type` | array of strings | Chemical, genetic, or other interventions. |
| `paired` | boolean | Whether molecular/sample identity can be linked to the measured response or perturbation condition. |
| `pre_post` | boolean | Whether matched pre-treatment and post-treatment samples are available. |
| `longitudinal` | boolean | Whether repeated measurements over time are available as a core design feature. |
| `drug_identity` | boolean or string | Whether treatment identity is available; strings such as `limited` may encode partial availability. |
| `dose` | boolean | Whether dose/concentration metadata are available. |
| `smiles` | boolean or `partial`/`limited` | Whether compound structures are directly available or can only be partially mapped. |
| `clinical_outcome` | boolean | Whether patient-level clinical outcomes are available. |
| `n_samples` | string | Human-readable scale summary. |
| `n_cells` | integer, string, or null | Cell count for single-cell datasets when meaningful. |
| `n_profiles` | integer, string, or null | Number of profiles in the curated comparison view. |
| `n_compounds` | integer, string, or null | Number of compounds/molecules in the curated comparison view. |
| `n_contexts` | integer, string, or null | Number of cellular or experimental contexts. |
| `readout` | string | Primary readout, e.g. `bulk-rna`, `pseudobulk-rna`, `single-cell-rna`, or `viability`. |
| `gene_panel` | string | Gene/readout panel summary, e.g. `20,251 full / 2,000 HVG` or `978 landmark genes`. |
| `time` | boolean | Whether treatment time metadata are available. |
| `access` | string | Dataset-level access summary. |

The v1 profiles are colocated with their existing modular `data/enrichment.*.yml` owners and rendered at `docs/dataset-explorer.html`.
