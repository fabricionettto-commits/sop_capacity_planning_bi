"""Plan versus actual comparison dashboard for the Good Winter 001 demo vessel."""

from __future__ import annotations

from good_winter_baplie_tools import fmt_int, fmt_tons, load_baplie, summary_totals, write_html_report


TARGETS = {
    "Units": 760,
    "TEUs": 1460,
    "Tons": 15000,
    "Reefer": 115,
    "NOR": 20,
}


def status(actual: float, target: float) -> str:
    diff = actual - target
    if abs(diff) <= max(target * 0.02, 1):
        return "On Plan"
    return "Over Plan" if diff > 0 else "Open Space"


def main() -> None:
    totals = summary_totals(load_baplie())
    rows = ""
    for key, target in TARGETS.items():
        actual = totals[key]
        formatter = fmt_tons if key == "Tons" else fmt_int
        rows += f"<tr><td>{key}</td><td>{formatter(target)}</td><td>{formatter(actual)}</td><td>{formatter(actual - target)}</td><td>{status(actual, target)}</td></tr>"

    body = f"""
    <div class="cards">
      <div class="card"><b>{fmt_int(totals['Units'])}</b><span>Actual Units</span></div>
      <div class="card"><b>{fmt_int(totals['TEUs'])}</b><span>Actual TEUs</span></div>
      <div class="card"><b>{fmt_tons(totals['Tons'])}</b><span>Actual Tons</span></div>
    </div>
    <section><h2>Planning Target vs BAPLIE Actual</h2><table><thead><tr><th>KPI</th><th>Target</th><th>Actual</th><th>Diff</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></section>
    """
    output = write_html_report("good_winter_comparison_dashboard.html", "Good Winter 001 · Planning Comparison", body)
    print(f"Created {output}")


if __name__ == "__main__":
    main()

