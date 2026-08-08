# AI4Bio Landscape Database

The landscape view treats the existing computational biology registry as a multidimensional database rather than a single hierarchical list.

## Design goals

- Keep the current curated resource records and generation pipeline intact.
- Expose orthogonal facets so one resource can be explored by resource type, biological/ML task, data modality, organism, and domain tag.
- Make the landscape useful without introducing a server or build-time dependency.
- Keep the data model extensible for richer AI4Bio metadata over time.

## Current facet model

The landscape UI derives the following dimensions from `docs/data/resources.json`:

| Dimension | Source field | Example values |
|---|---|---|
| Resource type | `type` | `database`, `benchmark`, `model`, `toolkit`, `api` |
| Task | `tasks` | `drug-response-prediction`, `cell-type-annotation`, `molecular-generation` |
| Modality | `modalities` | `transcriptomics`, `spatial-transcriptomics`, `protein-sequence` |
| Organism | `organism` | `human`, `mouse`, `multi-species` |
| Domain/tag | `tags` | `drug-discovery`, `single-cell`, `foundation-model` |

These are deliberately treated as separate axes. A model can therefore be, for example, a `model` that performs `perturbation-prediction` on `single-cell-rna-seq` data for `human` and carry tags such as `drug-discovery` and `foundation-model`.

## Recommended schema evolution

The current schema is compatible with a richer landscape database. New fields should be added incrementally and only when they can be curated consistently.

Suggested fields:

| Field | Type | Purpose |
|---|---|---|
| `entities` | array of strings | Biological entities such as `gene`, `protein`, `compound`, `cell`, `disease` |
| `methods` | array of strings | Method families such as `transformer`, `gnn`, `diffusion`, `optimal-transport` |
| `organizations` | array of strings | Primary organizations responsible for the resource |
| `year` | integer | Initial public release/publication year |
| `github` | string | Source repository when distinct from the canonical landing page |
| `documentation` | string | Documentation URL |
| `maintenance_status` | string | Curated status such as `active`, `maintenance`, `archived`, `unknown` |
| `last_checked` | string | Date the metadata/link was last manually or automatically checked |

Avoid adding dynamic popularity metrics such as GitHub stars directly to canonical records unless a reproducible refresh pipeline is introduced. Such values become stale quickly and should be stored as generated metadata rather than curated facts.

## Canonical-source policy

At present, `README.md` is the canonical curated list, with generated YAML/JSON/CSV artifacts. The landscape page intentionally consumes `docs/data/resources.json` without changing that policy.

A future migration may make `data/resources.yml` the canonical source once all README-only categorization semantics can be represented explicitly in structured fields. That migration should be a separate change because it changes contribution workflow and source-of-truth semantics.

## Landscape page

Open `docs/landscape.html` through GitHub Pages. It provides:

- full-text search across names, descriptions, tasks, modalities, organisms, and tags;
- filters for type, task, modality, organism, and tag;
- summary counts for resources and major dimensions;
- frequency bars recalculated for the current filtered result set;
- direct resource and paper links;
- client-side rendering with no additional dependencies.
