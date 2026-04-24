"""
Stage 1 market scan.

Pulls current price, 1d % change, 5d % change, and volume vs 30-day
average for every ticker in config/universe.yaml, then prints a
structured snapshot suitable for feeding into the hypothesis prompt.

Run with:  python -m src.market_scan
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import yaml
import yfinance as yf


CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "universe.yaml"

# 30-day avg needs ~30 trading days; 45 calendar days gives a safe margin
# across weekends and holidays. The 5-day return only reads the tail.
HISTORY_PERIOD = "45d"


@dataclass
class Quote:
    ticker: str
    price: float
    change_1d_pct: float | None
    change_5d_pct: float | None
    volume: int | None
    avg_volume_30d: float | None

    @property
    def volume_ratio(self) -> float | None:
        if self.volume is None or not self.avg_volume_30d:
            return None
        return self.volume / self.avg_volume_30d


def load_universe(path: Path = CONFIG_PATH) -> dict:
    with path.open() as f:
        return yaml.safe_load(f)


def _pct_change(curr: float, prev: float) -> float | None:
    if prev == 0 or prev is None:
        return None
    return (curr - prev) / prev * 100.0


def fetch_quote(ticker: str) -> Quote | None:
    """Pull history once per ticker and derive every field from it."""
    try:
        hist = yf.Ticker(ticker).history(period=HISTORY_PERIOD, auto_adjust=False)
    except Exception as exc:
        print(f"  ! {ticker}: fetch failed ({exc})")
        return None

    if hist.empty:
        print(f"  ! {ticker}: no data returned")
        return None

    closes = hist["Close"].dropna()
    volumes = hist["Volume"].dropna()
    if len(closes) < 2:
        return None

    price = float(closes.iloc[-1])
    change_1d = _pct_change(price, float(closes.iloc[-2]))
    change_5d = (
        _pct_change(price, float(closes.iloc[-6])) if len(closes) >= 6 else None
    )

    volume = int(volumes.iloc[-1]) if not volumes.empty else None
    avg_volume_30d = (
        float(volumes.tail(30).mean()) if len(volumes) >= 5 else None
    )

    return Quote(
        ticker=ticker,
        price=price,
        change_1d_pct=change_1d,
        change_5d_pct=change_5d,
        volume=volume,
        avg_volume_30d=avg_volume_30d,
    )


def scan(tickers: Iterable[str]) -> list[Quote]:
    results: list[Quote] = []
    for t in tickers:
        q = fetch_quote(t)
        if q is not None:
            results.append(q)
    return results


def _fmt_pct(x: float | None) -> str:
    return f"{x:+6.2f}%" if x is not None else "   n/a "


def _fmt_ratio(x: float | None) -> str:
    return f"{x:4.2f}x" if x is not None else " n/a "


def _print_table(title: str, quotes: list[Quote]) -> None:
    print(f"\n## {title}")
    print(f"{'Ticker':<8} {'Price':>10} {'1d %':>8} {'5d %':>8} {'Vol/30d':>8}")
    print("-" * 46)
    for q in quotes:
        print(
            f"{q.ticker:<8} {q.price:>10.2f} "
            f"{_fmt_pct(q.change_1d_pct)} {_fmt_pct(q.change_5d_pct)} "
            f"{_fmt_ratio(q.volume_ratio):>8}"
        )


def main() -> None:
    universe = load_universe()
    indices = universe.get("indices", [])
    sector_etfs = universe.get("sector_etfs", [])
    sp500 = universe.get("sp500", [])
    top_n = int(universe.get("top_movers_count", 20))

    print(f"# Market scan — {datetime.now().isoformat(timespec='seconds')}")
    print(
        f"Universe: {len(indices)} indices, {len(sector_etfs)} sector ETFs, "
        f"{len(sp500)} S&P 500 names"
    )

    print("\nFetching indices...")
    index_quotes = scan(indices)
    print("Fetching sector ETFs...")
    sector_quotes = scan(sector_etfs)
    print("Fetching S&P 500 subset...")
    sp500_quotes = scan(sp500)

    _print_table("Indices", index_quotes)
    _print_table("Sector ETFs", sector_quotes)

    ranked = [q for q in sp500_quotes if q.change_1d_pct is not None]
    ranked.sort(key=lambda q: q.change_1d_pct, reverse=True)
    _print_table(f"Top {top_n} gainers (S&P 500 subset)", ranked[:top_n])
    _print_table(
        f"Top {top_n} losers (S&P 500 subset)",
        list(reversed(ranked[-top_n:])),
    )

    fetched = len(index_quotes) + len(sector_quotes) + len(sp500_quotes)
    requested = len(indices) + len(sector_etfs) + len(sp500)
    print(f"\nFetched {fetched}/{requested} tickers.")


if __name__ == "__main__":
    main()
