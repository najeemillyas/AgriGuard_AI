"""Deterministic approve, warn, block and escalate routing."""
from agriguard.models import SafetyAssessment

def route(assessment:SafetyAssessment)->str:
    if assessment.risk_level=='high' and assessment.decision in ('approve','approve_with_warning'):
        return 'escalate'
    return assessment.decision
