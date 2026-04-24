"""
Stage 4b chart generation.

Three functions write SVGs to evaluations/charts/:
  - generate_cost_trend_chart(df)       cost over last 30 runs
  - generate_token_usage_chart(df)      stacked tokens over last 30 runs
  - generate_weekly_rollup_chart(dir)   last 7 days' category + confidence

All charts render with transparent backgrounds so they work on both
light and dark GitHub themes. The weekly rollup parses each memo's
markdown once and caches the result in a _parsed.json sidecar so
repeat runs are cheap and idempotent.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")  # headless; no display required

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


# Paths and constants ---------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
EVALUATIONS_DIR = ROOT / "evaluations"
CHARTS_DIR = EVALUATIONS_DIR / "charts"

LAST_N_RUNS = 30
WEEKLY_WINDOW_DAYS = 7

# Pricing constants duplicated from generate_hypotheses.py so this module
# can be imported independently (e.g., from the weekly workflow).
PRICE_INPUT = 3.00
PRICE_CACHE_READ = 0.30

CATEGORIES = [
    "Performance",
    "Profitability",
    "Efficiency",
    "Leverage",
    "Liquidity",
    "DuPont",
    "Macro/Strategic",
]
CONFIDENCE_LEVELS = ["Low", "Medium", "High"]

# Normalize common output variants back to the canonical tag.
_CATEGORY_ALIASES = {
    "macro": "Macro/Strategic",
    "strategic": "Macro/Strategic",
    "macro/strategic": "Macro/Strategic",
    "macro / strategic": "Macro/Strategic",
    "du pont": "DuPont",
    "dupont": "DuPont",
}


# Muted professional palette; steady across charts. -------------------
PALETTE = {
    "primary": "#2E5C8A",      # deep steel blue — actual values
    "accent": "#8AA686",       # sage green — savings / positive deltas
    "input": "#6B8FA8",        # lighter blue — input tokens
    "output": "#B87A5F",       # warm terracotta — output tokens
    "cache": "#8AA686",        # sage green — cache reads
    "confidence_low": "#C4A05C",
    "confidence_medium": "#6B8FA8",
    "confidence_high": "#4A7C59",
    "axis": "#555555",
    "grid": "#CCCCCC",
    "text": "#333333",
}


# Regex parsers --------------------------------------------------------

_CATEGORY_RE = re.compile(r"^\*\*Category:\*\*\s*(.+?)\s*$", re.MULTILINE)
_CONFIDENCE_RE = re.compile(r"^\*\*Confidence:\*\*\s*(.+?)\s*$", re.MULTILINE)


# Styling helpers ------------------------------------------------------

def _style_axes(ax: plt.Axes, *, grid: bool = True) -> None:
    ax.set_facecolor("none")
    for spine_name, spine in ax.spines.items():
        if spine_name in ("top", "right"):
            spine.set_visible(False)
        else:
            spine.set_color(PALETTE["axis"])
            spine.set_linewidth(0.8)
    ax.tick_params(colors=PALETTE["axis"], labelsize=11)
    ax.xaxis.label.set_color(PALETTE["axis"])
    ax.yaxis.label.set_color(PALETTE["axis"])
    ax.xaxis.label.set_size(12)
    ax.yaxis.label.set_size(12)
    if grid:
        ax.grid(True, axis="y", color=PALETTE["grid"], linewidth=0.6, alpha=0.6)
        ax.set_axisbelow(True)


def _save_svg(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.patch.set_alpha(0)
    fig.savefig(
        path,
        format="svg",
        transparent=True,
        bbox_inches="tight",
        facecolor="none",
    )
    plt.close(fig)


def _empty_placeholder(path: Path, title: str, message: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 3))
    _style_axes(ax, grid=False)
    ax.set_title(title, fontsize=14, color=PALETTE["text"], loc="left")
    ax.text(
        0.5,
        0.5,
        message,
        ha="center",
        va="center",
        transform=ax.transAxes,
        fontsize=12,
        color=PALETTE["axis"],
        style="italic",
    )
    ax.set_xticks([])
    ax.set_yticks([])
    _save_svg(fig, path)


def _prep_metrics_df(df: pd.DataFrame) -> pd.DataFrame:
    """Parse timestamps, sort, trim to last N runs."""
    working = df.copy()
    working["timestamp_utc"] = pd.to_datetime(working["timestamp_utc"], utc=True)
    working = working.sort_values("timestamp_utc").tail(LAST_N_RUNS)
    return working.reset_index(drop=True)


# Chart 1: cost trend --------------------------------------------------

def generate_cost_trend_chart(metrics_df: pd.DataFrame) -> Path:
    """
    Line chart of run cost over time, with a second line showing the
    dollar value saved by cache-read pricing (vs. billing those tokens
    as full-price input).
    """
    path = CHARTS_DIR / "cost_trend.svg"

    if metrics_df is None or metrics_df.empty:
        _empty_placeholder(
            path, "Run cost over time", "Insufficient data (no runs yet)"
        )
        return path

    df = _prep_metrics_df(metrics_df)
    df["cache_savings"] = (
        df["cache_read_tokens"] * (PRICE_INPUT - PRICE_CACHE_READ) / 1_000_000
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    _style_axes(ax)

    ax.plot(
        df["timestamp_utc"],
        df["cost_usd"],
        color=PALETTE["primary"],
        marker="o",
        markersize=4,
        linewidth=1.6,
        label="Actual cost",
    )
    ax.plot(
        df["timestamp_utc"],
        df["cache_savings"],
        color=PALETTE["accent"],
        marker="s",
        markersize=3,
        linewidth=1.2,
        linestyle="--",
        label="Cache-read savings",
    )

    # Annotate the most recent actual-cost point.
    last = df.iloc[-1]
    ax.annotate(
        f"${last['cost_usd']:.4f}",
        xy=(last["timestamp_utc"], last["cost_usd"]),
        xytext=(6, 6),
        textcoords="offset points",
        fontsize=11,
        color=PALETTE["primary"],
        fontweight="bold",
    )

    ax.set_title(
        "Run cost over time", fontsize=14, color=PALETTE["text"], loc="left"
    )
    ax.set_ylabel("USD")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.legend(
        loc="upper left",
        frameon=False,
        fontsize=11,
        labelcolor=PALETTE["text"],
    )

    fig.autofmt_xdate(rotation=0, ha="center")
    _save_svg(fig, path)
    return path


# Chart 2: token usage -------------------------------------------------

def generate_token_usage_chart(metrics_df: pd.DataFrame) -> Path:
    """Stacked bar chart of input / output / cache tokens per run."""
    path = CHARTS_DIR / "token_usage.svg"

    if metrics_df is None or metrics_df.empty:
        _empty_placeholder(
            path, "Token usage per run", "Insufficient data (no runs yet)"
        )
        return path

    df = _prep_metrics_df(metrics_df)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    _style_axes(ax)

    # Use numeric positions to keep bars evenly spaced regardless of
    # irregular run cadence; label each bar with its UTC date.
    x = range(len(df))
    width = 0.6

    inputs = df["input_tokens"].to_numpy()
    outputs = df["output_tokens"].to_numpy()
    caches = df["cache_read_tokens"].to_numpy()

    ax.bar(x, inputs, width, color=PALETTE["input"], label="Input")
    ax.bar(
        x,
        outputs,
        width,
        bottom=inputs,
        color=PALETTE["output"],
        label="Output",
    )
    ax.bar(
        x,
        caches,
        width,
        bottom=inputs + outputs,
        color=PALETTE["cache"],
        label="Cache read",
    )

    ax.set_xticks(list(x))
    labels = df["timestamp_utc"].dt.strftime("%m-%d\n%H:%MZ").tolist()
    # Thin labels if many runs so the axis stays readable.
    stride = max(1, len(labels) // 10)
    displayed = [lab if i % stride == 0 else "" for i, lab in enumerate(labels)]
    ax.set_xticklabels(displayed)

    ax.set_title(
        "Token usage per run",
        fontsize=14,
        color=PALETTE["text"],
        loc="left",
    )
    ax.set_ylabel("Tokens")
    ax.legend(
        loc="upper left",
        frameon=False,
        fontsize=11,
        labelcolor=PALETTE["text"],
    )
    _save_svg(fig, path)
    return path


# Chart 3: weekly rollup -----------------------------------------------

@dataclass
class ParsedHypothesis:
    category: str
    confidence: str


def _normalize_category(raw: str) -> str:
    key = raw.strip().lower()
    if key in _CATEGORY_ALIASES:
        return _CATEGORY_ALIASES[key]
    for canonical in CATEGORIES:
        if key == canonical.lower():
            return canonical
    return raw.strip()


def _normalize_confidence(raw: str) -> str:
    key = raw.strip().capitalize()
    return key if key in CONFIDENCE_LEVELS else raw.strip()


def _parse_memo(memo_path: Path) -> list[ParsedHypothesis]:
    text = memo_path.read_text()
    cats = _CATEGORY_RE.findall(text)
    confs = _CONFIDENCE_RE.findall(text)
    # Pair positionally — memos alternate Cat/Conf per hypothesis.
    return [
        ParsedHypothesis(
            category=_normalize_category(c),
            confidence=_normalize_confidence(cf),
        )
        for c, cf in zip(cats, confs)
    ]


def _parsed_sidecar_path(memo_path: Path) -> Path:
    return memo_path.with_name(memo_path.stem + "._parsed.json")


def _load_or_parse(memo_path: Path) -> list[ParsedHypothesis]:
    sidecar = _parsed_sidecar_path(memo_path)
    memo_mtime = memo_path.stat().st_mtime
    if sidecar.exists() and sidecar.stat().st_mtime >= memo_mtime:
        try:
            data = json.loads(sidecar.read_text())
            return [
                ParsedHypothesis(**entry) for entry in data.get("hypotheses", [])
            ]
        except (json.JSONDecodeError, TypeError):
            pass  # fall through to re-parse

    parsed = _parse_memo(memo_path)
    sidecar.write_text(
        json.dumps(
            {
                "memo_file": memo_path.name,
                "hypotheses": [
                    {"category": p.category, "confidence": p.confidence}
                    for p in parsed
                ],
            },
            indent=2,
        )
    )
    return parsed


def _find_recent_memos(memos_dir: Path, since: datetime) -> list[Path]:
    """Return .md memos (not the sidecar/metrics/README) newer than `since`."""
    results: list[Path] = []
    for path in memos_dir.rglob("*.md"):
        if path.name in {"README.md"}:
            continue
        # Filename pattern: YYYY-MM-DD-HHMM.md
        stem = path.stem
        try:
            memo_ts = datetime.strptime(stem, "%Y-%m-%d-%H%M").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            continue
        if memo_ts >= since:
            results.append(path)
    results.sort()
    return results


def generate_weekly_rollup_chart(memos_dir: Path = EVALUATIONS_DIR) -> Path:
    """Two-panel chart: category counts + confidence distribution for last 7d."""
    path = CHARTS_DIR / "weekly_rollup.svg"
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=WEEKLY_WINDOW_DAYS)

    memos = _find_recent_memos(memos_dir, since)
    all_hypotheses: list[ParsedHypothesis] = []
    for memo in memos:
        try:
            all_hypotheses.extend(_load_or_parse(memo))
        except Exception as exc:
            print(f"  ! weekly: failed to parse {memo.name}: {exc}")

    if not all_hypotheses:
        _empty_placeholder(
            path,
            f"Week of {(now - timedelta(days=6)).strftime('%b %d')}",
            "No hypotheses generated in the last 7 days",
        )
        return path

    # Aggregations.
    cat_counts = {c: 0 for c in CATEGORIES}
    for h in all_hypotheses:
        if h.category in cat_counts:
            cat_counts[h.category] += 1
        else:
            cat_counts[h.category] = cat_counts.get(h.category, 0) + 1

    conf_counts = {c: 0 for c in CONFIDENCE_LEVELS}
    for h in all_hypotheses:
        conf_counts[h.confidence] = conf_counts.get(h.confidence, 0) + 1

    week_label = (now - timedelta(days=6)).strftime("%b %d")
    title = (
        f"Week of {week_label} — {len(memos)} memos, "
        f"{len(all_hypotheses)} hypotheses"
    )

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(8, 4.5), gridspec_kw={"width_ratios": [1.5, 1]}
    )
    fig.suptitle(title, fontsize=14, color=PALETTE["text"], x=0.02, ha="left")

    # (a) horizontal bar: category counts
    _style_axes(ax1, grid=True)
    ax1.grid(True, axis="x", color=PALETTE["grid"], linewidth=0.6, alpha=0.6)
    ax1.grid(False, axis="y")
    labels = list(cat_counts.keys())
    values = [cat_counts[k] for k in labels]
    ax1.barh(labels, values, color=PALETTE["primary"], height=0.65)
    ax1.invert_yaxis()
    ax1.set_xlabel("Hypotheses")
    ax1.set_title(
        "By category", fontsize=12, color=PALETTE["text"], loc="left", pad=4
    )
    # Integer ticks only
    if max(values) > 0:
        ax1.set_xticks(range(0, max(values) + 1))

    # (b) vertical bar: confidence distribution
    _style_axes(ax2, grid=True)
    conf_colors = [
        PALETTE["confidence_low"],
        PALETTE["confidence_medium"],
        PALETTE["confidence_high"],
    ]
    conf_values = [conf_counts.get(c, 0) for c in CONFIDENCE_LEVELS]
    ax2.bar(CONFIDENCE_LEVELS, conf_values, color=conf_colors, width=0.6)
    ax2.set_ylabel("Hypotheses")
    ax2.set_title(
        "By confidence",
        fontsize=12,
        color=PALETTE["text"],
        loc="left",
        pad=4,
    )
    if max(conf_values) > 0:
        ax2.set_yticks(range(0, max(conf_values) + 1))

    plt.tight_layout(rect=(0, 0, 1, 0.93))
    _save_svg(fig, path)
    return path


# CLI for quick testing ------------------------------------------------

def _main() -> None:
    metrics_path = EVALUATIONS_DIR / "_metrics.csv"
    if metrics_path.exists():
        df = pd.read_csv(metrics_path)
        print(f"cost_trend    -> {generate_cost_trend_chart(df)}")
        print(f"token_usage   -> {generate_token_usage_chart(df)}")
    else:
        print("(no metrics.csv; skipping cost/token charts)")
    print(f"weekly_rollup -> {generate_weekly_rollup_chart(EVALUATIONS_DIR)}")


if __name__ == "__main__":
    _main()
