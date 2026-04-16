from __future__ import annotations

import io
import json

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def summary_dataframe(company: dict, baseline: dict, ai: dict, sim: dict, result: dict) -> pd.DataFrame:
    data = [
        ("Company", company.get("company_name", "")),
        ("Industry", company.get("industry", "")),
        ("Country", company.get("country", "")),
        ("Scenario", sim.get("scenario_type", "")),
        ("Contribution %", sim.get("contribution_rate_percent", 0)),
        ("Gross Productivity Gain", result.get("gross_productivity_gain", 0)),
        ("Total AI Cost", result.get("total_ai_cost", 0)),
        ("Adjusted Net Gain", result.get("adjusted_net_gain", 0)),
        ("Proposed Pension Contribution", result.get("proposed_pension_contribution", 0)),
        ("Platform Success Fee", result.get("platform_success_fee", 0)),
        ("Employer Retained Value", result.get("employer_retained_value", 0)),
    ]
    return pd.DataFrame(data, columns=["Metric", "Value"])


def to_json_bytes(payload: dict) -> bytes:
    return json.dumps(payload, indent=2, default=str).encode("utf-8")


def build_pdf_report(
    branding: dict,
    company: dict,
    baseline: dict,
    ai: dict,
    sim: dict,
    result: dict,
    disclaimer: str,
) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, branding.get("product_name", "Pension from Productivity"))
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(40, y, branding.get("subtitle", "A Responsible AI Dividend Model for Japan"))
    y -= 30

    def row(label: str, value: str):
        nonlocal y
        c.setFont("Helvetica-Bold", 10)
        c.drawString(40, y, f"{label}:")
        c.setFont("Helvetica", 10)
        c.drawString(190, y, str(value))
        y -= 16

    row("Company", company.get("company_name", ""))
    row("Industry", company.get("industry", ""))
    row("Scenario", sim.get("scenario_type", ""))
    row("Gross Productivity Gain", f"{result.get('gross_productivity_gain', 0):,.2f}")
    row("Total AI Cost", f"{result.get('total_ai_cost', 0):,.2f}")
    row("Adjusted Net Gain", f"{result.get('adjusted_net_gain', 0):,.2f}")
    row("Pension Contribution", f"{result.get('proposed_pension_contribution', 0):,.2f}")
    row("Platform Success Fee", f"{result.get('platform_success_fee', 0):,.2f}")
    row("Employer Retained Value", f"{result.get('employer_retained_value', 0):,.2f}")

    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, "Disclaimer")
    y -= 14
    c.setFont("Helvetica", 9)
    for line in [disclaimer[i : i + 100] for i in range(0, len(disclaimer), 100)]:
        c.drawString(40, y, line)
        y -= 12

    c.showPage()
    c.save()
    buf.seek(0)
    return buf.read()
