"""AGR-TC-034 through AGR-TC-037."""
from agriguard.orchestration.graph import AgriGuardWorkflow
from agriguard.models import CropCase,WeatherResult
class Weather:
    def get(self,location):return WeatherResult(location=location,spray_status='suitable',reason='fixture')
def test_unsupported_crop_is_persisted_for_expert(settings):
    flow=AgriGuardWorkflow(settings,Weather());state=flow.run(CropCase(crop='rice',stage='vegetative',location='X',symptoms='tiny insects on leaves',severity='medium'))
    assert state.safety.decision=='escalate' and state.escalation_id
    record=flow.cases.get_escalation(state.escalation_id)
    assert record['case_id']==state.case.case_id and record['evidence'] is not None
