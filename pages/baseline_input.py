from __future__ import annotations

from datetime import datetime

import streamlit as st

from core.database import execute, fetch_one
from core.validation import validate_baseline


def render() -> None:
    st.header("Baseline Input")
    st.write("Capture pre-AI operational metrics.")
    cid = st.session_state.get("selected_company_id")
    if not cid:
        st.warning("Please select/save a company profile first.")
        return

    with st.form("baseline_form"):
        department_name = st.text_input("Department Name", help="Team or function under analysis.")
        reporting_period = st.text_input("Reporting Period", value="2026-01", help="Format YYYY-MM.")
        employees_in_scope = st.number_input("Employees in Scope", min_value=0, value=50)
        monthly_working_hours = st.number_input("Monthly Working Hours", min_value=0.0, value=10000.0)
        average_loaded_hourly_cost = st.number_input("Average Loaded Hourly Cost", min_value=0.0, value=30.0)
        monthly_transactions = st.number_input("Monthly Transactions", min_value=0.0, value=10000.0)
        average_handling_time_minutes = st.number_input("Average Handling Time (minutes)", min_value=0.0, value=10.0)
        error_rate_percent = st.number_input("Error Rate (%)", min_value=0.0, max_value=100.0, value=3.0)
        rework_rate_percent = st.number_input("Rework Rate (%)", min_value=0.0, max_value=100.0, value=2.0)
        overtime_hours_per_month = st.number_input("Overtime Hours / Month", min_value=0.0, value=300.0)
        outsourcing_cost_per_month = st.number_input("Outsourcing Cost / Month", min_value=0.0, value=50000.0)
        admin_overhead_cost_per_month = st.number_input("Admin Overhead Cost / Month", min_value=0.0, value=15000.0)
        additional_notes = st.text_area("Additional Notes")
        submitted = st.form_submit_button("Save Baseline Input")

    if submitted:
        data = dict(
            department_name=department_name,
            reporting_period=reporting_period,
            employees_in_scope=employees_in_scope,
            monthly_working_hours=monthly_working_hours,
            average_loaded_hourly_cost=average_loaded_hourly_cost,
            monthly_transactions=monthly_transactions,
            average_handling_time_minutes=average_handling_time_minutes,
            error_rate_percent=error_rate_percent,
            rework_rate_percent=rework_rate_percent,
            overtime_hours_per_month=overtime_hours_per_month,
            outsourcing_cost_per_month=outsourcing_cost_per_month,
            admin_overhead_cost_per_month=admin_overhead_cost_per_month,
            additional_notes=additional_notes,
        )
        ok, msg = validate_baseline(data)
        if not ok:
            st.error(msg)
        else:
            now = datetime.utcnow().isoformat()
            execute(
                """
            INSERT INTO baseline_inputs (company_id, department_name, reporting_period, employees_in_scope, monthly_working_hours,
            average_loaded_hourly_cost, monthly_transactions, average_handling_time_minutes, error_rate_percent, rework_rate_percent,
            overtime_hours_per_month, outsourcing_cost_per_month, admin_overhead_cost_per_month, additional_notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    cid,
                    department_name,
                    reporting_period,
                    employees_in_scope,
                    monthly_working_hours,
                    average_loaded_hourly_cost,
                    monthly_transactions,
                    average_handling_time_minutes,
                    error_rate_percent,
                    rework_rate_percent,
                    overtime_hours_per_month,
                    outsourcing_cost_per_month,
                    admin_overhead_cost_per_month,
                    additional_notes,
                    now,
                    now,
                ),
            )
            st.success("Baseline input saved.")

    if st.button("Load latest baseline for active company"):
        latest = fetch_one("SELECT * FROM baseline_inputs WHERE company_id=? ORDER BY id DESC LIMIT 1", (cid,))
        if latest:
            st.json(latest)
