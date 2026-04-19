"""Capacity planning dashboard for the Good Winter 001 demo vessel."""

from __future__ import annotations

import html

from good_winter_baplie_tools import fmt_int, fmt_tons, load_baplie, summary_totals, write_html_report


def main() -> None:
    df = load_baplie()
    totals = summary_totals(df)
    by_type = df.groupby("Type").agg(Units=("Container", "count"), TEUs=("TEUs", "sum"), Tons=("Tons", "sum")).reset_index()
    by_pod = df.groupby("POD").agg(Units=("Container", "count"), TEUs=("TEUs", "sum"), Tons=("Tons", "sum")).reset_index()

    cards = "".join(
        f"<div class='card'><b>{value}</b><span>{label}</span></div>"
        for label, value in [
            ("Units", fmt_int(totals["Units"])),
            ("TEUs", fmt_int(totals["TEUs"])),
            ("Tons", fmt_tons(totals["Tons"])),
            ("Reefer", fmt_int(totals["Reefer"])),
            ("NOR", fmt_int(totals["NOR"])),
            ("OOG", fmt_int(totals["OOG"])),
        ]
    )
    type_rows = "".join(
        f"<tr><td>{html.escape(str(r.Type))}</td><td>{fmt_int(r.Units)}</td><td>{fmt_int(r.TEUs)}</td><td>{fmt_tons(r.Tons)}</td></tr>"
        for r in by_type.sort_values("Units", ascending=False).itertuples()
    )
    pod_rows = "".join(
        f"<tr><td>{html.escape(str(r.POD))}</td><td>{fmt_int(r.Units)}</td><td>{fmt_int(r.TEUs)}</td><td>{fmt_tons(r.Tons)}</td></tr>"
        for r in by_pod.sort_values("Units", ascending=False).itertuples()
    )
    body = f"""
    <div class="cards">{cards}</div>
    <section><h2>Capacity by Equipment Type</h2><table><thead><tr><th>Type</th><th>Units</th><th>TEUs</th><th>Tons</th></tr></thead><tbody>{type_rows}</tbody></table></section>
    <section><h2>Capacity by POD</h2><table><thead><tr><th>POD</th><th>Units</th><th>TEUs</th><th>Tons</th></tr></thead><tbody>{pod_rows}</tbody></table></section>
    """
    output = write_html_report("good_winter_capacity_planning.html", "Good Winter 001 · Capacity Planning", body)
    print(f"Created {output}")


if __name__ == "__main__":
    main()

