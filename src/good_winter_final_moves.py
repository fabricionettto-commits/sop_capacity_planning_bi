"""Executive final moves summary for the Good Winter 001 demo vessel."""

from __future__ import annotations

import html

from good_winter_baplie_tools import fmt_int, fmt_tons, load_baplie, summary_totals, write_html_report


def main() -> None:
    df = load_baplie()
    totals = summary_totals(df)
    by_port = df.groupby("POD").agg(Units=("Container", "count"), TEUs=("TEUs", "sum"), Tons=("Tons", "sum"), Reefer=("Reefer", "sum"), NOR=("NOR", "sum")).reset_index()
    rows = "".join(
        f"<tr><td>{html.escape(r.POD)}</td><td>{fmt_int(r.Units)}</td><td>{fmt_int(r.TEUs)}</td><td>{fmt_tons(r.Tons)}</td><td>{fmt_int(r.Reefer)}</td><td>{fmt_int(r.NOR)}</td></tr>"
        for r in by_port.sort_values("Units", ascending=False).itertuples()
    )
    body = f"""
    <div class="cards">
      <div class="card"><b>{fmt_int(totals['Units'])}</b><span>Final Units</span></div>
      <div class="card"><b>{fmt_int(totals['TEUs'])}</b><span>Final TEUs</span></div>
      <div class="card"><b>{fmt_tons(totals['Tons'])}</b><span>Final Tons</span></div>
      <div class="card"><b>{fmt_int(totals['Reefer'] + totals['NOR'])}</b><span>Reefer Equipment</span></div>
    </div>
    <section><h2>Final Moves by POD</h2><table><thead><tr><th>POD</th><th>Units</th><th>TEUs</th><th>Tons</th><th>Reefer</th><th>NOR</th></tr></thead><tbody>{rows}</tbody></table></section>
    """
    output = write_html_report("good_winter_final_moves.html", "Good Winter 001 · Final Moves", body)
    print(f"Created {output}")


if __name__ == "__main__":
    main()

