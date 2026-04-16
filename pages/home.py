from __future__ import annotations

import streamlit as st

from core.config import DEFAULT_BRANDING
from core.database import fetch_one


def render() -> None:
    branding = fetch_one("SELECT * FROM branding_settings WHERE id = 1") or DEFAULT_BRANDING

    if branding.get("logo_path"):
        st.image(branding["logo_path"], width=140)

    st.title(branding.get("product_name", "Pension from Productivity"))
    st.subheader(branding.get("subtitle", "A Responsible AI Dividend Model for Japan"))
    st.write("Measure AI productivity gains, simulate a pension productivity dividend, and generate executive-ready reports.")

    col1, col2, col3 = st.columns(3)
    col1.info("**Measure AI productivity**\n\nCapture baseline vs post-AI operational outcomes.")
    col2.info("**Simulate pension allocation**\n\nTest 1%, 3%, 5% or custom contribution rates.")
    col3.info("**Generate executive reports**\n\nExport PDF, CSV, and JSON summaries for stakeholders.")

    if st.button("Start New Analysis", type="primary"):
        st.success("Use the sidebar to complete Company Profile → Baseline → AI Input → Simulator.")

    st.divider()
    st.markdown(f"**Founder / Company:** {branding.get('founder_name', '')}")
    st.markdown(f"**Email:** {branding.get('contact_email', '')}")
    st.markdown(f"**Phone/WhatsApp:** {branding.get('contact_phone', '')}")
    st.markdown(f"**LinkedIn:** {branding.get('linkedin_url', '')}")
    st.markdown(f"**Website:** {branding.get('website', '')}")
    st.caption(branding.get("footer_text", ""))
