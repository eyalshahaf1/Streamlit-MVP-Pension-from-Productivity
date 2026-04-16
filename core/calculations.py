from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SimulationResult:
    hours_saved: float
    hours_saved_value: float
    overtime_savings: float
    overtime_savings_value: float
    outsourcing_savings: float
    gross_productivity_gain: float
    total_ai_cost: float
    net_productivity_gain: float
    adjusted_net_gain: float
    proposed_pension_contribution: float
    platform_success_fee: float
    employer_retained_value: float


def run_simulation(
    baseline: dict,
    ai: dict,
    sim: dict,
    implementation_amort_months: int = 12,
) -> SimulationResult:
    hours_saved = baseline["monthly_working_hours"] - ai["new_monthly_working_hours"]
    hours_saved_value = hours_saved * baseline["average_loaded_hourly_cost"]

    overtime_savings = baseline["overtime_hours_per_month"] - ai["new_overtime_hours_per_month"]
    overtime_savings_value = overtime_savings * baseline["average_loaded_hourly_cost"]

    outsourcing_savings = baseline["outsourcing_cost_per_month"] - ai["new_outsourcing_cost_per_month"]

    gross_productivity_gain = (
        hours_saved_value
        + overtime_savings_value
        + outsourcing_savings
        + ai["monetized_quality_improvement_value"]
    )

    total_ai_cost = (
        ai["ai_tool_monthly_cost"]
        + (ai["implementation_cost"] / implementation_amort_months)
        + (ai["training_cost"] / implementation_amort_months)
    )

    net_productivity_gain = gross_productivity_gain - total_ai_cost
    adjusted_net_gain = net_productivity_gain * (1 - sim["confidence_haircut_percent"] / 100)
    proposed_pension_contribution = adjusted_net_gain * (sim["contribution_rate_percent"] / 100)
    platform_success_fee = proposed_pension_contribution * (sim["success_fee_percent"] / 100)

    employer_retained_value = (
        adjusted_net_gain
        - proposed_pension_contribution
        - platform_success_fee
    )

    return SimulationResult(
        hours_saved=hours_saved,
        hours_saved_value=hours_saved_value,
        overtime_savings=overtime_savings,
        overtime_savings_value=overtime_savings_value,
        outsourcing_savings=outsourcing_savings,
        gross_productivity_gain=gross_productivity_gain,
        total_ai_cost=total_ai_cost,
        net_productivity_gain=net_productivity_gain,
        adjusted_net_gain=adjusted_net_gain,
        proposed_pension_contribution=proposed_pension_contribution,
        platform_success_fee=platform_success_fee,
        employer_retained_value=employer_retained_value,
    )
