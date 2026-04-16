from __future__ import annotations

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, model_validator

ScenarioType = Literal["Conservative", "Base", "Optimistic"]


class CompanyProfile(BaseModel):
    company_name: str = Field(min_length=1)
    industry: Optional[str] = ""
    country: Optional[str] = "Japan"
    total_employees: int = Field(ge=0)
    employees_in_scope: int = Field(ge=0)
    contact_person: Optional[str] = ""
    contact_email: EmailStr
    contact_phone: Optional[str] = ""
    logo_path: Optional[str] = ""
    notes: Optional[str] = ""

    @model_validator(mode="after")
    def validate_scope(self):
        if self.employees_in_scope > self.total_employees:
            raise ValueError("employees_in_scope cannot exceed total_employees")
        return self


class BaselineInput(BaseModel):
    department_name: str
    reporting_period: str
    employees_in_scope: int = Field(ge=0)
    monthly_working_hours: float = Field(ge=0)
    average_loaded_hourly_cost: float = Field(ge=0)
    monthly_transactions: float = Field(ge=0)
    average_handling_time_minutes: float = Field(ge=0)
    error_rate_percent: float = Field(ge=0, le=100)
    rework_rate_percent: float = Field(ge=0, le=100)
    overtime_hours_per_month: float = Field(ge=0)
    outsourcing_cost_per_month: float = Field(ge=0)
    admin_overhead_cost_per_month: float = Field(ge=0)
    additional_notes: Optional[str] = ""


class AIInput(BaseModel):
    ai_solution_name: str
    deployment_date: date
    ai_tool_monthly_cost: float = Field(ge=0)
    implementation_cost: float = Field(ge=0)
    training_cost: float = Field(ge=0)
    new_monthly_working_hours: float = Field(ge=0)
    new_monthly_transactions: float = Field(ge=0)
    new_average_handling_time_minutes: float = Field(ge=0)
    new_error_rate_percent: float = Field(ge=0, le=100)
    new_rework_rate_percent: float = Field(ge=0, le=100)
    new_overtime_hours_per_month: float = Field(ge=0)
    new_outsourcing_cost_per_month: float = Field(ge=0)
    monetized_quality_improvement_value: float = Field(ge=0)
    additional_notes: Optional[str] = ""


class SimulationInput(BaseModel):
    contribution_rate_percent: float = Field(ge=0, le=100)
    platform_setup_fee: float = Field(ge=0)
    annual_platform_fee: float = Field(ge=0)
    success_fee_percent: float = Field(ge=0, le=100)
    confidence_haircut_percent: float = Field(ge=0, le=100)
    scenario_type: ScenarioType
