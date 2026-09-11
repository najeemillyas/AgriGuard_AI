"""Score grounding, diagnosis confidence, safety and overall confidence."""

from agriguard.models import CropCase, Classification, Evidence, WeatherResult, Advisory, SafetyAssessment
from agriguard.safety.confidence import clamp, overall
from agriguard.safety.guardrails import evidence_is_adequate, advisory_sources_valid
from agriguard.safety.red_flags import chemical_claim_risk

class SafetyCritic:
    def __init__(self,supported_crops:tuple[str,...]):self.supported={x.lower() for x in supported_crops}
    def review(self,case:CropCase,classification:Classification,evidence:list[Evidence],weather:WeatherResult,advisory:Advisory|None)->SafetyAssessment:
        grounding=clamp((max((e.score for e in evidence),default=0))*1.1 if advisory_sources_valid(advisory,evidence) else 0)
        diagnosis=0.35 if classification.category=='unclear' else 0.68
        if len(evidence)>=2:diagnosis+=.12
        if classification.missing_information:diagnosis-=.18
        diagnosis=clamp(diagnosis)
        safety=.95
        reasons=[]
        unsupported=case.crop.lower() not in self.supported
        no_evidence=not evidence_is_adequate(evidence)
        chemical=chemical_claim_risk(case.symptoms)
        if weather.spray_status=='unavailable':safety-=.12; reasons.append('Weather is unavailable.')
        if weather.spray_status=='unsuitable':safety-=.08; reasons.append('Immediate spraying is weather-unsafe.')
        if chemical:safety-=.35; reasons.append('Unverified chemical or dosage request.')
        if classification.prompt_injection_detected:safety-=.45; reasons.append('Prompt-injection attempt detected.')
        if no_evidence:safety-=.35; reasons.append('Adequate retrieved evidence is unavailable.')
        safety=clamp(safety); score=overall(grounding,diagnosis,safety)
        hard_red=bool(classification.red_flags) or unsupported or chemical or classification.prompt_injection_detected
        if unsupported:reasons.append('Crop is outside prototype scope.')
        if classification.red_flags:reasons.extend(classification.red_flags)
        if hard_red:decision='escalate';risk='high'
        elif no_evidence or score<.50:decision='escalate';risk='high'
        elif score<.70:decision='approve_with_warning';risk='medium'
        else:decision='approve';risk='low' if weather.spray_status=='suitable' else 'medium'
        return SafetyAssessment(grounding_score=grounding,diagnosis_confidence=diagnosis,safety_score=safety,overall_confidence=score,risk_level=risk,decision=decision,reason=' '.join(dict.fromkeys(reasons)) or 'Grounded evidence and configured safety checks passed.')
