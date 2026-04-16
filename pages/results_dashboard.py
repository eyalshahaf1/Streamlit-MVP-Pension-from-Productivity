from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from core.calculations import run_simulation
from core.database import fetch_one


def render() -> None:
    st.header("Results Dashboard")
    st.write("View KPI changes, financial outcomes, scenario comparison, and management interpretation.")
    cid = st.session_state.get("selected_company_id")
    if not cid:
        st.warning("Please select a company first.")
        return

    baseline = fetch_one("SELECT * FROM baseline_inputs WHERE company_id=? ORDER BY id DESC LIMIT 1", (cid,))
    ai = fetch_one("SELECT * FROM ai_inputs WHERE company_id=? ORDER BY id DESC LIMIT 1", (cid,))
    if not baseline or not ai:
        st.warning("Missing baseline or AI inputs.")
        return

    sim = {
        "contribution_rate_percent": 3.0,
        "platform_setup_fee": 0.0,
        "annual_platform_fee": 50000.0,
        "success_fee_percent": 10.0,
        "confidence_haircut_percent": 10.0,
        "scenario_type": "Base",
    }
    result = run_simulation(baseline, ai, sim)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Hours (Before)", f"{baseline['monthly_working_hours']:,.0f}")
    c2.metric("Hours (After)", f"{ai['new_monthly_working_hours']:,.0f}")
    c3.metric("Error % (Before)", f"{baseline['error_rate_percent']:.2f}")
    c4.metric("Error % (After)", f"{ai['new_error_rate_percent']:.2f}")

    st.subheader("Financial Summary")
    f1, f2, f3 = st.columns(3)
    f1.metric("Adjusted Net Gain", f"{result.adjusted_net_gain:,.2f}")
    f2.metric("Pension Contribution", f"{result.proposed_pension_contribution:,.2f}")
    f3.metric("Employer Retained", f"{result.employer_retained_value:,.2f}")

    st.subheader("Charts")
    df_hours = pd.DataFrame({"Stage": ["Baseline", "Post-AI"], "Hours": [baseline["monthly_working_hours"], ai["new_monthly_working_hours"]]})
    st.plotly_chart(px.bar(df_hours, x="Stage", y="Hours", title="Baseline vs Post-AI Hours"), use_container_width=True)

    df_err = pd.DataFrame({"Stage": ["Baseline", "Post-AI"], "Error Rate": [baseline["error_rate_percent"], ai["new_error_rate_percent"]]})
    st.plotly_chart(px.bar(df_err, x="Stage", y="Error Rate", title="Baseline vs Post-AI Error Rate"), use_container_width=True)

    pie_df = pd.DataFrame(
        {
            "Category": ["Employer Retained", "Pension Contribution", "Platform Success Fee"],
            "Value": [result.employer_retained_value, result.proposed_pension_contribution, result.platform_success_fee],
        }
    )
    st.plotly_chart(px.pie(pie_df, names="Category", values="Value", title="Allocation Breakdown"), use_container_width=True)

    scenario_rates = [1, 3, 5]
    scenario_vals = []
    for r in scenario_rates:
        sim_r = {**sim, "contribution_rate_percent": float(r)}
        rr = run_simulation(baseline, ai, sim_r)
        scenario_vals.append(rr.proposed_pension_contribution)
    scen_df = pd.DataFrame({"Rate": ["1%", "3%", "5%"], "Pension Contribution": scenario_vals})
    st.plotly_chart(px.bar(scen_df, x="Rate", y="Pension Contribution", title="Scenario Comparison"), use_container_width=True)

    st.subheader("Management Interpretation")
    cfo, hr, esg = st.columns(3)
    cfo.success("**CFO View**\n\nNet gain remains positive after haircut and dividend allocation.")
    hr.info("**HR View**\n\nModel links AI productivity to shared workforce outcomes.")
    esg.info("**ESG / Impact View**\n\nSupports responsible AI value-sharing narrative.")
