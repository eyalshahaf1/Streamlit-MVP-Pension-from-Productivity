from __future__ import annotations

from datetime import datetime

import streamlit as st

from core.calculations import run_simulation
from core.database import execute, fetch_one
from core.validation import validate_simulation


def render() -> None:
    st.header("Dividend Simulator")
    st.write("Calculate value creation and pension productivity dividend allocations.")
    cid = st.session_state.get("selected_company_id")
    if not cid:
        st.warning("Please select a company first.")
        return

    baseline = fetch_one("SELECT * FROM baseline_inputs WHERE company_id=? ORDER BY id DESC LIMIT 1", (cid,))
    ai = fetch_one("SELECT * FROM ai_inputs WHERE company_id=? ORDER BY id DESC LIMIT 1", (cid,))
    if not baseline or not ai:
        st.warning("Missing baseline or AI deployment inputs.")
        return

    rate_option = st.selectbox("Contribution Rate (%)", ["1", "3", "5", "Custom"])
    contribution_rate_percent = (
        st.number_input("Custom Rate", min_value=0.0, max_value=100.0, value=3.0) if rate_option == "Custom" else float(rate_option)
    )
    platform_setup_fee = st.number_input("Platform Setup Fee", min_value=0.0, value=0.0)
    annual_platform_fee = st.number_input("Annual Platform Fee", min_value=0.0, value=50000.0)
    success_fee_percent = st.number_input("Success Fee (%)", min_value=0.0, max_value=100.0, value=10.0)
    confidence_haircut_percent = st.selectbox("Confidence Haircut (%)", [0, 10, 20])
    scenario_type = st.selectbox("Scenario Type", ["Conservative", "Base", "Optimistic"])

    st.markdown("### Formula")
    st.code("""gross = hours_saved_value + overtime_savings_value + outsourcing_savings + monetized_quality_improvement_value
total_ai_cost = ai_tool_monthly_cost + implementation_cost/12 + training_cost/12
adjusted_net_gain = (gross - total_ai_cost) * (1 - confidence_haircut/100)
proposed_contribution = adjusted_net_gain * (contribution_rate/100)
platform_success_fee = proposed_contribution * (success_fee/100)
employer_retained = adjusted_net_gain - proposed_contribution - platform_success_fee""")

    if st.button("Run Simulation", type="primary"):
        sim_input = {
            "contribution_rate_percent": contribution_rate_percent,
            "platform_setup_fee": platform_setup_fee,
            "annual_platform_fee": annual_platform_fee,
            "success_fee_percent": success_fee_percent,
            "confidence_haircut_percent": confidence_haircut_percent,
            "scenario_type": scenario_type,
        }
        ok, msg = validate_simulation(sim_input)
        if not ok:
            st.error(msg)
            return

        if contribution_rate_percent > 20:
            st.warning("Contribution rate may be unrealistic for early-stage adoption.")
        result = run_simulation(baseline, ai, sim_input)
        st.session_state.latest_result = result.__dict__
        st.metric("Gross Productivity Gain", f"{result.gross_productivity_gain:,.2f}")
        st.metric("Total AI Cost", f"{result.total_ai_cost:,.2f}")
        st.metric("Adjusted Net Gain", f"{result.adjusted_net_gain:,.2f}")
        st.metric("Proposed Pension Contribution", f"{result.proposed_pension_contribution:,.2f}")
        st.metric("Platform Success Fee", f"{result.platform_success_fee:,.2f}")
        st.metric("Annual Platform Fee", f"{annual_platform_fee:,.2f}")
        st.metric("Employer Retained Value", f"{result.employer_retained_value:,.2f}")

        if result.employer_retained_value < 0:
            st.error("Warning: Employer retained value is negative.")
        if result.total_ai_cost > result.gross_productivity_gain:
            st.warning("AI cost exceeds productivity gains in this scenario.")

        now = datetime.utcnow().isoformat()
        execute(
            """
        INSERT INTO simulation_runs (company_id, contribution_rate_percent, platform_setup_fee, annual_platform_fee, success_fee_percent,
        confidence_haircut_percent, scenario_type, gross_productivity_gain, total_ai_cost, adjusted_net_gain,
        proposed_pension_contribution, platform_success_fee, employer_retained_value, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                cid,
                contribution_rate_percent,
                platform_setup_fee,
                annual_platform_fee,
                success_fee_percent,
                confidence_haircut_percent,
                scenario_type,
                result.gross_productivity_gain,
                result.total_ai_cost,
                result.adjusted_net_gain,
                result.proposed_pension_contribution,
                result.platform_success_fee,
                result.employer_retained_value,
                now,
            ),
        )
        st.success("Simulation saved.")
