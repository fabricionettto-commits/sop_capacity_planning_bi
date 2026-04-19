"""Detailed all-ports movement export for the Good Winter 001 demo vessel."""

from __future__ import annotations

import html

from good_winter_baplie_tools import ensure_reports_dir, fmt_int, fmt_tons, load_baplie, summary_totals, write_html_report


def main() -> None:
    df = load_baplie()
    totals = summary_totals(df)
    export_cols = ["Vessel", "Container", "POL", "POD", "Type", "TEUs", "Tons", "Reefer", "NOR", "IMO", "OOG", "Client"]
    excel_path = ensure_reports_dir() / "good_winter_moves_all_ports.xlsx"
    df[export_cols].to_excel(excel_path, index=False)

    detail = df.sort_values(["POD", "Type", "Container"]).head(120)
    rows = "".join(
        "<tr>"
        f"<td>{html.escape(r.Container)}</td><td>{html.escape(r.POL)}</td><td>{html.escape(r.POD)}</td>"
        f"<td>{html.escape(r.Type)}</td><td>{fmt_int(r.TEUs)}</td><td>{fmt_tons(r.Tons)}</td><td>{html.escape(r.Client)}</td>"
        "</tr>"
        for r in detail.itertuples()
    )
    body = f"""
    <div class="cards">
      <div class="card"><b>{fmt_int(totals['Units'])}</b><span>Units</span></div>
      <div class="card"><b>{fmt_int(totals['TEUs'])}</b><span>TEUs</span></div>
      <div class="card"><b>{fmt_tons(totals['Tons'])}</b><span>Tons</span></div>
    </div>
    <section><h2>All Ports Movement Detail</h2><table><thead><tr><th>Container</th><th>POL</th><th>POD</th><th>Type</th><th>TEUs</th><th>Tons</th><th>Client</th></tr></thead><tbody>{rows}</tbody></table></section>
    """
    html_path = write_html_report("good_winter_moves_all_ports.html", "Good Winter 001 · All Ports Moves", body)
    print(f"Created {html_path}")
    print(f"Created {excel_path}")


if __name__ == "__main__":
    main()

