from __future__ import annotations

from pydantic import ValidationError

from core.models import AIInput, BaselineInput, CompanyProfile, SimulationInput


def validate_company(data: dict) -> tuple[bool, str]:
    try:
        CompanyProfile(**data)
        return True, "OK"
    except ValidationError as e:
        return False, str(e)


def validate_baseline(data: dict) -> tuple[bool, str]:
    try:
        BaselineInput(**data)
        return True, "OK"
    except ValidationError as e:
        return False, str(e)


def validate_ai_input(data: dict) -> tuple[bool, str]:
    try:
        AIInput(**data)
        return True, "OK"
    except ValidationError as e:
        return False, str(e)


def validate_simulation(data: dict) -> tuple[bool, str]:
    try:
        SimulationInput(**data)
        return True, "OK"
    except ValidationError as e:
        return False, str(e)
