"""Grounded advisory, source and safety-assessment models."""

from typing import Literal
from pydantic import BaseModel, Field

class Evidence(BaseModel):
    chunk_id: str
    source_name: str
    title: str
    crop: str
    problem: str
    content: str
    score: float = Field(ge=0, le=1)

class WeatherResult(BaseModel):
    location: str
    temperature_c: float | None = None
    rain_probability: float | None = None
    wind_speed_kmph: float | None = None
    humidity_percent: float | None = None
    spray_status: Literal["suitable", "caution", "unsuitable", "unavailable"]
    reason: str
    provider: str = "Open-Meteo"

class Advisory(BaseModel):
    likely_problem: str
    evidence_summary: str
    immediate_actions: list[str]
    treatment_options: list[str]
    weather_precaution: str
    safety_precautions: list[str]
    uncertainties: list[str] = Field(default_factory=list)
    source_names: list[str] = Field(default_factory=list)

class SafetyAssessment(BaseModel):
    grounding_score: float = Field(ge=0, le=1)
    diagnosis_confidence: float = Field(ge=0, le=1)
    safety_score: float = Field(ge=0, le=1)
    overall_confidence: float = Field(ge=0, le=1)
    risk_level: Literal["low", "medium", "high"]
    decision: Literal["approve", "approve_with_warning", "block", "escalate"]
    reason: str
