"""
Stage 3b — generate the daily hypothesis memo.

Pipeline:
  1. Load prompts/, config/universe.yaml, and .env (ANTHROPIC_API_KEY).
  2. Run market_scan and news_scan, each wrapped so a single-scan
     failure degrades to partial inputs rather than crashing the run.
  3. Build a compact user payload (indices, sectors, top movers, news).
     Raw S&P 500 list is intentionally omitted to save tokens.
  4. Call claude-sonnet-4-5 with three cached system blocks (the
     three prompt files) + one non-cached user message.
  5. Write evaluations/YYYY/MM/YYYY-MM-DD-HHMM.md and .meta.json
     (UTC-dated filenames).

Run with:  python -m src.generate_hypotheses
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from src.market_scan import Quote, load_universe, scan as market_scan_run
from src.news_scan import (
    NewsItem,
    WINDOW_HOURS,
    load_cap,
    load_feeds,
    scan as news_scan_run,
)


ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
EVALUATIONS_DIR = ROOT / "evaluations"

MODEL = "claude-sonnet-4-5"
MAX_TOKENS = 4000
TEMPERATURE = 0.3

# claude-sonnet-4-5 pricing, USD per 1M tokens.
PRICE_INPUT = 3.00
PRICE_CACHE_WRITE = 3.75
PRICE_CACHE_READ = 0.30
PRICE_OUTPUT = 15.00


# ---------- loading ----------

def load_prompts() -> dict[str, str]:
    return {
        "system_prompt": (PROMPTS_DIR / "system_prompt.md").read_text(),
        "hypothesis_format": (PROMPTS_DIR / "hypothesis_format.md").read_text(),
        "examples": (PROMPTS_DIR / "examples.md").read_text(),
    }


def run_market_scan() -> tuple[list[Quote], list[Quote], list[Quote], int] | None:
    """(indices, sectors, sp500_ranked_desc, top_n) or None on failure."""
    try:
        universe = load_universe()
        indices = market_scan_run(universe.get("indices", []))
        sectors = market_scan_run(universe.get("sector_etfs", []))
        sp500 = market_scan_run(universe.get("sp500", []))
        top_n = int(universe.get("top_movers_count", 20))
        ranked = [q for q in sp500 if q.change_1d_pct is not None]
        ranked.sort(key=lambda q: q.change_1d_pct, reverse=True)
        return indices, sectors, ranked, top_n
    except Exception as exc:
        print(f"  ! market_scan failed: {exc}")
        return None


def run_news_scan() -> list[NewsItem]:
    try:
        feeds = load_feeds()
        cap = load_cap()
        return news_scan_run(feeds, hours=WINDOW_HOURS, cap=cap)
    except Exception as exc:
        print(f"  ! news_scan failed: {exc}")
        return []


# ---------- payload formatting ----------

def _pct(x: float | None) -> str:
    return f"{x:+.2f}%" if x is not None else "n/a"


def _ratio(x: float | None) -> str:
    return f"{x:.2f}x" if x is not None else "n/a"


def format_quote_table(title: str, quotes: list[Quote]) -> str:
    if not quotes:
        return f"\n### {title}\n\n_(no data)_\n"
    lines = [
        f"\n### {title}\n",
        "| Ticker | Price | 1d % | 5d % | Vol/30d |",
        "|---|---:|---:|---:|---:|",
    ]
    for q in quotes:
        lines.append(
            f"| {q.ticker} | {q.price:.2f} | {_pct(q.change_1d_pct)} | "
            f"{_pct(q.change_5d_pct)} | {_ratio(q.volume_ratio)} |"
        )
    return "\n".join(lines) + "\n"


def format_news_digest(items: list[NewsItem]) -> str:
    if not items:
        return "\n## News Digest\n\n_(no news available)_\n"
    by_source: dict[str, list[NewsItem]] = {}
    for item in items:
        by_source.setdefault(item.source, []).append(item)

    lines = ["\n## News Digest"]
    for source in sorted(by_source):
        lines.append(f"\n### {source} ({len(by_source[source])})\n")
        for item in by_source[source]:
            ts = (
                item.published_at.strftime("%Y-%m-%d %H:%MZ")
                if item.published_at
                else "n/a"
            )
            lines.append(f"- **[{ts}] {item.title}**")
            if item.summary:
                summary = (
                    item.summary
                    if len(item.summary) <= 300
                    else item.summary[:297] + "..."
                )
                lines.append(f"  - {summary}")
    return "\n".join(lines) + "\n"


def build_user_payload(
    market: tuple | None,
    news: list[NewsItem],
    run_ts: datetime,
) -> tuple[str, dict]:
    """Return (payload_text, {tickers_included, headlines_included})."""
    parts = [
        f"# Daily Scan Inputs\n",
        f"**Timestamp (UTC):** {run_ts.isoformat(timespec='seconds')}\n",
    ]
    included_tickers: list[str] = []
    included_headlines: list[dict] = []

    if market is not None:
        indices, sectors, ranked, top_n = market
        gainers = ranked[:top_n]
        # losers = bottom N, but presented highest-loss-first
        losers = list(reversed(ranked[-top_n:])) if len(ranked) > top_n else []

        parts.append("## Market Snapshot")
        parts.append(format_quote_table("Indices", indices))
        parts.append(format_quote_table("Sector ETFs", sectors))
        parts.append(
            format_quote_table(
                f"Top {len(gainers)} gainers (S&P 500 subset)", gainers
            )
        )
        parts.append(
            format_quote_table(
                f"Top {len(losers)} losers (S&P 500 subset)", losers
            )
        )
        for q in indices + sectors + gainers + losers:
            included_tickers.append(q.ticker)
    else:
        parts.append("\n## Market Snapshot\n\n_(market scan failed; no data)_\n")

    parts.append(format_news_digest(news))
    for item in news:
        included_headlines.append(
            {
                "source": item.source,
                "title": item.title,
                "published_at": (
                    item.published_at.isoformat()
                    if item.published_at
                    else None
                ),
            }
        )

    parts.append(
        "\n---\n\n"
        "Generate 3–5 hypotheses worth presenting to the CFO. Be skeptical, "
        "specific, and actionable. Follow the format in `hypothesis_format.md` "
        "and the quality bar in `system_prompt.md`; use the strong/weak "
        "contrast in `examples.md` as your reference.\n"
    )

    # Preserve order while deduping.
    seen: set[str] = set()
    unique_tickers: list[str] = []
    for t in included_tickers:
        if t not in seen:
            seen.add(t)
            unique_tickers.append(t)

    meta = {
        "tickers_included": unique_tickers,
        "headlines_included": included_headlines,
    }
    return "\n".join(parts), meta


# ---------- API ----------

def call_claude(prompts: dict[str, str], user_payload: str):
    load_dotenv(ROOT / ".env")
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set — add it to .env or the environment."
        )

    client = anthropic.Anthropic(api_key=api_key)

    # Three separate blocks so each prompt file stays logically distinct.
    # Single cache_control at the end of system => the entire system
    # prefix is cached together; the per-run user payload stays uncached.
    system_blocks = [
        {"type": "text", "text": prompts["system_prompt"]},
        {"type": "text", "text": prompts["hypothesis_format"]},
        {
            "type": "text",
            "text": prompts["examples"],
            "cache_control": {"type": "ephemeral"},
        },
    ]

    return client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        system=system_blocks,
        messages=[{"role": "user", "content": user_payload}],
    )


def estimate_cost(usage) -> float:
    input_tok = getattr(usage, "input_tokens", 0) or 0
    output_tok = getattr(usage, "output_tokens", 0) or 0
    cache_write = getattr(usage, "cache_creation_input_tokens", 0) or 0
    cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
    return (
        input_tok * PRICE_INPUT
        + cache_write * PRICE_CACHE_WRITE
        + cache_read * PRICE_CACHE_READ
        + output_tok * PRICE_OUTPUT
    ) / 1_000_000


# ---------- output ----------

def write_outputs(
    memo_text: str,
    response,
    run_ts: datetime,
    inputs_meta: dict,
) -> tuple[Path, Path]:
    year = run_ts.strftime("%Y")
    month = run_ts.strftime("%m")
    slug = run_ts.strftime("%Y-%m-%d-%H%M")
    out_dir = EVALUATIONS_DIR / year / month
    out_dir.mkdir(parents=True, exist_ok=True)

    memo_path = out_dir / f"{slug}.md"
    meta_path = out_dir / f"{slug}.meta.json"

    memo_path.write_text(memo_text)

    usage = response.usage
    meta = {
        "timestamp_utc": run_ts.isoformat(timespec="seconds"),
        "model": getattr(response, "model", MODEL),
        "stop_reason": getattr(response, "stop_reason", None),
        "input_tokens": getattr(usage, "input_tokens", 0),
        "output_tokens": getattr(usage, "output_tokens", 0),
        "cache_creation_input_tokens": (
            getattr(usage, "cache_creation_input_tokens", 0) or 0
        ),
        "cache_read_input_tokens": (
            getattr(usage, "cache_read_input_tokens", 0) or 0
        ),
        "cost_usd": round(estimate_cost(usage), 6),
        "tickers_included": inputs_meta["tickers_included"],
        "headlines_included": inputs_meta["headlines_included"],
    }
    meta_path.write_text(json.dumps(meta, indent=2))
    return memo_path, meta_path


# ---------- main ----------

def main() -> None:
    run_ts = datetime.now(timezone.utc)
    print(f"# generate_hypotheses — {run_ts.isoformat(timespec='seconds')}")

    print("\n[1/4] Loading prompt files...")
    prompts = load_prompts()

    print("[2/4] Running scans...")
    print("  - market_scan...")
    market = run_market_scan()
    print("  - news_scan...")
    news = run_news_scan()

    if market is None and not news:
        raise RuntimeError(
            "Both market_scan and news_scan returned no data; aborting."
        )

    print("[3/4] Assembling payload and calling Claude...")
    user_payload, inputs_meta = build_user_payload(market, news, run_ts)
    response = call_claude(prompts, user_payload)

    memo_text = response.content[0].text if response.content else ""

    print("[4/4] Writing outputs...")
    memo_path, meta_path = write_outputs(memo_text, response, run_ts, inputs_meta)

    usage = response.usage
    cost = estimate_cost(usage)
    print(f"\n  memo -> {memo_path.relative_to(ROOT)}")
    print(f"  meta -> {meta_path.relative_to(ROOT)}")
    print(
        f"\nTokens: input={usage.input_tokens}  output={usage.output_tokens}  "
        f"cache_read={getattr(usage, 'cache_read_input_tokens', 0) or 0}  "
        f"cache_write={getattr(usage, 'cache_creation_input_tokens', 0) or 0}"
    )
    print(f"Cost estimate: ${cost:.4f}")


if __name__ == "__main__":
    main()
