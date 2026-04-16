from __future__ import annotations

from datetime import date, datetime

import streamlit as st

from core.database import execute, fetch_one
from core.validation import validate_ai_input


def render() -> None:
    st.header("AI Deployment Input")
    st.write("Capture post-AI operational metrics and AI-related costs.")
    cid = st.session_state.get("selected_company_id")
    if not cid:
        st.warning("Please select/save a company profile first.")
        return

    with st.form("ai_form"):
        ai_solution_name = st.text_input("AI Solution Name", value="AI Ops CoPilot")
        deployment_date = st.date_input("Deployment Date", value=date(2026, 2, 1))
        ai_tool_monthly_cost = st.number_input("AI Tool Monthly Cost", min_value=0.0, value=45000.0)
        implementation_cost = st.number_input("Implementation Cost", min_value=0.0, value=240000.0)
        training_cost = st.number_input("Training Cost", min_value=0.0, value=120000.0)
        new_monthly_working_hours = st.number_input("New Monthly Working Hours", min_value=0.0, value=15000.0)
        new_monthly_transactions = st.number_input("New Monthly Transactions", min_value=0.0, value=28000.0)
        new_average_handling_time_minutes = st.number_input(
            "New Average Handling Time (minutes)", min_value=0.0, value=9.0
        )
        new_error_rate_percent = st.number_input("New Error Rate (%)", min_value=0.0, max_value=100.0, value=2.8)
        new_rework_rate_percent = st.number_input("New Rework Rate (%)", min_value=0.0, max_value=100.0, value=2.1)
        new_overtime_hours_per_month = st.number_input("New Overtime Hours / Month", min_value=0.0, value=550.0)
        new_outsourcing_cost_per_month = st.number_input("New Outsourcing Cost / Month", min_value=0.0, value=85000.0)
        monetized_quality_improvement_value = st.number_input(
            "Monetized Quality Improvement Value", min_value=0.0, value=30000.0
        )
        additional_notes = st.text_area("Additional Notes")
        submitted = st.form_submit_button("Save AI Deployment Input")

    if submitted:
        data = {
            "ai_solution_name": ai_solution_name,
            "deployment_date": deployment_date,
            "ai_tool_monthly_cost": ai_tool_monthly_cost,
            "implementation_cost": implementation_cost,
            "training_cost": training_cost,
            "new_monthly_working_hours": new_monthly_working_hours,
            "new_monthly_transactions": new_monthly_transactions,
            "new_average_handling_time_minutes": new_average_handling_time_minutes,
            "new_error_rate_percent": new_error_rate_percent,
            "new_rework_rate_percent": new_rework_rate_percent,
            "new_overtime_hours_per_month": new_overtime_hours_per_month,
            "new_outsourcing_cost_per_month": new_outsourcing_cost_per_month,
            "monetized_quality_improvement_value": monetized_quality_improvement_value,
            "additional_notes": additional_notes,
        }
        ok, msg = validate_ai_input(data)
        if not ok:
            st.error(msg)
        else:
            now = datetime.utcnow().isoformat()
            execute(
                """
                INSERT INTO ai_inputs (company_id, ai_solution_name, deployment_date, ai_tool_monthly_cost, implementation_cost, training_cost,
                new_monthly_working_hours, new_monthly_transactions, new_average_handling_time_minutes, new_error_rate_percent,
                new_rework_rate_percent, new_overtime_hours_per_month, new_outsourcing_cost_per_month, monetized_quality_improvement_value,
                additional_notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    cid,
                    ai_solution_name,
                    str(deployment_date),
                    ai_tool_monthly_cost,
                    implementation_cost,
                    training_cost,
                    new_monthly_working_hours,
                    new_monthly_transactions,
                    new_average_handling_time_minutes,
                    new_error_rate_percent,
                    new_rework_rate_percent,
                    new_overtime_hours_per_month,
                    new_outsourcing_cost_per_month,
                    monetized_quality_improvement_value,
                    additional_notes,
                    now,
                    now,
                ),
            )
            st.success("AI deployment input saved.")

    if st.button("Load latest AI input for active company"):
        latest = fetch_one("SELECT * FROM ai_inputs WHERE company_id=? ORDER BY id DESC LIMIT 1", (cid,))
        if latest:
            st.json(latest)
