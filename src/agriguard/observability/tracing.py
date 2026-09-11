"""Structured agent, tool, retrieval and routing traces."""
from time import perf_counter
from agriguard.models import TraceEvent

class TraceRecorder:
    def __init__(self,case_id:str):self.case_id=case_id;self.events=[]
    def add(self,component:str,action:str,outcome:str,reason:str='',duration_ms:float=0,details:dict|None=None):
        event=TraceEvent(case_id=self.case_id,component=component,action=action,outcome=outcome,reason=reason,duration_ms=round(duration_ms,2),details=details or {})
        self.events.append(event);return event
    def timed(self,component,action):return _Timer(self,component,action)

class _Timer:
    def __init__(self,recorder,component,action):self.r=recorder;self.c=component;self.a=action
    def __enter__(self):self.start=perf_counter();return self
    def __exit__(self,typ,val,tb):self.duration=(perf_counter()-self.start)*1000
