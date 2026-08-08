# AI4Bio Resource Schema v2

This document defines the richer landscape metadata layered on top of the curated Awesome Computational Biology list.

## Source model

The repository intentionally separates **membership/basic metadata** from **landscape enrichment**:

1. `README.md` is the canonical curated resource list.
2. `scripts/sync_resources_from_readme.py` derives `data/resources.yml` from README headings and bullets.
3. `data/enrichment.yml` stores richer metadata keyed by stable resource `id`.
4. `data/vocabulary.yml` defines canonical terms for controlled enrichment dimensions.
5. `scripts/build_resources.py` merges base records and enrichment, validates them, and writes `data/resources.json`, `data/resources.csv`, and `docs/data/resources.json`.

This separation prevents hand-curated AI4Bio metadata from being erased by README synchronization.

## Core identity fields

These fields are required and may not be overridden by `data/enrichment.yml`:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable lowercase `snake_case` identifier |
| `name` | string | Official display name |
| `type` | enum | `api`, `benchmark`, `database`, `model`, `resource`, or `toolkit` |
| `url` | URL | Canonical landing page |
| `description` | string | Short factual description |

## Landscape dimensions

| Field | Type | Meaning |
|---|---|---|
| `tasks` | string[] | Biological or ML tasks performed |
| `modalities` | string[] | Input/output data modalities |
| `organism` | string[] | Covered organisms or species groups |
| `entities` | string[] | Biological entities: gene, protein, compound, cell, disease, etc. |
| `methods` | string[] | Method families: transformer, GNN, diffusion, optimal transport, etc. |
| `tags` | string[] | Broad domain and curation labels |
| `organizations` | string[] | Organizations maintaining or primarily responsible for the resource |

These dimensions are deliberately orthogonal. Do not encode a task as a modality or a biological entity as a resource type.

## Controlled vocabulary

New values added through `data/enrichment.yml` for `entities`, `methods`, `modalities`, and `tasks` must use canonical terms from `data/vocabulary.yml`.

Canonical terms use lowercase kebab-case, for example:

```yaml
entities: [cell, gene]
methods: [transformer, self-supervised-learning]
modalities: [single-cell-rna-seq, transcriptomics]
tasks: [foundation-model-pretraining, cell-type-annotation]
```

This rule is intentionally applied only to enrichment metadata. Existing README-derived values remain valid for backward compatibility and can be migrated separately without blocking routine resource updates.

When a required concept is missing, add a reusable canonical term to `data/vocabulary.yml` instead of inventing a one-off spelling in an enrichment record. `tags`, `organism`, and `organizations` remain free-form because their vocabularies are broader or context dependent.

## Provenance and lifecycle fields

| Field | Type | Meaning |
|---|---|---|
| `year` | integer | Initial public release or primary publication year |
| `github` | URL | Source repository when available |
| `documentation` | URL | Documentation landing page |
| `paper` | URL | Primary publication or preprint |
| `license` | string | SPDX identifier preferred |
| `api` | boolean | Programmatic API availability |
| `access` | enum | `open`, `registration`, `restricted`, `commercial`, `unknown` |
| `maintenance_status` | enum | `active`, `maintenance`, `archived`, `unknown` |
| `updated` | date | Last-known upstream update date |
| `last_checked` | date | Date this repository verified the metadata |
| `metadata_sources` | URL[] | Sources supporting enriched metadata |

`last_checked` is a curation timestamp, not an upstream release date. `updated` should only be populated when an upstream update date is known.

## Enrichment rules

`data/enrichment.yml` is a mapping keyed by resource id:

```yaml
resources:
  example_resource:
    entities: [gene, disease]
    methods: [transformer]
    organizations: [Example Lab]
    year: 2025
    github: https://github.com/example/project
    documentation: https://example.org/docs
    maintenance_status: active
    access: open
    last_checked: 2026-08-08
    metadata_sources:
      - https://example.org/about
```

Enrichment cannot override `id`, `name`, `type`, `url`, or `description`. A referenced id must already exist in `data/resources.yml`.

## Validation contract

`python scripts/validate_resources.py` checks:

- required fields and field types;
- stable id format and id uniqueness;
- allowed enum values;
- HTTP(S) URL shape;
- ISO `YYYY-MM-DD` dates;
- list uniqueness and non-empty values;
- enrichment references and forbidden identity overrides;
- controlled enrichment terms against `data/vocabulary.yml`;
- vocabulary uniqueness and lowercase kebab-case normalization;
- unknown field names.

The machine-readable resource counterpart is `docs/data/resource.schema.json` (JSON Schema 2020-12). Controlled vocabulary enforcement is performed at the enrichment layer because legacy README-derived values intentionally remain backward compatible.

## Curation guidance

Prefer verified metadata over exhaustive metadata. Unknown fields should be omitted rather than guessed. For facts likely to change, include `last_checked` and at least one `metadata_sources` URL. Dynamic popularity metrics such as GitHub stars should remain generated telemetry rather than canonical curated fields.
