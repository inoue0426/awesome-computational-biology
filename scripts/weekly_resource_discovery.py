#!/usr/bin/env python3
"""Conservatively discover *peer-reviewed*, code-backed biological AI resources.

No LLM or third-party repository code is executed. Publications must have an
indexed DOI and mention a concrete public GitHub repository in their abstract.
Uncertain or duplicate candidates are skipped. README is the canonical source.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

README = Path("README.md")
API = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
REPO_API = "https://api.github.com/repos/"
MAX_ADDITIONS = 3
LOOKBACK_DAYS = 14
USER_AGENT = "awesome-computational-biology-weekly-curator/1.0"
GITHUB_RE = re.compile(
    r"https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)",
    re.IGNORECASE,
)
RESOURCE_RE = re.compile(
    r"\b(benchmark|database|atlas|dataset|resource|foundation model|"
    r"deep learning model|machine learning model|software|toolkit)\b",
    re.IGNORECASE,
)
BIO_RE = re.compile(
    r"\b(single.cell|transcriptom|proteom|genom|perturb|bioinformatic|"
    r"protein|drug|cancer|molecular|spatial omics)\b",
    re.IGNORECASE,
)
EXCLUDE_RE = re.compile(
    r"\b(review|perspective|editorial|protocol|commentary|correction|retraction)\b",
    re.IGNORECASE,
)
BULLET_RE = re.compile(r"^- \[(.+?)\]\((.+?)\) — ")
HEADINGS = {
    "dataset": "### General Biological ML & Knowledge Graph Benchmarks",
    "model": "#### Multi-Modal Foundation Models",
    "toolkit": "## Preprocessing Tools",
}


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.load(response)


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]*>", " ", value or ""))).strip()


def normalize_repo(url: str) -> str | None:
    match = GITHUB_RE.match(url.strip())
    if not match:
        return None
    owner, name = match.groups()
    name = name.removesuffix(".git").rstrip(".")
    if owner.lower() in {"topics", "features", "orgs", "settings", "marketplace"}:
        return None
    if name.lower() in {"issues", "pulls", "actions", "releases", "wiki"}:
        return None
    return f"https://github.com/{owner.lower()}/{name.lower()}"


def classify(title: str) -> tuple[str, str] | None:
    if not RESOURCE_RE.search(title) or not BIO_RE.search(title) or EXCLUDE_RE.search(title):
        return None
    lower = title.lower()
    if re.search(r"\b(database|benchmark|atlas|dataset|resource)\b", lower):
        kind = "dataset"
    elif re.search(r"\b(software|toolkit)\b", lower):
        kind = "toolkit"
    elif re.search(r"\b(model|deep learning)\b", lower):
        kind = "model"
    else:
        return None
    area = (
        "single-cell and perturbation biology" if re.search(r"single.cell|perturb", lower)
        else "computational biology"
    )
    return kind, area


def extract_candidate(article: dict) -> dict | None:
    title = clean(article.get("title", ""))
    abstract = clean(article.get("abstractText", ""))
    doi = (article.get("doi") or "").strip().lower()
    journal = clean(article.get("journalTitle", "") or article.get("journalInfo", {}).get("journal", {}).get("title", ""))
    date = article.get("firstPublicationDate") or ""
    if (not doi.startswith("10.") or len(title) > 115 or len(title) < 14
            or not date or not abstract or not journal or article.get("isRetracted") is True):
        return None
    category = classify(title)
    if category is None:
        return None
    match = GITHUB_RE.search(abstract)
    if not match:
        return None
    repo = normalize_repo(match.group(0))
    if not repo:
        return None
    kind, area = category
    # Authorship and availability are supported by the indexed record. Avoid
    # synthesizing any biological results or performance claims from abstracts.
    year = date[:4]
    description = (
        f"{kind.capitalize()} for {area}; published in {journal} ({year}). "
        f"DOI: https://doi.org/{doi}"
    )
    if len(description) > 280 or "]" in title or "[" in title or "\n" in title:
        return None
    return {"name": title, "url": repo, "doi": doi, "category": kind, "description": description}


def existing_resources(readme: str) -> tuple[set[str], set[str]]:
    names, repos = set(), set()
    for line in readme.splitlines():
        m = BULLET_RE.match(line)
        if not m:
            continue
        names.add(clean(m.group(1)).casefold())
        repo = normalize_repo(m.group(2))
        if repo:
            repos.add(repo)
    return names, repos


def verify_repo(url: str) -> bool:
    # Only GitHub's public REST API, never URLs furnished by an abstract.
    path = url.removeprefix("https://github.com/")
    try:
        result = fetch_json(REPO_API + path)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as error:
        print(f"Skip unverifiable repository {url}: {error}", file=sys.stderr)
        return False
    full_name = result.get("full_name", "").lower()
    return (
        full_name == path
        and not result.get("archived", False)
        and not result.get("disabled", False)
        and result.get("private") is False
    )


def add_resources(readme: str, candidates: list[dict]) -> str:
    # Insert directly after a known heading; no arbitrary HTML, Markdown, or shell.
    for candidate in reversed(candidates):
        heading = HEADINGS[candidate["category"]]
        if heading not in readme:
            raise RuntimeError(f"README heading absent: {heading}")
        line = f"- [{candidate['name']}]({candidate['url']}) — {candidate['description']}\n"
        readme = readme.replace(heading + "\n", heading + "\n" + line, 1)
    return readme


def discover(today: dt.date, readme: str, max_additions: int = MAX_ADDITIONS) -> list[dict]:
    start = today - dt.timedelta(days=LOOKBACK_DAYS)
    query = (
        f'FIRST_PDATE:[{start.isoformat()} TO {today.isoformat()}] '
        'AND SRC:MED '
        'AND (TITLE:benchmark OR TITLE:database OR TITLE:atlas '
        'OR TITLE:dataset OR TITLE:"foundation model" OR TITLE:toolkit) '
        'AND NOT PUB_TYPE:review'
    )
    params = urllib.parse.urlencode({
        "query": query, "format": "json", "resultType": "core",
        "pageSize": "100", "sort": "FIRST_PDATE_D desc"
    })
    results = fetch_json(API + "?" + params).get("resultList", {}).get("result", [])
    old_names, old_repos = existing_resources(readme)
    selected, seen_dois = [], set()
    for item in results:
        candidate = extract_candidate(item)
        if not candidate or candidate["doi"] in seen_dois:
            continue
        seen_dois.add(candidate["doi"])
        if candidate["name"].casefold() in old_names or candidate["url"] in old_repos:
            continue
        if any(x["url"] == candidate["url"] for x in selected):
            continue
        if not verify_repo(candidate["url"]):
            continue
        selected.append(candidate)
        if len(selected) >= max_additions:
            break
    return selected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--readme", type=Path, default=README)
    parser.add_argument("--today", type=dt.date.fromisoformat, default=dt.datetime.now(dt.timezone.utc).date())
    parser.add_argument("--max-additions", type=int, default=MAX_ADDITIONS)
    args = parser.parse_args()
    if not 1 <= args.max_additions <= MAX_ADDITIONS:
        parser.error(f"--max-additions must be 1..{MAX_ADDITIONS}")
    content = args.readme.read_text(encoding="utf-8")
    candidates = discover(args.today, content, args.max_additions)
    if candidates:
        args.readme.write_text(add_resources(content, candidates), encoding="utf-8")
    print(json.dumps({"date": args.today.isoformat(), "added": candidates}, indent=2))


if __name__ == "__main__":
    main()
