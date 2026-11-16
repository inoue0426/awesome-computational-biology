# Agent instructions

These instructions apply to the entire `awesome-computational-biology` repository.
They are for AI assistants and automated curation (including the ChatGPT weekly
maintenance task). Follow them before editing resources or creating a PR.

## Project purpose and scope

Maintain a curated, usable collection of computational biology and biomedical
AI resources. Prioritize high-quality, reproducible resources over quantity:
datasets, benchmarks, foundation models, perturbation and drug-response models,
biological AI agents, and practical databases and tools. Focus especially on
single-cell and spatial omics, biological interventions, patient treatment
response, and clinically relevant transfer evaluation, while retaining the
repository's broader computational biology coverage.

Do not equate an interesting paper with a usable resource. Do not add a claim
about availability, performance, size, release date, or clinical validation
unless a primary source supports it.

## Check before making changes

1. Read `README.md`, `scripts/sync_resources_from_readme.py`,
   `scripts/build_resources.py`, `scripts/build_resources_v2.py`,
   `scripts/validate_resources.py`, `data/vocabulary.yml`, and relevant
   `data/enrichment*.yml` fragments. Check existing CI workflows.
2. Check the current default branch and open PRs, especially those affecting
   resources, before adding new items.
3. Search existing README entries and `data/resources.yml` plus enrichment
   files for matching names, canonical URLs, GitHub repositories, DOIs, and
   renamed versions. Update an existing entry rather than duplicate it.
4. Verify candidate sources directly: original article or preprint, official
   project website, dataset record and/or maintained source repository.
   Distinguish peer-reviewed publications from preprints and announcements.
5. If the resource cannot be verified or its metadata is contradictory, skip
   it or leave the PR for manual review. Never manufacture references.

## Resource selection criteria

- Prefer genuinely new, influential, or uniquely useful datasets, benchmarks,
  methods, foundation models, agents, and reproducible toolkits.
- For **datasets**, verify modality, organism, sample source, size and unit
  (cells versus samples versus independent patients), access conditions,
  interventions, matched pre/post availability, and outcomes if stated.
- For **perturbation datasets**, distinguish single-cell measurements from
  bulk or cell viability, observed versus simulated treatment changes, and
  drug, dose, timing, and cellular context coverage.
- For **models**, record their task, training source, intended inputs/outputs,
  code/weights availability, known limitations and generalization claims.
- For **benchmarks**, check splitting strategy (drug-OOD, cell-OOD, source-OOD,
  patient-OOD, etc.), targets, metrics, and whether clinical outcomes were
  actually evaluated.
- For **agents**, distinguish released software from demonstrations and
  evaluate tool availability, reproducibility and domain fit.
- Separate *cell-line-to-patient drug sensitivity transfer*, *drug-induced
  molecular-state prediction* and *actual patient clinical response*. Do not
  claim one task establishes the others.
- Prefer concise, neutral one-line descriptions. Use verifiable scale numbers
  only with explicit units. Never advertise unverified superiority.

## Canonical data workflow

**README.md is the curated source of resource identity and placement.** Its
resource bullet syntax is parsed by the sync script:

```markdown
- [Resource Name](https://official-resource-url) — Concise factual description.
```

Place each resource under the correct existing heading. The parser derives
`id`, `type`, `tags`, `tasks`, and `modalities` from these headings;
do not hand-invent an ID without checking the generated slug and duplicates.

**Do not hand-edit machine-generated JSON/CSV artifacts.**

1. Edit the manually curated list in `README.md`.
2. Run `scripts/sync_resources_from_readme.py` to regenerate
   `data/resources.yml`. Do not maintain entries in both places independently.
3. Put optional metadata (e.g., `dataset_profile`, `method_profile`,
   `foundation_profile`, `agent_profile`, `paper`, `github`,
   `metadata_sources`, `last_checked`) in an appropriate
   `data/enrichment.*.yml` fragment keyed by the **generated** resource ID.
   Do not override identity fields in enrichment.
4. Use `data/vocabulary.yml` for canonical `entities`, `methods`,
   `modalities`, and `tasks`. Prefer existing valid values. Respect schema
   types and enumerations; for example, descriptive sample counts can require
   strings rather than numbers.
5. Run the canonical builder to generate `data/resources.json`,
   `data/resources.csv`, and `docs/data/resources.json` together.
6. If spellcheck flags a legitimate new scientific proper name, add only that
   exact name to `cspell.json`, rather than weakening spellcheck broadly.

## Validation

From the repository root (with `uv` available):

```bash
uv run --with 'PyYAML' python scripts/sync_resources_from_readme.py
uv run --with 'PyYAML' python scripts/validate_resources.py
uv run --with 'PyYAML' python scripts/build_resources.py
git diff --check
git status --short
```

Review the full generated diff. Confirm that there are no duplicate resources,
invalid metadata, misleading claims, unexpected deletions, unrelated changes or
unsynchronized artifacts. Run any additional tests appropriate to the changes.

The repository's GitHub Actions checks are authoritative for merging.
In particular, check schema validation, docs lint, artifact generation and
resource consistency. A green check for only part of the suite is insufficient.

## PR and merge policy

- Create a **separate branch and a focused PR** for each coherent update.
  Include primary-source links, a short explanation of what was added, and
  validation results. Do not push directly to `main`.
- In automated weekly curation, prefer a small, high-confidence batch. When
  nothing trustworthy qualifies, report no change rather than creating filler.
- Do not overwrite another contributor's work or amend unrelated PRs.
- Automated merging is permitted **only** for a resource-only PR that has
  passed all applicable required CI checks and has no merge conflict,
  unresolved factual concern, or repository rule blocking merge.
- Never bypass branch protection, force-push, disable checks, or alter repo
  permissions to make a PR pass. Stop and report the blocker if checks cannot
  run, permissions are missing, or evidence is inconclusive.
- After merge, report the exact PR and merged status. Never claim a merge
  succeeded unless GitHub confirms it.

## Weekly ChatGPT maintenance

On each scheduled run, **read this `AGENTS.md` from the repository's current
default branch first**, then follow the normal review, curation, generation,
validation, PR, and merge workflow above. Compare candidate resources against
existing entries and prior merged PRs. Never assume a scheduled ChatGPT task
is itself a GitHub Actions workflow. Report useful additions, skipped uncertain
items, the PR URL, CI outcome, and actual merge status.
