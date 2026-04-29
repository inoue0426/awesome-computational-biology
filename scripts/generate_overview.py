#!/usr/bin/env python3
"""Generate an overview figure of the Awesome Computational Biology resource landscape.

Usage:
    python scripts/generate_overview.py

Output:
    docs/overview.png  — static PNG embedded in the web overview page

Requirements:
    pip install matplotlib       # or: pip install -r scripts/requirements.txt
"""

import json
import sys
from collections import Counter
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
except ImportError:
    print("ERROR: matplotlib is not installed. Run: pip install matplotlib", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = REPO_ROOT / "docs" / "data" / "resources.json"
OUTPUT_FILE = REPO_ROOT / "docs" / "overview.png"

# ---------------------------------------------------------------------------
# Colour palette (consistent with docs/styles.css)
# ---------------------------------------------------------------------------
TYPE_COLORS = {
    "database":  "#2a9d8f",
    "model":     "#2c7be5",
    "toolkit":   "#e9c46a",
    "benchmark": "#9b5de5",
    "api":       "#e76f51",
}
DEFAULT_COLOR = "#adb5bd"

TASK_COLOR     = "#3a86ff"
MODALITY_COLOR = "#06d6a0"


def load_resources(path: Path) -> list[dict]:
    if not path.exists():
        print(f"ERROR: {path} not found. Run build_resources.py first.", file=sys.stderr)
        sys.exit(1)
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        print("ERROR: resources.json must be a JSON array.", file=sys.stderr)
        sys.exit(1)
    return data


def count_by_field(resources: list[dict], field: str) -> Counter:
    counter: Counter = Counter()
    for r in resources:
        value = r.get(field)
        if isinstance(value, list):
            for v in value:
                counter[v] += 1
        elif value:
            counter[value] += 1
    return counter


def main() -> None:
    resources = load_resources(INPUT_FILE)

    type_counts     = count_by_field(resources, "type")
    task_counts     = count_by_field(resources, "tasks")
    modality_counts = count_by_field(resources, "modalities")

    top_tasks     = task_counts.most_common(10)
    top_modalities = modality_counts.most_common(10)

    # ── Figure layout ────────────────────────────────────────────────────
    fig = plt.figure(figsize=(16, 11))
    fig.patch.set_facecolor("#f8f9fa")

    gs = fig.add_gridspec(
        2, 2,
        left=0.07, right=0.97,
        top=0.88, bottom=0.06,
        hspace=0.45, wspace=0.35,
    )

    ax_type     = fig.add_subplot(gs[0, 0])
    ax_task     = fig.add_subplot(gs[0, 1])
    ax_modality = fig.add_subplot(gs[1, 0])
    ax_summary  = fig.add_subplot(gs[1, 1])

    # ── Shared helper ─────────────────────────────────────────────────────
    def style_ax(ax: plt.Axes) -> None:
        ax.set_facecolor("#ffffff")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#dee2e6")
        ax.spines["bottom"].set_color("#dee2e6")
        ax.tick_params(colors="#6c757d", labelsize=9)

    # ── 1. Resources by type (vertical bar) ───────────────────────────────
    types  = [t for t, _ in type_counts.most_common()]
    counts = [type_counts[t] for t in types]
    colors = [TYPE_COLORS.get(t, DEFAULT_COLOR) for t in types]

    bars = ax_type.bar(types, counts, color=colors, edgecolor="white", linewidth=1.2)
    for bar, cnt in zip(bars, counts):
        ax_type.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.8,
            str(cnt),
            ha="center", va="bottom",
            fontsize=9, color="#495057", fontweight="bold",
        )
    ax_type.set_title("Resources by Type", fontsize=11, fontweight="bold", color="#212529", pad=8)
    ax_type.set_ylabel("Count", fontsize=9, color="#6c757d")
    ax_type.set_ylim(0, max(counts) * 1.18)
    style_ax(ax_type)

    # ── 2. Top 10 tasks (horizontal bar) ──────────────────────────────────
    task_labels  = [t for t, _ in reversed(top_tasks)]
    task_values  = [c for _, c in reversed(top_tasks)]

    h_bars = ax_task.barh(task_labels, task_values, color=TASK_COLOR, edgecolor="white")
    for bar, cnt in zip(h_bars, task_values):
        ax_task.text(
            bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
            str(cnt), va="center", fontsize=8, color="#495057",
        )
    ax_task.set_title("Top 10 Tasks", fontsize=11, fontweight="bold", color="#212529", pad=8)
    ax_task.set_xlabel("Count", fontsize=9, color="#6c757d")
    ax_task.set_xlim(0, max(task_values) * 1.18)
    style_ax(ax_task)
    ax_task.tick_params(axis="y", labelsize=8)

    # ── 3. Top 10 modalities (horizontal bar) ─────────────────────────────
    mod_labels = [m for m, _ in reversed(top_modalities)]
    mod_values = [c for _, c in reversed(top_modalities)]

    h_bars2 = ax_modality.barh(mod_labels, mod_values, color=MODALITY_COLOR, edgecolor="white")
    for bar, cnt in zip(h_bars2, mod_values):
        ax_modality.text(
            bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
            str(cnt), va="center", fontsize=8, color="#495057",
        )
    ax_modality.set_title("Top 10 Modalities", fontsize=11, fontweight="bold", color="#212529", pad=8)
    ax_modality.set_xlabel("Count", fontsize=9, color="#6c757d")
    ax_modality.set_xlim(0, max(mod_values) * 1.18)
    style_ax(ax_modality)
    ax_modality.tick_params(axis="y", labelsize=8)

    # ── 4. Summary stats ──────────────────────────────────────────────────
    ax_summary.set_facecolor("#ffffff")
    ax_summary.axis("off")

    total        = len(resources)
    n_tasks      = len(task_counts)
    n_modalities = len(modality_counts)
    n_types      = len(type_counts)

    summary_items = [
        ("Total Resources",    str(total),       "#2c7be5"),
        ("Resource Types",    str(n_types),      "#2a9d8f"),
        ("Unique Tasks",       str(n_tasks),      "#9b5de5"),
        ("Unique Modalities",  str(n_modalities), "#e76f51"),
    ]

    for i, (label, value, color) in enumerate(summary_items):
        y = 0.82 - i * 0.22
        ax_summary.text(0.08, y + 0.04, value, fontsize=26, fontweight="bold",
                        color=color, va="center", transform=ax_summary.transAxes)
        ax_summary.text(0.08, y - 0.06, label, fontsize=9, color="#6c757d",
                        va="center", transform=ax_summary.transAxes)

    # legend for type colours
    patches = [
        mpatches.Patch(color=c, label=t.capitalize())
        for t, c in TYPE_COLORS.items()
    ]
    ax_summary.legend(
        handles=patches, loc="lower center", ncol=3,
        fontsize=8, frameon=False,
        title="Resource Types", title_fontsize=8,
    )

    # ── Super-title ──────────────────────────────────────────────────────
    fig.suptitle(
        "Awesome Computational Biology — Resource Landscape",
        fontsize=14, fontweight="bold", color="#212529", y=0.95,
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Overview figure saved → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
