from __future__ import annotations

import os

DB_PATH = os.getenv("APP_DB_PATH", "data/pension_productivity.db")
ENABLE_SUPABASE = os.getenv("ENABLE_SUPABASE", "false").lower() == "true"

DEFAULT_BRANDING = {
    "product_name": "Pension from AI Productivity",
    "subtitle": "A Responsible AI Dividend Model for Japan",
    "logo_path": "",
    "founder_name": "Eyal Shahaf",
    "contact_email": "eyal@eyalshahaf.com",
    "contact_phone": "+972542000747",
    "website": "https://www.eyalshahaf.com",
    "linkedin_url": "https://www.linkedin.com/in/eyalshahaf/",
    "footer_text": "© 2026 Pension from AI Productivity. All rights reserved.",
    "company_description": "Prototype for AI productivity measurement and pension dividend simulation.",
}

DISCLAIMER_TEXT = (
    "This prototype is a measurement, simulation, and reporting tool only. "
    "It does not operate as a pension administrator, financial institution, "
    "payment service, or investment advisor."
)
