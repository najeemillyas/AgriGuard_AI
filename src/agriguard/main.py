"""Application composition root and command-line smoke run."""
from .settings import get_settings
from .models import CropCase
from .orchestration.graph import AgriGuardWorkflow

def main()->None:
    state=AgriGuardWorkflow(get_settings()).run(CropCase(crop='chrysanthemum',stage='flowering',location='Bagepally',symptoms='tiny insects inside flowers and damaged petals',severity='medium'))
    print(state.safety.model_dump_json(indent=2));print('Sources:',', '.join(x.source_name for x in state.evidence));print('Escalation:',state.escalation_id or 'not required')
if __name__=='__main__':main()
