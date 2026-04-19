"""Shared BAPLIE demo tools for the Good Winter 001 portfolio project."""

from __future__ import annotations

import html
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "Baplie_Github.xlsx"
REPORTS_DIR = PROJECT_ROOT / "reports"
VESSEL_NAME = "Good Winter 001"


DEMO_CLIENTS = [
    "Client Aurora",
    "Client Summit",
    "Client Harmony",
    "Client Compass",
    "Client Horizon",
    "Client Meridian",
]


def ensure_reports_dir() -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    return REPORTS_DIR


def has_value(value) -> bool:
    if pd.isna(value):
        return False
    text = str(value).strip().upper()
    return text not in {"", "NAN", "NONE", "NULL", "0", "0.0", "-"}


def find_header_row(path: Path = DATA_FILE) -> int:
    raw = pd.read_excel(path, header=None)
    for idx in range(min(40, len(raw))):
        values = [str(x).strip().upper() for x in raw.iloc[idx].fillna("").values]
        if "CONTAINER ID" in values and "TYPE" in values:
            return idx
    raise ValueError("Could not find the BAPLIE header row.")


def normalize_type(raw_type, size=None, height=None, setting=None) -> str:
    text = str(raw_type or "").strip().upper()
    size_text = str(size or "").strip().upper()
    height_text = str(height or "").strip().upper()
    setting_text = str(setting or "").strip().upper()

    if "FR" in text or "FLAT" in text:
        return "FR40" if "40" in text or size_text == "40" else "FR20"
    if "OT" in text or "OPEN" in text or "OH" in text:
        return "OT40" if "40" in text or size_text == "40" else "OT20"
    if "RH" in text or "RF" in text or "RE" in text or "R1" in text:
        return "RH40" if "40" in text or size_text == "40" else "RF20"
    if "HC" in text or text in {"45G1", "4510", "4EG1"} or height_text == "9'6":
        return "HC40" if "40" in text or size_text == "40" else "DC20"
    if "20" in text or size_text == "20":
        return "DC20"
    if "40" in text or size_text == "40":
        return "HC40" if height_text == "9'6" else "DC40"
    if "DRY REEFER" in setting_text:
        return "RH40"
    return text or "UNKNOWN"


def teu_from_type(cntr_type: str, size=None) -> int:
    text = str(cntr_type or "").upper()
    size_text = str(size or "").strip()
    if "20" in text or size_text == "20":
        return 1
    if "40" in text or size_text == "40":
        return 2
    return 0


def is_reefer_equipment(raw_type, norm_type: str) -> bool:
    text = str(raw_type or "").upper()
    return norm_type in {"RH40", "RF20"} or any(token in text for token in ("RH", "RF", "RE", "R1"))


def is_active_reefer(raw_type, norm_type: str, setting) -> bool:
    setting_text = str(setting or "").strip().upper()
    return is_reefer_equipment(raw_type, norm_type) and has_value(setting_text) and "DRY REEFER" not in setting_text


def is_nor(raw_type, norm_type: str, setting) -> bool:
    return is_reefer_equipment(raw_type, norm_type) and not is_active_reefer(raw_type, norm_type, setting)


def is_oog(raw_type, norm_type: str) -> bool:
    text = f"{raw_type or ''} {norm_type or ''}".upper()
    return any(token in text for token in ("FR", "OT", "OH", "FLAT", "OPEN"))


