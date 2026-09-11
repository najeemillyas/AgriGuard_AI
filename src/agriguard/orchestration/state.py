"""Shared structured state exchanged between workflow nodes."""
from dataclasses import dataclass,field
from agriguard.models import CropCase,Classification,Evidence,WeatherResult,Advisory,SafetyAssessment,TraceEvent

@dataclass
class WorkflowState:
    case:CropCase
    classification:Classification|None=None
    evidence:list[Evidence]=field(default_factory=list)
    weather:WeatherResult|None=None
    advisory:Advisory|None=None
    safety:SafetyAssessment|None=None
    escalation_id:str|None=None
    trace:list[TraceEvent]=field(default_factory=list)
