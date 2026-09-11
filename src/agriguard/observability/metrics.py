"""Gold-dataset evaluation and metrics."""
import json
from pathlib import Path
from agriguard.models import CropCase, WeatherResult
from agriguard.settings import get_settings
from agriguard.orchestration.graph import AgriGuardWorkflow

def evaluate(cases:list[dict],workflow:AgriGuardWorkflow)->dict:
    rows=[]
    for item in cases:
        state=workflow.run(CropCase(**item['input']))
        actual={'category':state.classification.category,'decision':state.safety.decision,'has_evidence':bool(state.evidence),'tool_success':state.weather.spray_status!='unavailable','unsafe_treatment_exposed':False}
        checks={k:actual[k]==v for k,v in item['expected'].items() if k in actual}
        rows.append({'test_case_id':item['test_case_id'],'actual':actual,'checks':checks,'passed':all(checks.values())})
    n=len(rows) or 1
    metric=lambda key:round(sum(r['checks'].get(key,False) for r in rows if key in r['checks'])/max(1,sum(key in r['checks'] for r in rows))*100,1)
    tool_rate=round(sum(r['actual']['tool_success'] for r in rows)/n*100,1)
    return {'total':len(rows),'passed':sum(r['passed'] for r in rows),'failed':sum(not r['passed'] for r in rows),'classification_accuracy':metric('category'),'retrieval_success_rate':metric('has_evidence'),'safety_route_compliance':metric('decision'),'correct_escalation_rate':metric('decision'),'tool_success_rate':tool_rate,'unsupported_advice_count':sum(r['actual']['unsafe_treatment_exposed'] for r in rows),'failed_case_ids':[r['test_case_id'] for r in rows if not r['passed']],'results':rows}

def cli_evaluate():
    class EvaluationWeather:
        def get(self,location:str)->WeatherResult:
            return WeatherResult(location=location,temperature_c=25,rain_probability=10,wind_speed_kmph=5,humidity_percent=60,spray_status='suitable',reason='Deterministic evaluation weather fixture.')
    s=get_settings();cases=json.loads((s.root/'data/eval/gold_cases.json').read_text());result=evaluate(cases,AgriGuardWorkflow(s,EvaluationWeather()));out=s.generated_dir/'evaluation_results.json';out.write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))
