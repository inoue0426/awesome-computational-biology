# AI4Bio data files

- `resources.json`: generated merged resource registry consumed by GitHub Pages.
- `resource.schema.json`: JSON Schema 2020-12 contract for one resource object.
- `SCHEMA.md`: original schema notes.
- `SCHEMA_V2.md`: richer AI4Bio landscape schema and enrichment workflow.

The enriched build path is `scripts/build_resources_v2.py`, which combines `data/resources.yml` with `data/enrichment.yml` and runs `scripts/validate_resources.py` before writing artifacts.
