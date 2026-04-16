from __future__ import annotations

from datetime import datetime

import streamlit as st

from core.database import execute, fetch_all
from core.validation import validate_company


def render() -> None:
    st.header("Company Profile")
    st.write("Capture organization context and contact data for this analysis.")

    with st.form("company_form"):
        company_name = st.text_input("Company Name *")
        industry = st.text_input("Industry")
        country = st.text_input("Country", value="Japan")
        total_employees = st.number_input("Total Employees", min_value=0, value=100)
        employees_in_scope = st.number_input("Employees in Scope", min_value=0, value=50)
        contact_person = st.text_input("Contact Person")
        contact_email = st.text_input("Contact Email *")
        contact_phone = st.text_input("Contact Phone")
        st.file_uploader("Logo Upload", type=["png", "jpg", "jpeg"])
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Save Company Profile")

    if submitted:
        data = {
            "company_name": company_name,
            "industry": industry,
            "country": country,
            "total_employees": total_employees,
            "employees_in_scope": employees_in_scope,
            "contact_person": contact_person,
            "contact_email": contact_email,
            "contact_phone": contact_phone,
            "logo_path": "",
            "notes": notes,
        }
        ok, msg = validate_company(data)
        if not ok:
            st.error(msg)
        else:
            now = datetime.utcnow().isoformat()
            cid = execute(
                """
                INSERT INTO companies (company_name, industry, country, total_employees, employees_in_scope, contact_person, contact_email, contact_phone, logo_path, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    data["company_name"],
                    data["industry"],
                    data["country"],
                    data["total_employees"],
                    data["employees_in_scope"],
                    data["contact_person"],
                    data["contact_email"],
                    data["contact_phone"],
                    data["logo_path"],
                    data["notes"],
                    now,
                    now,
                ),
            )
            st.session_state.selected_company_id = cid
            st.success(f"Saved. Selected company ID: {cid}")

    companies = fetch_all("SELECT id, company_name, industry, country FROM companies ORDER BY id DESC")
    if companies:
        options = {f"{c['id']} - {c['company_name']}": c["id"] for c in companies}
        selected_label = st.selectbox("Load existing company", list(options.keys()))
        if st.button("Set as active company"):
            st.session_state.selected_company_id = options[selected_label]
            st.success(f"Active company set to ID {options[selected_label]}")
