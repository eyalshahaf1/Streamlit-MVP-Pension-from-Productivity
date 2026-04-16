from __future__ import annotations

import streamlit as st

from core.database import init_db, seed_demo_data
from core.config import DISCLAIMER_TEXT
from pages import (
    home,
    company_profile,
    baseline_input,
    ai_input,
    dividend_simulator,
    results_dashboard,
    executive_report,
    admin_branding,
)

st.set_page_config(page_title="Pension from Productivity", layout="wide")


def ensure_bootstrap() -> None:
    init_db()
    if "db_initialized" not in st.session_state:
        st.session_state.db_initialized = True
    if "selected_company_id" not in st.session_state:
        st.session_state.selected_company_id = None
    if "seeded" not in st.session_state:
        seed_demo_data()
        st.session_state.seeded = True


def main() -> None:
    ensure_bootstrap()
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        [
            "Home",
            "Company Profile",
            "Baseline Input",
            "AI Deployment Input",
            "Dividend Simulator",
            "Results Dashboard",
            "Executive Report",
            "Admin / Branding",
        ],
    )

    page_map = {
        "Home": home.render,
        "Company Profile": company_profile.render,
        "Baseline Input": baseline_input.render,
        "AI Deployment Input": ai_input.render,
        "Dividend Simulator": dividend_simulator.render,
        "Results Dashboard": results_dashboard.render,
        "Executive Report": executive_report.render,
        "Admin / Branding": admin_branding.render,
    }

    page_map[page]()
    st.divider()
    st.caption(DISCLAIMER_TEXT)


if __name__ == "__main__":
    main()
