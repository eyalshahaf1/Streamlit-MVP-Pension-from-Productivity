from __future__ import annotations

import os

DB_PATH = os.getenv("APP_DB_PATH", "data/pension_productivity.db")
ENABLE_SUPABASE = os.getenv("ENABLE_SUPABASE", "false").lower() == "true"

DEFAULT_BRANDING = {
    "product_name": "Pension from Productivity",
    "subtitle": "A Responsible AI Dividend Model for Japan",
    "logo_path": "",
    "founder_name": "Founder Name",
    "contact_email": "info@example.com",
    "contact_phone": "+81-00-0000-0000",
    "website": "https://example.com",
    "linkedin_url": "https://linkedin.com/in/example",
    "footer_text": "© 2026 Pension from Productivity. All rights reserved.",
    "company_description": "Prototype for AI productivity measurement and pension dividend simulation.",
}

DISCLAIMER_TEXT = (
    "This prototype is a measurement, simulation, and reporting tool only. "
    "It does not operate as a pension administrator, financial institution, "
    "payment service, or investment advisor."
)
