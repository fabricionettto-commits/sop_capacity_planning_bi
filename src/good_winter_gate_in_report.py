"""Gate-in / loaded cargo report for the Good Winter 001 demo vessel."""

from __future__ import annotations

import html

from good_winter_baplie_tools import fmt_int, fmt_tons, load_baplie, summary_totals, write_html_report


def main() -> None:
    df = load_baplie()
    totals = summary_totals(df)
    preview = df.sort_values(["POD", "Type", "Container"]).head(80)

    cards = "".join(
        f"<div class='card'><b>{value}</b><span>{label}</span></div>"
        for label, value in [
            ("Loaded Units", fmt_int(totals["Units"])),
            ("Loaded TEUs", fmt_int(totals["TEUs"])),
            ("Loaded Tons", fmt_tons(totals["Tons"])),
            ("Active Reefer", fmt_int(totals["Reefer"])),
            ("NOR", fmt_int(totals["NOR"])),
        ]
    )
    rows = "".join(
        "<tr>"
        f"<td>{html.escape(r.Container)}</td><td>{html.escape(r.POL)}</td><td>{html.escape(r.POD)}</td>"
        f"<td>{html.escape(r.Type)}</td><td>{fmt_tons(r.Tons)}</td><td>{fmt_int(r.TEUs)}</td>"
        f"<td>{'Reefer' if r.Reefer else 'NOR' if r.NOR else ''}</td>"
        "</tr>"
        for r in preview.itertuples()
    )
    body = f"""
    <div class="cards">{cards}</div>
    <section><h2>Gate-In / BAPLIE Preview</h2><table><thead><tr><th>Container</th><th>POL</th><th>POD</th><th>Type</th><th>Tons</th><th>TEUs</th><th>Special</th></tr></thead><tbody>{rows}</tbody></table></section>
    """
    output = write_html_report("good_winter_gate_in_report.html", "Good Winter 001 · Gate-In Report", body)
    print(f"Created {output}")


if __name__ == "__main__":
    main()

