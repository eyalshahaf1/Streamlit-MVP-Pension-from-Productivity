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

    latest_baseline = fetch_one("SELECT * FROM baseline_inputs WHERE company_id=? ORDER BY id DESC LIMIT 1", (cid,))
    if latest_baseline:
        default_new_monthly_working_hours = float(latest_baseline["monthly_working_hours"]) * 0.85
        default_new_monthly_transactions = float(latest_baseline["monthly_transactions"]) * 1.1
        default_new_average_handling_time_minutes = float(latest_baseline["average_handling_time_minutes"]) * 0.9
        default_new_error_rate_percent = min(float(latest_baseline["error_rate_percent"]) * 0.9, 100.0)
        default_new_rework_rate_percent = min(float(latest_baseline["rework_rate_percent"]) * 0.9, 100.0)
        default_new_overtime_hours_per_month = float(latest_baseline["overtime_hours_per_month"]) * 0.7
        default_new_outsourcing_cost_per_month = float(latest_baseline["outsourcing_cost_per_month"]) * 0.8
    else:
        default_new_monthly_working_hours = 8500.0
        default_new_monthly_transactions = 12000.0
        default_new_average_handling_time_minutes = 9.0
        default_new_error_rate_percent = 2.8
        default_new_rework_rate_percent = 2.1
        default_new_overtime_hours_per_month = 200.0
        default_new_outsourcing_cost_per_month = 40000.0

    with st.form("ai_form"):
        ai_solution_name = st.text_input("AI Solution Name", value="AI Ops CoPilot")
        deployment_date = st.date_input("Deployment Date", value=date(2026, 2, 1))
        ai_tool_monthly_cost = st.number_input("AI Tool Monthly Cost", min_value=0.0, value=45000.0)
        implementation_cost = st.number_input("Implementation Cost", min_value=0.0, value=240000.0)
        training_cost = st.number_input("Training Cost", min_value=0.0, value=120000.0)
        new_monthly_working_hours = st.number_input(
            "New Monthly Working Hours", min_value=0.0, value=default_new_monthly_working_hours
        )
        new_monthly_transactions = st.number_input(
            "New Monthly Transactions", min_value=0.0, value=default_new_monthly_transactions
        )
        new_average_handling_time_minutes = st.number_input(
            "New Average Handling Time (minutes)", min_value=0.0, value=default_new_average_handling_time_minutes
        )
        new_error_rate_percent = st.number_input(
            "New Error Rate (%)", min_value=0.0, max_value=100.0, value=default_new_error_rate_percent
        )
        new_rework_rate_percent = st.number_input(
            "New Rework Rate (%)", min_value=0.0, max_value=100.0, value=default_new_rework_rate_percent
        )
        new_overtime_hours_per_month = st.number_input(
            "New Overtime Hours / Month", min_value=0.0, value=default_new_overtime_hours_per_month
        )
        new_outsourcing_cost_per_month = st.number_input(
            "New Outsourcing Cost / Month", min_value=0.0, value=default_new_outsourcing_cost_per_month
        )
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
