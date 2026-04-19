"""Commercial intelligence view using fictitious clients and demo BAPLIE volumes."""

from __future__ import annotations

import html

from good_winter_baplie_tools import fmt_int, fmt_tons, load_baplie, write_html_report


def main() -> None:
    df = load_baplie()
    client = df.groupby("Client").agg(Units=("Container", "count"), TEUs=("TEUs", "sum"), Tons=("Tons", "sum"), Reefer=("Reefer", "sum")).reset_index()
    client["RevenueIndex"] = (client["TEUs"] * 100 + client["Tons"] * 2 + client["Reefer"] * 35).round(0)

    rows = "".join(
        f"<tr><td>{html.escape(r.Client)}</td><td>{fmt_int(r.Units)}</td><td>{fmt_int(r.TEUs)}</td><td>{fmt_tons(r.Tons)}</td><td>{fmt_int(r.Reefer)}</td><td>{fmt_int(r.RevenueIndex)}</td></tr>"
        for r in client.sort_values("RevenueIndex", ascending=False).itertuples()
    )
    body = f"""
    <div class="cards">
      <div class="card"><b>{fmt_int(client['Units'].sum())}</b><span>Portfolio Units</span></div>
      <div class="card"><b>{fmt_int(client['TEUs'].sum())}</b><span>Portfolio TEUs</span></div>
      <div class="card"><b>{fmt_int(client['RevenueIndex'].sum())}</b><span>Revenue Index</span></div>
    </div>
    <section><h2>Commercial Portfolio by Fictitious Client</h2><table><thead><tr><th>Client</th><th>Units</th><th>TEUs</th><th>Tons</th><th>Reefer</th><th>Revenue Index</th></tr></thead><tbody>{rows}</tbody></table></section>
    """
    output = write_html_report("good_winter_commercial_intelligence.html", "Good Winter 001 · Commercial Intelligence", body)
    print(f"Created {output}")


if __name__ == "__main__":
    main()
