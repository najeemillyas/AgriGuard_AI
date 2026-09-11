"""Crop case and classification models."""

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator

Category = Literal["insect_attack", "fungal_disease", "nutrient_deficiency", "unclear"]

class CropCase(BaseModel):
    case_id: str = Field(default_factory=lambda: f"AGR-CASE-{uuid4().hex[:10].upper()}")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    crop: str
    stage: str
    location: str
    symptoms: str
    severity: Literal["low", "medium", "severe"] = "medium"

    @field_validator("crop", "stage", "location", "symptoms")
    @classmethod
    def required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field is required")
        return value

class Classification(BaseModel):
    category: Category
    rationale: str
    missing_information: list[str] = Field(default_factory=list)
    red_flags: list[str] = Field(default_factory=list)
    prompt_injection_detected: bool = False
