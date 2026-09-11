"""Trace event and escalation-record models."""

from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field

class TraceEvent(BaseModel):
    case_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    component: str
    action: str
    outcome: str
    duration_ms: float = 0
    reason: str = ""
    details: dict[str, Any] = Field(default_factory=dict)

class EscalationRecord(BaseModel):
    escalation_id: str
    case_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "pending_expert_review"
    case: dict[str, Any]
    classification: dict[str, Any]
    evidence: list[dict[str, Any]]
    weather: dict[str, Any] | None
    advisory: dict[str, Any] | None
    safety: dict[str, Any]
    reason: str