def load_baplie(path: Path = DATA_FILE) -> pd.DataFrame:
    header = find_header_row(path)
    df = pd.read_excel(path, header=header).dropna(how="all").copy()
    df = df[df.get("Container Id", "").apply(has_value)].copy()

    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()

    rows = []
    for idx, row in df.reset_index(drop=True).iterrows():
        norm_type = normalize_type(row.get("Type", ""), row.get("Size", ""), row.get("Height", ""), row.get("Setting", ""))
        weight_kg = pd.to_numeric(row.get("Weight", 0), errors="coerce")
        weight_kg = 0 if pd.isna(weight_kg) else float(weight_kg)
        client = DEMO_CLIENTS[idx % len(DEMO_CLIENTS)]
        rows.append(
            {
                "Vessel": VESSEL_NAME,
                "Container": f"DEMO{idx + 1:06d}",
                "POL": str(row.get("POL", "")).upper(),
                "POD": str(row.get("POD", "")).upper(),
                "Carrier": str(row.get("Carrier", "")).upper(),
                "Size": str(row.get("Size", "")),
                "Raw Type": str(row.get("Type", "")).upper(),
                "Type": norm_type,
                "Weight kg": weight_kg,
                "Tons": weight_kg / 1000,
                "Temp": str(row.get("Setting", "")).strip(),
                "IMO Class": str(row.get("Class", "")).strip(),
                "TEUs": teu_from_type(norm_type, row.get("Size", "")),
                "Reefer": 1 if is_active_reefer(row.get("Type", ""), norm_type, row.get("Setting", "")) else 0,
                "NOR": 1 if is_nor(row.get("Type", ""), norm_type, row.get("Setting", "")) else 0,
                "IMO": 1 if has_value(row.get("Class", "")) else 0,
                "OOG": 1 if is_oog(row.get("Type", ""), norm_type) else 0,
                "Client": client,
            }
        )
    return pd.DataFrame(rows)


def summary_totals(df: pd.DataFrame) -> dict[str, float]:
    if df.empty:
        return {"Units": 0, "TEUs": 0, "Tons": 0, "Reefer": 0, "NOR": 0, "IMO": 0, "OOG": 0}
    return {
        "Units": int(len(df)),
        "TEUs": int(df["TEUs"].sum()),
        "Tons": float(df["Tons"].sum()),
        "Reefer": int(df["Reefer"].sum()),
        "NOR": int(df["NOR"].sum()),
        "IMO": int(df["IMO"].sum()),
        "OOG": int(df["OOG"].sum()),
    }


def fmt_int(value) -> str:
    return f"{int(round(float(value))):,}".replace(",", ".")


def fmt_tons(value) -> str:
    return f"{float(value):,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


def html_page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{ --navy:#071a33; --navy2:#0d2a52; --sky:#7cc7ff; --sky2:#d8efff; --paper:#f5f8fc; --line:#d7e3ef; --ink:#111827; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Arial, Helvetica, sans-serif; background:var(--paper); color:var(--ink); }}
    header {{ background:linear-gradient(135deg,var(--navy),var(--navy2)); color:white; padding:34px min(5vw,56px); }}
    header span {{ color:var(--sky2); font-size:12px; font-weight:900; text-transform:uppercase; }}
    h1 {{ margin:8px 0 0; font-size:clamp(30px,5vw,54px); line-height:1; }}
    main {{ width:min(1180px, calc(100% - 32px)); margin:28px auto 44px; }}
    .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin-bottom:20px; }}
    .card {{ background:white; border:1px solid var(--line); border-radius:8px; padding:16px; }}
    .card b {{ display:block; color:var(--navy2); font-size:28px; line-height:1; }}
    .card span {{ display:block; margin-top:8px; color:#627084; font-size:12px; font-weight:900; text-transform:uppercase; }}
    section {{ background:white; border:1px solid var(--line); border-radius:8px; padding:18px; margin-top:16px; }}
    h2 {{ margin:0 0 12px; color:var(--navy2); }}
    table {{ width:100%; border-collapse:collapse; font-size:13px; }}
    th, td {{ padding:10px; border-bottom:1px solid var(--line); text-align:left; }}
    th {{ background:var(--navy2); color:white; font-size:11px; text-transform:uppercase; }}
    .note {{ margin-top:16px; color:#627084; font-size:12px; }}
  </style>
</head>
<body>
  <header>
    <span>S&OP · Capacity Planning · Business Intelligence</span>
    <h1>{html.escape(title)}</h1>
  </header>
  <main>
    {body}
    <p class="note">** Dados ficticios para demonstracao. Names, clients, ports, voyages, and business references were adapted for public portfolio use.</p>
  </main>
</body>
</html>"""


def write_html_report(filename: str, title: str, body: str) -> Path:
    output = ensure_reports_dir() / filename
    output.write_text(html_page(title, body), encoding="utf-8")
    return output

