"""Grounding, unsupported-claim and chemical-safety guardrails."""

from agriguard.models import Advisory, Evidence

def evidence_is_adequate(evidence:list[Evidence],minimum:float=.50)->bool:
    return bool(evidence) and max(x.score for x in evidence)>=minimum

def advisory_sources_valid(advisory:Advisory|None,evidence:list[Evidence])->bool:
    if advisory is None:return False
    known={e.source_name for e in evidence}
    return bool(advisory.source_names) and set(advisory.source_names).issubset(known)
