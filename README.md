# S&OP Capacity Planning BI

Portfolio project focused on **S&OP, capacity planning, maritime logistics, business intelligence, and process automation**.

This repository demonstrates how operational shipping data can be transformed into executive-ready intelligence: from BAPLIE-style Excel files to capacity KPIs, gate-in visibility, commercial views, and decision dashboards.

## Why This Project Matters

Logistics teams often work with fragmented spreadsheets, manual checks, and urgent operational questions:

- How much capacity is planned versus loaded?
- Which ports and cargo types are driving volume?
- Where are reefer, NOR, OOG, and weight risks concentrated?
- How can commercial, planning, and execution teams read the same numbers?

This project turns that workflow into a structured analytical pipeline using Python, Excel automation, and HTML dashboards.

## Professional Focus

- **S&OP and Capacity Planning**: TEU, weight, port, and special cargo visibility.
- **Business Intelligence**: executive KPIs, dashboard-ready outputs, and summarized views.
- **Commercial Intelligence**: customer-style segmentation, volume concentration, and booking/revenue logic.
- **Operational Execution**: gate-in, BAPLIE, load/discharge comparison, and exception tracking.
- **Automation**: repeatable Python scripts that reduce manual spreadsheet consolidation.

## Demo Vessel

All public examples use the fictitious vessel name:

**Good Winter 001**

Names, clients, voyages, and some port references are adapted for portfolio use.

## Repository Structure

```text
.
├── README.md
├── index.html
├── requirements.txt
├── .gitignore
├── data/
│   └── Baplie_Github.xlsx
├── docs/
│   └── GitHub_Capa_Logistica_Automacao.html
├── reports/
│   └── README.md
└── src/
    ├── good_winter_baplie_tools.py
    ├── good_winter_capacity_planning.py
    ├── good_winter_commercial_intelligence.py
    ├── good_winter_comparison_dashboard.py
    ├── good_winter_final_moves.py
    ├── good_winter_gate_in_report.py
    └── good_winter_moves_all_ports.py
```

## Main Scripts

| Script | Purpose |
| --- | --- |
| `good_winter_capacity_planning.py` | Builds capacity indicators by units, TEUs, tons, equipment type, reefer, NOR, IMO, and OOG. |
| `good_winter_gate_in_report.py` | Creates a gate-in/load execution report from the BAPLIE demo file. |
| `good_winter_commercial_intelligence.py` | Produces a fictitious commercial view by client, port, volume, and revenue-like index. |
| `good_winter_comparison_dashboard.py` | Compares plan-style capacity targets versus loaded BAPLIE figures. |
| `good_winter_final_moves.py` | Generates an executive final-moves summary for planning and execution teams. |
| `good_winter_moves_all_ports.py` | Exports detailed movements by port and equipment type. |

## How To Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run any report script:

```bash
python src/good_winter_capacity_planning.py
python src/good_winter_gate_in_report.py
python src/good_winter_commercial_intelligence.py
python src/good_winter_comparison_dashboard.py
python src/good_winter_final_moves.py
python src/good_winter_moves_all_ports.py
```

Outputs are written to:

```text
reports/
```

## Data Disclaimer

** Dados ficticios para demonstracao. Names, clients, ports, voyages, and business references were adapted for public portfolio use. The project is designed to demonstrate technical and analytical capability without exposing confidential operational data.

