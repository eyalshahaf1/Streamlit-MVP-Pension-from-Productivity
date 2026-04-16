from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from typing import Any, Optional

from core.config import DB_PATH, DEFAULT_BRANDING


def get_conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        industry TEXT,
        country TEXT,
        total_employees INTEGER,
        employees_in_scope INTEGER,
        contact_person TEXT,
        contact_email TEXT,
        contact_phone TEXT,
        logo_path TEXT,
        notes TEXT,
        created_at TEXT,
        updated_at TEXT
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS baseline_inputs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER NOT NULL,
        department_name TEXT,
        reporting_period TEXT,
        employees_in_scope INTEGER,
        monthly_working_hours REAL,
        average_loaded_hourly_cost REAL,
        monthly_transactions REAL,
        average_handling_time_minutes REAL,
        error_rate_percent REAL,
        rework_rate_percent REAL,
        overtime_hours_per_month REAL,
        outsourcing_cost_per_month REAL,
        admin_overhead_cost_per_month REAL,
        additional_notes TEXT,
        created_at TEXT,
        updated_at TEXT
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS ai_inputs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER NOT NULL,
        ai_solution_name TEXT,
        deployment_date TEXT,
        ai_tool_monthly_cost REAL,
        implementation_cost REAL,
        training_cost REAL,
        new_monthly_working_hours REAL,
        new_monthly_transactions REAL,
        new_average_handling_time_minutes REAL,
        new_error_rate_percent REAL,
        new_rework_rate_percent REAL,
        new_overtime_hours_per_month REAL,
        new_outsourcing_cost_per_month REAL,
        monetized_quality_improvement_value REAL,
        additional_notes TEXT,
        created_at TEXT,
        updated_at TEXT
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS simulation_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER NOT NULL,
        contribution_rate_percent REAL,
        platform_setup_fee REAL,
        annual_platform_fee REAL,
        success_fee_percent REAL,
        confidence_haircut_percent REAL,
        scenario_type TEXT,
        gross_productivity_gain REAL,
        total_ai_cost REAL,
        adjusted_net_gain REAL,
        proposed_pension_contribution REAL,
        platform_success_fee REAL,
        employer_retained_value REAL,
        created_at TEXT
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS branding_settings (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        product_name TEXT,
        subtitle TEXT,
        logo_path TEXT,
        founder_name TEXT,
        contact_email TEXT,
        contact_phone TEXT,
        website TEXT,
        linkedin_url TEXT,
        footer_text TEXT,
        company_description TEXT,
        updated_at TEXT
    )""")

    now = datetime.utcnow().isoformat()
    c.execute("SELECT COUNT(*) AS cnt FROM branding_settings")
    if c.fetchone()["cnt"] == 0:
        c.execute(
            """
        INSERT INTO branding_settings
        (id, product_name, subtitle, logo_path, founder_name, contact_email, contact_phone, website, linkedin_url, footer_text, company_description, updated_at)
        VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                DEFAULT_BRANDING["product_name"],
                DEFAULT_BRANDING["subtitle"],
                DEFAULT_BRANDING["logo_path"],
                DEFAULT_BRANDING["founder_name"],
                DEFAULT_BRANDING["contact_email"],
                DEFAULT_BRANDING["contact_phone"],
                DEFAULT_BRANDING["website"],
                DEFAULT_BRANDING["linkedin_url"],
                DEFAULT_BRANDING["footer_text"],
                DEFAULT_BRANDING["company_description"],
                now,
            ),
        )

    conn.commit()
    conn.close()


def seed_demo_data() -> None:
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) AS cnt FROM companies")
    if c.fetchone()["cnt"] > 0:
        conn.close()
        return

    now = datetime.utcnow().isoformat()
    c.execute(
        """
    INSERT INTO companies
    (company_name, industry, country, total_employees, employees_in_scope, contact_person, contact_email, contact_phone, logo_path, notes, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            "Demo Manufacturing KK",
            "Manufacturing",
            "Japan",
            500,
            120,
            "Aiko Tanaka",
            "aiko@example.com",
            "+81-90-1234-5678",
            "",
            "Seed demo company",
            now,
            now,
        ),
    )
    company_id = c.lastrowid

    c.execute(
        """
    INSERT INTO baseline_inputs
    (company_id, department_name, reporting_period, employees_in_scope, monthly_working_hours, average_loaded_hourly_cost,
     monthly_transactions, average_handling_time_minutes, error_rate_percent, rework_rate_percent, overtime_hours_per_month,
     outsourcing_cost_per_month, admin_overhead_cost_per_month, additional_notes, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            company_id,
            "Operations",
            "2026-01",
            120,
            18000,
            35.0,
            25000,
            12.0,
            4.2,
            3.1,
            900,
            120000,
            40000,
            "Pre-AI baseline",
            now,
            now,
        ),
    )

    c.execute(
        """
    INSERT INTO ai_inputs
    (company_id, ai_solution_name, deployment_date, ai_tool_monthly_cost, implementation_cost, training_cost, new_monthly_working_hours,
     new_monthly_transactions, new_average_handling_time_minutes, new_error_rate_percent, new_rework_rate_percent,
     new_overtime_hours_per_month, new_outsourcing_cost_per_month, monetized_quality_improvement_value, additional_notes, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            company_id,
            "AI Ops CoPilot",
            "2026-02-01",
            45000,
            240000,
            120000,
            15000,
            28000,
            9.0,
            2.8,
            2.1,
            550,
            85000,
            30000,
            "Post-AI first quarter",
            now,
            now,
        ),
    )

    conn.commit()
    conn.close()


def fetch_one(query: str, params: tuple = ()) -> Optional[dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params)
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def fetch_all(query: str, params: tuple = ()) -> list[dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def execute(query: str, params: tuple = ()) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id
