"""
Stage 4b dashboard generator.

regenerate_dashboard() writes evaluations/README.md from:
  - the most recent memo's executive summary (extracted from markdown)
  - the rolling _metrics.csv
  - the three chart SVGs in evaluations/charts/

Intentionally does not regenerate the charts themselves; that's
charts.py's job. The dashboard is pure formatting.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
EVALUATIONS_DIR = ROOT / "evaluations"
METRICS_PATH = EVALUATIONS_DIR / "_metrics.csv"
DASHBOARD_PATH = EVALUATIONS_DIR / "README.md"

RECENT_RUNS_TABLE_ROWS = 10

# Grabs the prose between "## Executive Summary" and the next `---` or `##`.
_EXEC_SUMMARY_RE = re.compile(
    r"^## Executive Summary\s*\n+(.+?)(?=\n\s*\n---|\n\s*\n## )",
    re.MULTILINE | re.DOTALL,
)

# Extract session from the sidecar meta if we want it; cheaper to pull
# from the metrics row directly.


def _find_latest_memo(memos_root: Path = EVALUATIONS_DIR) -> Path | None:
    """Latest .md whose filename matches YYYY-MM-DD-HHMM.md."""
    candidates: list[tuple[datetime, Path]] = []
    for path in memos_root.rglob("*.md"):
        if path.name == "README.md":
            continue
        try:
            ts = datetime.strptime(path.stem, "%Y-%m-%d-%H%M")
        except ValueError:
            continue
        candidates.append((ts, path))
    if not candidates:
        return None
    candidates.sort()
    return candidates[-1][1]


def _memo_relative_link(memo_path: Path) -> str:
    """Path relative to evaluations/ for use in markdown links."""
    return str(memo_path.relative_to(EVALUATIONS_DIR)).replace("\\", "/")


def _extract_exec_summary(memo_text: str) -> str:
    match = _EXEC_SUMMARY_RE.search(memo_text)
    if not match:
        return "_(executive summary could not be extracted)_"
    return match.group(1).strip()


def _format_session(session: str) -> str:
    return "Pre-market" if session == "premarket" else "Close"


def _format_memo_header(memo_path: Path, session: str | None) -> str:
    """E.g. 'April 24, 2026 — Close'."""
    ts = datetime.strptime(memo_path.stem, "%Y-%m-%d-%H%M")
    session_label = _format_session(session) if session else "Session unknown"
    return f"{ts.strftime('%B %-d, %Y')} — {session_label}"


def _load_metrics() -> pd.DataFrame | None:
    if not METRICS_PATH.exists():
        return None
    df = pd.read_csv(METRICS_PATH)
    if df.empty:
        return None
    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], utc=True)
    return df.sort_values("timestamp_utc").reset_index(drop=True)


def _latest_metrics_row(df: pd.DataFrame) -> pd.Series | None:
    return df.iloc[-1] if not df.empty else None


def _format_recent_runs_table(df: pd.DataFrame) -> str:
    """Render the last N runs as a markdown table."""
    recent = df.sort_values("timestamp_utc", ascending=False).head(
        RECENT_RUNS_TABLE_ROWS
    )
    lines = [
        "| Date | Session | Hypotheses | Cost | Link |",
        "|---|---|---:|---:|---|",
    ]
    for _, row in recent.iterrows():
        ts: pd.Timestamp = row["timestamp_utc"]
        date_str = ts.strftime("%Y-%m-%d %H:%MZ")
        session_label = _format_session(str(row["session"]))
        memo_rel = (
            f"{ts.strftime('%Y/%m')}/{ts.strftime('%Y-%m-%d-%H%M')}.md"
        )
        cost = float(row["cost_usd"])
        hyps = int(row["num_hypotheses"])
        lines.append(
            f"| {date_str} | {session_label} | {hyps} | "
            f"${cost:.4f} | [memo]({memo_rel}) |"
        )
    return "\n".join(lines)


def regenerate_dashboard() -> Path:
    """Write evaluations/README.md based on the latest memo + metrics."""
    latest_memo = _find_latest_memo()
    metrics_df = _load_metrics()

    parts: list[str] = [
        "# Daily Market Hypothesis Evaluations",
        "",
        "> Autonomous system scanning the US equity market and financial news "
        "twice per trading day, generating CFO-grade analytical hypotheses.  ",
        "> See [system spec](../docs/hypothesis-generator-spec.md) for design.",
        "",
    ]

    # --- Latest memo section ---
    if latest_memo is not None:
        session_label: str | None = None
        if metrics_df is not None:
            latest_row = _latest_metrics_row(metrics_df)
            if latest_row is not None:
                session_label = str(latest_row["session"])
        header_label = _format_memo_header(latest_memo, session_label)
        memo_text = latest_memo.read_text()
        summary = _extract_exec_summary(memo_text)
        link = _memo_relative_link(latest_memo)
        parts += [
            f"## Latest memo — {header_label}",
            "",
            summary,
            "",
            f"[Read full memo →]({link})",
            "",
        ]
    else:
        parts += [
            "## Latest memo",
            "",
            "_No memos have been generated yet._",
            "",
        ]

    # --- Operational metrics ---
    parts += [
        "## Operational metrics",
        "",
        "![Run cost](charts/cost_trend.svg)",
        "",
        "![Token usage](charts/token_usage.svg)",
        "",
        "## This week",
        "",
        "![Weekly rollup](charts/weekly_rollup.svg)",
        "",
    ]

    # --- Recent runs ---
    parts += ["## Recent runs", ""]
    if metrics_df is not None and not metrics_df.empty:
        parts.append(_format_recent_runs_table(metrics_df))
    else:
        parts.append("_No run metrics recorded yet._")
    parts.append("")

    # --- How this runs ---
    parts += [
        "## How this runs",
        "",
        "See the main [README](../README.md#daily-market-hypothesis-generator) "
        "for the schedule, manual trigger command, and a short description of "
        "each stage.",
        "",
    ]

    DASHBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    DASHBOARD_PATH.write_text("\n".join(parts))
    return DASHBOARD_PATH


if __name__ == "__main__":
    print(f"dashboard -> {regenerate_dashboard()}")
