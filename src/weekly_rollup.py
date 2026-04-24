"""
Stage 4b weekly rollup entry point.

Runs the heavy weekly chart and refreshes the dashboard so the README's
embedded weekly chart reflects the new SVG. The per-run pipeline
intentionally skips the weekly chart because it scans every memo from
the last seven days.
"""

from __future__ import annotations

from src import charts, dashboard
from src.charts import EVALUATIONS_DIR


def main() -> None:
    print("Regenerating weekly rollup chart...")
    print(f"  -> {charts.generate_weekly_rollup_chart(EVALUATIONS_DIR)}")
    print("Refreshing dashboard README...")
    print(f"  -> {dashboard.regenerate_dashboard()}")


if __name__ == "__main__":
    main()
