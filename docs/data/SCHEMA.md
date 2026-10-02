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
| `method_profile` | object | Optional Method Explorer metadata for structured comparison of response and perturbation methods. |
| `foundation_profile` | object | Optional Foundation Model Explorer metadata for modality, model scale, size, and availability. |
| `agent_profile` | object | Optional Agent Explorer metadata for agent architecture, capabilities, and scientific workflow support. |

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
| `genetic_modes` | array of strings | Genetic perturbation mechanisms, e.g. `crispri`, `crispra`, `crispr-ko`, `enhancer-targeting`, `combinatorial`, or `mixed`. |
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
| `n_perturbations` | integer, string, or null | Number of perturbation targets/conditions, especially useful for genetic screens. |
| `n_compounds` | integer, string, or null | Number of compounds/molecules in the curated comparison view. |
| `n_contexts` | integer, string, or null | Number of cellular or experimental contexts. |
| `readout` | string | Primary readout, e.g. `bulk-rna`, `pseudobulk-rna`, `single-cell-rna`, or `viability`. |
| `gene_panel` | string | Gene/readout panel summary, e.g. `20,251 full / 2,000 HVG` or `978 landmark genes`. |
| `time` | boolean | Whether treatment time metadata are available. |
| `view_scope` | string | Scope of the displayed scale fields, e.g. `full-resource`, `study-cohort`, or `bison-benchmark-view`. |
| `access` | string | Dataset-level access summary. |

The v1 profiles are colocated with their existing modular `data/enrichment.*.yml` owners and rendered at `docs/dataset-explorer.html`.

## Method Explorer profile

Methods shown in the Method Explorer may define a `method_profile` object in a modular enrichment fragment.

| Field | Type | Meaning |
|---|---|---|
| `task_family` | string | High-level task, currently `drug-response-prediction` or `drug-perturbation`. |
| `year` | integer | Publication/release year used for navigation. |
| `input` | string | Main biological/model input. |
| `drug_representation` | string | Chemical or treatment representation. |
| `context_representation` | string | Cellular, patient, or experimental context representation. |
| `output` | string | Main prediction target. |
| `unseen_drug` | boolean/string | Support for unseen-drug generalization; `limited` denotes partial or task-dependent support. |
| `unseen_context` | boolean/string | Support for new cellular/patient contexts. |
| `dose` | boolean/string | Whether dose is explicitly represented. |
| `time` | boolean/string | Whether treatment time is explicitly represented. |
| `patient_transfer` | boolean/string | Whether the method explicitly transfers to or predicts patient response. |
| `code` | boolean/string | Whether an implementation is linked from the curated resource entry. |

The Method Explorer is rendered at `docs/method-explorer.html`.

## Foundation Model Explorer profile

Foundation models shown in the Foundation Model Explorer may define a `foundation_profile` object in a modular enrichment fragment.

| Field | Type | Meaning |
|---|---|---|
| `year` | integer | Publication or release year used for navigation. |
| `modalities` | array of strings | Fine-grained modalities such as `scrna`, `bulk-rna`, `proteomics`, `mutation`, `methylation`, `atac`, `spatial`, `pathology`, `dna`, `rna`, `chemical`, or `protein`. |
| `params` | string or null | Human-readable parameter count or family range, e.g. `100M` or `1B / 7B / 40B`. |
| `params_millions` | number | Largest representative parameter count in millions, used only for sorting. |
| `pretraining_scale` | string or null | Human-readable summary of the pretraining corpus size. |
| `species` | array of strings | Species represented in pretraining or primary use. |
| `zero_shot` | boolean/string | Whether zero-shot use is explicitly supported; `limited` denotes task-dependent support. |
| `finetunable` | boolean/string | Whether fine-tuning or parameter-efficient adaptation is supported. |
| `weights` | boolean/string | Whether pretrained weights are publicly available. |
| `code` | boolean/string | Whether implementation code is publicly available. |
| `perturbation` | boolean/string | Whether perturbation prediction or in-silico perturbation is a supported use case. |
| `spatial` | boolean/string | Whether spatial data are directly modeled or supported. |

Unknown or unverified values should be omitted rather than inferred. The Foundation Model Explorer is rendered at `docs/foundation-explorer.html`.


## Agent Explorer profile

Agentic AI systems shown in the Agent Explorer may define an `agent_profile` object in a modular enrichment fragment.

| Field | Type | Meaning |
|---|---|---|
| `year` | integer | Initial public release or publication year. |
| `domains` | array of strings | Main scientific domains such as `general-biomedicine`, `therapeutics`, `bioinformatics`, `single-cell`, `scientific-workflow`, or `paper-to-agent`. |
| `architecture` | string | `single-agent`, `multi-agent`, or `agent-ecosystem`. |
| `tool_use` | boolean/string | Whether external scientific tools/APIs are used. |
| `code_execution` | boolean/string | Whether the system executes code as part of its workflow. |
| `web_retrieval` | boolean/string | Whether web or online database retrieval is supported. |
| `literature` | boolean/string | Whether literature search/reasoning is explicitly supported. |
| `omics` | boolean/string | Whether omics analysis is a first-class supported workflow. |
| `wet_lab` | boolean/string | Whether wet-lab planning, experimental design, or laboratory-facing workflows are supported. |
| `autonomous_experiment` | boolean/string | Whether the system can carry out iterative computational/experimental research loops. |
| `human_in_loop` | boolean/string | Whether human collaboration or approval is an explicit part of the design. |
| `open_source` | boolean/string | Whether implementation code is publicly available. |

Capability fields may use `limited` or `unknown` when support is workflow-dependent or not clearly documented. The Agent Explorer is rendered at `docs/agent-explorer.html`.
