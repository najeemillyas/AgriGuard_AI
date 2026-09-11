"""Persist an expert-review escalation record."""
from uuid import uuid4
from agriguard.models import EscalationRecord
from agriguard.orchestration.state import WorkflowState
from agriguard.storage.case_repository import CaseRepository

def create_expert_escalation(state:WorkflowState,repo:CaseRepository)->str:
    eid=f"AGR-ESC-{uuid4().hex[:10].upper()}"
    record=EscalationRecord(escalation_id=eid,case_id=state.case.case_id,case=state.case.model_dump(mode='json'),classification=state.classification.model_dump(),evidence=[x.model_dump() for x in state.evidence],weather=state.weather.model_dump() if state.weather else None,advisory=state.advisory.model_dump() if state.advisory else None,safety=state.safety.model_dump(),reason=state.safety.reason)
    repo.save_escalation(record);return eid
