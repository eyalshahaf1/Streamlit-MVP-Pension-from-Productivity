from __future__ import annotations

import streamlit as st

from core.calculations import run_simulation
from core.config import DISCLAIMER_TEXT
from core.database import fetch_one
from core.reporting import build_pdf_report, summary_dataframe, to_json_bytes


def render() -> None:
    st.header("Executive Report")
    st.write("Generate stakeholder-facing summary and downloadable report artifacts.")
    cid = st.session_state.get("selected_company_id")
    if not cid:
        st.warning("Please select a company first.")
        return

    branding = fetch_one("SELECT * FROM branding_settings WHERE id=1")
    company = fetch_one("SELECT * FROM companies WHERE id=?", (cid,))
    baseline = fetch_one("SELECT * FROM baseline_inputs WHERE company_id=? ORDER BY id DESC LIMIT 1", (cid,))
    ai = fetch_one("SELECT * FROM ai_inputs WHERE company_id=? ORDER BY id DESC LIMIT 1", (cid,))

    if not (company and baseline and ai):
        st.warning("Missing required inputs.")
        return

    sim = {
        "contribution_rate_percent": 3.0,
        "platform_setup_fee": 0.0,
        "annual_platform_fee": 50000.0,
        "success_fee_percent": 10.0,
        "confidence_haircut_percent": 10.0,
        "scenario_type": "Base",
    }
    result = run_simulation(baseline, ai, sim).__dict__

    st.subheader("Headline")
    st.write(f"{branding['product_name']} — Executive Summary")
    st.write(branding["subtitle"])

    st.subheader("Company Snapshot")
    st.write(f"**{company['company_name']}** ({company['industry']}, {company['country']})")

    st.subheader("Productivity Results")
    st.write(f"- Gross productivity gain: **{result['gross_productivity_gain']:,.2f}**")
    st.write(f"- Adjusted net gain: **{result['adjusted_net_gain']:,.2f}**")
    st.write(f"- Proposed pension allocation (3%): **{result['proposed_pension_contribution']:,.2f}**")
    st.write(f"- Employer retained value: **{result['employer_retained_value']:,.2f}**")

    st.subheader("Interpretation")
    st.write("This scenario indicates measurable AI-enabled value creation with an optional shared-value allocation framework.")

    st.subheader("Disclaimer")
    st.caption(DISCLAIMER_TEXT)

    df = summary_dataframe(company, baseline, ai, sim, result)
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    json_bytes = to_json_bytes(
        {"branding": branding, "company": company, "baseline": baseline, "ai": ai, "simulation": sim, "result": result}
    )
    pdf_bytes = build_pdf_report(branding, company, baseline, ai, sim, result, DISCLAIMER_TEXT)

    c1, c2, c3 = st.columns(3)
    c1.download_button("Download PDF", pdf_bytes, file_name="executive_report.pdf", mime="application/pdf")
    c2.download_button("Download CSV summary", csv_bytes, file_name="executive_summary.csv", mime="text/csv")
    c3.download_button(
        "Download JSON summary", json_bytes, file_name="executive_summary.json", mime="application/json"
    )
