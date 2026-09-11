"""Explicit multi-agent workflow with deterministic safety routing."""
from agriguard.models import CropCase
from agriguard.agents import IntakeAgent,RetrievalAgent,AdvisoryAgent,SafetyCritic
from agriguard.services import WeatherService,LLMService
from agriguard.rag import SQLiteVectorStore,Retriever,ingest
from agriguard.settings import Settings
from agriguard.observability.tracing import TraceRecorder
from agriguard.storage.case_repository import CaseRepository
from agriguard.storage.trace_repository import TraceRepository
from agriguard.tools.escalation_tool import create_expert_escalation
from .state import WorkflowState
from .router import route

class AgriGuardWorkflow:
    def __init__(self,settings:Settings,weather_service:WeatherService|None=None):
        self.settings=settings;self.store=SQLiteVectorStore(settings.database_path)
        if self.store.count()==0:ingest(settings.knowledge_dir,settings.database_path)
        self.intake=IntakeAgent();self.retrieval=RetrievalAgent(Retriever(self.store));self.weather=weather_service or WeatherService()
        self.advisory=AdvisoryAgent(LLMService(settings.model));self.critic=SafetyCritic(settings.supported_crops)
        self.cases=CaseRepository(settings.database_path);self.traces=TraceRepository(settings.generated_dir/'traces.jsonl')
    def run(self,case:CropCase)->WorkflowState:
        s=WorkflowState(case=case);tr=TraceRecorder(case.case_id)
        with tr.timed('Intake Agent','classify') as t:s.classification=self.intake.classify(case)
        tr.add('Intake Agent','classify','completed',s.classification.rationale,t.duration,{'category':s.classification.category,'red_flags':s.classification.red_flags})
        with tr.timed('Retrieval Agent','retrieve') as t:s.evidence=self.retrieval.run(case)
        tr.add('Retrieval Agent','retrieve','completed',f'{len(s.evidence)} chunks retrieved',t.duration,{'sources':[e.source_name for e in s.evidence]})
        with tr.timed('Weather Tool','lookup') as t:s.weather=self.weather.get(case.location)
        tr.add('Weather Tool','lookup',s.weather.spray_status,s.weather.reason,t.duration)
        with tr.timed('Advisory Agent','draft') as t:s.advisory=self.advisory.draft(case,s.classification,s.evidence,s.weather)
        tr.add('Advisory Agent','draft','completed' if s.advisory else 'withheld','Grounded draft created.' if s.advisory else 'No adequate evidence.',t.duration)
        with tr.timed('Safety Critic','review') as t:s.safety=self.critic.review(case,s.classification,s.evidence,s.weather,s.advisory)
        decision=route(s.safety);s.safety.decision=decision
        tr.add('Safety Critic','review',decision,s.safety.reason,t.duration,{'confidence':s.safety.overall_confidence,'risk':s.safety.risk_level})
        if decision=='escalate':
            s.escalation_id=create_expert_escalation(s,self.cases);tr.add('Escalation Tool','create','completed',s.safety.reason,details={'escalation_id':s.escalation_id})
        s.trace=tr.events
        self.cases.save_case(case.case_id,{'case':case.model_dump(mode='json'),'classification':s.classification.model_dump(),'evidence':[e.model_dump() for e in s.evidence],'weather':s.weather.model_dump(),'advisory':s.advisory.model_dump() if s.advisory else None,'safety':s.safety.model_dump(),'escalation_id':s.escalation_id})
        self.traces.append(s.trace);return s
