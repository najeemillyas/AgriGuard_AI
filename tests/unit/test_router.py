"""AGR-TC-026 through AGR-TC-033."""
from agriguard.models import CropCase,WeatherResult
from agriguard.agents import IntakeAgent,SafetyCritic
def test_red_flag_forces_escalation():
    case=CropCase(crop='tomato',stage='fruiting',location='X',symptoms='rapidly spreading insect damage',severity='severe')
    c=IntakeAgent().classify(case);w=WeatherResult(location='X',spray_status='suitable',reason='fixture')
    result=SafetyCritic(('tomato',)).review(case,c,[],w,None)
    assert result.decision=='escalate' and result.risk_level=='high'
