"""
Stage 2 news scan.

Aggregates the last 12 hours of business-news headlines from the RSS
feeds in config/universe.yaml, strips HTML from summaries, dedupes by
title similarity (Jaccard >= 0.85, keeping the earliest publish time),
sorts newest-first, and caps the result.

Run with:  python -m src.news_scan
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

import feedparser
import yaml


CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "universe.yaml"

WINDOW_HOURS = 12
DEFAULT_CAP = 40
SIMILARITY_THRESHOLD = 0.85

# Some publishers block the default feedparser UA; a browser-shaped UA is
# the simplest workaround and is harmless otherwise.
USER_AGENT = (
    "Mozilla/5.0 (compatible; hypothesis-generator/0.1; "
    "+https://github.com/anthropics/claude-code)"
)

_HTML_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")
_WORD = re.compile(r"[a-z0-9]+")


@dataclass
class NewsItem:
    source: str
    title: str
    summary: str
    url: str
    published_at: datetime | None


def _load_config(path: Path) -> dict:
    with path.open() as f:
        return yaml.safe_load(f) or {}


def load_feeds(path: Path = CONFIG_PATH) -> dict[str, str]:
    return _load_config(path).get("news_feeds", {}) or {}


def load_cap(path: Path = CONFIG_PATH) -> int:
    return int(_load_config(path).get("news_cap", DEFAULT_CAP))


def _strip_html(text: str | None) -> str:
    if not text:
        return ""
    text = html.unescape(text)
    text = _HTML_TAG.sub("", text)
    return _WS.sub(" ", text).strip()


def _parse_published(entry) -> datetime | None:
    """Return a timezone-aware UTC datetime, or None if unparseable."""
    for attr in ("published_parsed", "updated_parsed"):
        t = entry.get(attr)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except (TypeError, ValueError):
                continue
    return None


def _tokens(title: str) -> set[str]:
    return set(_WORD.findall(title.lower()))


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    union = len(a | b)
    return len(a & b) / union if union else 0.0


def fetch_feed(source: str, url: str) -> list[NewsItem]:
    parsed = feedparser.parse(url, agent=USER_AGENT)
    if parsed.bozo and not parsed.entries:
        reason = getattr(parsed, "bozo_exception", "unknown")
        print(f"  ! {source}: parse issue ({reason})")
        return []

    items: list[NewsItem] = []
    for entry in parsed.entries:
        title = _strip_html(entry.get("title", ""))
        if not title:
            continue
        summary = _strip_html(
            entry.get("summary") or entry.get("description") or ""
        )
        items.append(
            NewsItem(
                source=source,
                title=title,
                summary=summary,
                url=entry.get("link", ""),
                published_at=_parse_published(entry),
            )
        )
    return items


def filter_recent(
    items: Iterable[NewsItem], hours: int = WINDOW_HOURS
) -> list[NewsItem]:
    """Keep items within the window. Missing timestamps default to include."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    return [
        i for i in items
        if i.published_at is None or i.published_at >= cutoff
    ]


def deduplicate(
    items: list[NewsItem], threshold: float = SIMILARITY_THRESHOLD
) -> list[NewsItem]:
    """Drop later duplicates; keep the earliest publish time for each cluster."""
    # Earliest-first so subsequent similar titles are dropped.
    # Items with no timestamp sort last — items that have a timestamp win.
    sentinel_late = datetime.max.replace(tzinfo=timezone.utc)
    ordered = sorted(items, key=lambda i: i.published_at or sentinel_late)

    kept: list[NewsItem] = []
    kept_tokens: list[set[str]] = []
    for item in ordered:
        toks = _tokens(item.title)
        if any(_jaccard(toks, kt) >= threshold for kt in kept_tokens):
            continue
        kept.append(item)
        kept_tokens.append(toks)
    return kept


def scan(
    feeds: dict[str, str],
    hours: int = WINDOW_HOURS,
    cap: int = DEFAULT_CAP,
) -> list[NewsItem]:
    raw: list[NewsItem] = []
    for source, url in feeds.items():
        print(f"  - {source}: fetching {url}")
        fetched = fetch_feed(source, url)
        print(f"    returned {len(fetched)} entries")
        raw.extend(fetched)

    recent = filter_recent(raw, hours=hours)
    deduped = deduplicate(recent)

    sentinel_early = datetime.min.replace(tzinfo=timezone.utc)
    deduped.sort(
        key=lambda i: i.published_at or sentinel_early, reverse=True
    )
    return deduped[:cap]


def _print_digest(items: list[NewsItem]) -> None:
    by_source: dict[str, list[NewsItem]] = {}
    for item in items:
        by_source.setdefault(item.source, []).append(item)

    for source in sorted(by_source):
        print(f"\n## {source} ({len(by_source[source])})")
        for item in by_source[source]:
            ts = (
                item.published_at.strftime("%Y-%m-%d %H:%MZ")
                if item.published_at
                else "       n/a       "
            )
            print(f"  [{ts}] {item.title}")
            if item.summary:
                summary = (
                    item.summary
                    if len(item.summary) <= 200
                    else item.summary[:197] + "..."
                )
                print(f"      {summary}")
            if item.url:
                print(f"      -> {item.url}")


def main() -> None:
    feeds = load_feeds()
    cap = load_cap()

    print(
        f"# News scan — {datetime.now(timezone.utc).isoformat(timespec='seconds')}"
    )
    print(
        f"Window: last {WINDOW_HOURS}h | Sources: {len(feeds)} | Cap: {cap}"
    )
    print()

    items = scan(feeds, hours=WINDOW_HOURS, cap=cap)
    print(f"\nKept {len(items)} items after filter + dedupe + cap.")

    if items:
        _print_digest(items)


if __name__ == "__main__":
    main()
