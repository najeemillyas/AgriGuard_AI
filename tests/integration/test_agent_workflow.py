"""AGR-TC-001 through AGR-TC-003 and AGR-TC-024 through AGR-TC-027."""
from agriguard.orchestration.graph import AgriGuardWorkflow
from agriguard.models import CropCase,WeatherResult
class Weather:
    def get(self,location):return WeatherResult(location=location,temperature_c=25,rain_probability=10,wind_speed_kmph=5,spray_status='suitable',reason='Controlled safe weather.')
def test_complete_workflow(settings):
    state=AgriGuardWorkflow(settings,Weather()).run(CropCase(crop='chrysanthemum',stage='flowering',location='Bagepally',symptoms='tiny insects inside flowers and damaged petals',severity='medium'))
    names=[e.component for e in state.trace]
    assert names[:5]==['Intake Agent','Retrieval Agent','Weather Tool','Advisory Agent','Safety Critic']
    assert state.evidence and state.advisory and state.safety
    assert state.advisory.source_names
