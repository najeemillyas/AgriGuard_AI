"""AGR-TC-028 through AGR-TC-033 and AGR-TC-056."""
from agriguard.models import SafetyAssessment
from agriguard.orchestration.router import route

def assessment(score,decision,risk='low'):
    return SafetyAssessment(grounding_score=.8,diagnosis_confidence=.8,safety_score=.8,overall_confidence=score,risk_level=risk,decision=decision,reason='fixture')
def test_boundary_routes_are_deterministic():
    assert route(assessment(.70,'approve'))=='approve'
    assert route(assessment(.69,'approve_with_warning','medium'))=='approve_with_warning'
    assert route(assessment(.50,'approve_with_warning','medium'))=='approve_with_warning'
    assert route(assessment(.49,'escalate','high'))=='escalate'
def test_high_risk_overrides_approval():assert route(assessment(.95,'approve','high'))=='escalate'
