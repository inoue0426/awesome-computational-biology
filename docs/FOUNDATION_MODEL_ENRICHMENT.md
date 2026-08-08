# Foundation Model Enrichment

This document tracks the first curated metadata-enrichment pass for AI4Bio foundation models.

## Scope

The initial pass focuses on representative single-cell and transcriptomics foundation models already present in the resource registry, beginning with:

- scGPT
- Geneformer

The scope may be expanded incrementally once the curation rules below are validated in practice.

## Curation rules

Metadata must be supported by at least one primary or official source:

- official project repository or model card;
- official documentation;
- primary peer-reviewed publication or preprint.

Unknown or ambiguous metadata is omitted rather than inferred.

For each resource, curate fields where evidence is available:

- `entities`
- `methods`
- `organizations`
- `year`
- `github`
- `documentation`
- `maintenance_status`
- `last_checked`
- `metadata_sources`

`maintenance_status` should only be marked `active` when there is direct evidence of ongoing maintenance, such as a recent official release or repository activity. Otherwise use `unknown` or omit the field.

## Initial evidence targets

### scGPT

Primary evidence should include the official `bowang-lab/scGPT` repository and the Nature Methods publication.

### Geneformer

Primary evidence should include the official `ctheodoris/Geneformer` model repository/model card and the primary Nature publication.

## Completion criteria

A resource is considered enriched when:

1. all added metadata is supported by `metadata_sources`;
2. no unsupported organization, method, year, or maintenance claim is introduced;
3. generated JSON/CSV artifacts are regenerated and committed;
4. schema validation and resource-consistency CI checks pass.

## Provenance

This enrichment pass is being prepared with assistance from OpenAI GPT-5.6 Sol. Final metadata is intended to remain source-verifiable and reviewable through the recorded provenance URLs.
