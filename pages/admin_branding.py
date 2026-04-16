from __future__ import annotations

import os
from datetime import datetime

import streamlit as st

from core.config import DEFAULT_BRANDING
from core.database import execute, fetch_one


def render() -> None:
    st.header("Admin / Branding")
    st.write("Configure product branding and contact details used on Home and Report pages.")

    settings = fetch_one("SELECT * FROM branding_settings WHERE id=1") or DEFAULT_BRANDING

    with st.form("branding_form"):
        product_name = st.text_input("Product Name", value=settings.get("product_name", ""))
        subtitle = st.text_input("Subtitle", value=settings.get("subtitle", ""))
        logo_upload = st.file_uploader("Logo Upload", type=["png", "jpg", "jpeg"])
        founder_name = st.text_input("Founder Name", value=settings.get("founder_name", ""))
        contact_email = st.text_input("Contact Email", value=settings.get("contact_email", ""))
        contact_phone = st.text_input("Contact Phone", value=settings.get("contact_phone", ""))
        website = st.text_input("Website", value=settings.get("website", ""))
        linkedin_url = st.text_input("LinkedIn URL", value=settings.get("linkedin_url", ""))
        footer_text = st.text_input("Footer Text", value=settings.get("footer_text", ""))
        company_description = st.text_area("Company Description", value=settings.get("company_description", ""))
        submitted = st.form_submit_button("Save Branding")

    logo_path = settings.get("logo_path", "")
    if submitted:
        if logo_upload is not None:
            os.makedirs("assets", exist_ok=True)
            logo_path = f"assets/{logo_upload.name}"
            with open(logo_path, "wb") as f:
                f.write(logo_upload.getbuffer())

        now = datetime.utcnow().isoformat()
        execute(
            """
        INSERT OR REPLACE INTO branding_settings
        (id, product_name, subtitle, logo_path, founder_name, contact_email, contact_phone, website, linkedin_url, footer_text, company_description, updated_at)
        VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                product_name,
                subtitle,
                logo_path,
                founder_name,
                contact_email,
                contact_phone,
                website,
                linkedin_url,
                footer_text,
                company_description,
                now,
            ),
        )
        st.success("Branding updated.")
