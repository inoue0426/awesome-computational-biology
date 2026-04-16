# Contribution Guidelines

Contributions are welcome!

Please note that this project is released with a
[Contributor Code of Conduct](code-of-conduct.md). By participating in this
project you agree to abide by its terms.

## Pull Requests

- Search previous suggestions before making a new one, as yours may be a duplicate.
- Add one link per pull request.
- Prefer official and trustworthy sources (official docs, organization pages, maintained repositories, or official dataset pages).
- Include supporting technical evidence for new resources:
  - Ideally a peer-reviewed publication.
  - At minimum, a preprint or official technical documentation.
- Avoid submissions that are primarily promotional pages, generic blog posts, or opinion-only writeups.
- Add the link:
  - `[name](http://example.com/)` - A short description ends with a period.
  - Keep descriptions concise.
  - Maintain alphabetical ordering where applicable.
- Add a section if needed.
  - Add the section description.
  - Add the section title to the [Index](https://github.com/inoue0426/awesome-computational-biology#Contents).
- Check your spelling and grammar.
- Remove any trailing whitespace.
- Send a pull request with the reason why the addition is awesome.
- Use the following format for your pull request title:
  - Add user/repo - Short repo description

## Data Workflow (README and JSON)

- The curated source list is maintained in `README.md`.
- Machine-readable files are generated from README:
  - `python scripts/sync_resources_from_readme.py`
  - `python scripts/build_resources.py`
- For resource additions/edits, include updated generated files in the same PR:
  - `data/resources.yml`
  - `data/resources.json`
  - `data/resources.csv`
  - `docs/data/resources.json`
- Field definitions and naming rules are documented in [`docs/data/SCHEMA.md`](docs/data/SCHEMA.md).

## GitHub Pages UI

- The UI reads `docs/data/resources.json`.
- Search and filters are driven by these fields:
  - Search: `name`, `description`, `tasks`, `modalities`, `tags`
  - Filters: `type`, `tasks`, `modalities`

## Updates to Existing Links or Sections

- Improvements to the existing sections are welcome.
- If you think a listed link is not awesome, feel free to submit an issue or pull request to begin the discussion.
- Broken links are checked by CI; if you find one, please submit a fix to the canonical URL (or remove the entry if no stable canonical URL exists).

## Updating your PR

A lot of times, making a PR adhere to the standards above can be difficult.
If the maintainers notice anything that we'd like changed, we'll ask you to
edit your PR before we merge it. There's no need to open a new PR, just edit
the existing one. If you're not sure how to do that,
[here is a guide](https://github.com/RichardLitt/knowledge/blob/master/github/amending-a-commit-guide.md)
on the different ways you can update your PR so that we can merge it.
