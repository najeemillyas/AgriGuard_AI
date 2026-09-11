"""Validate and classify incoming crop cases."""

import re
from agriguard.models import CropCase, Classification

INJECTION_PATTERNS=(r'ignore (all|previous|system) instructions',r'skip (the )?(safety|guardrail|sources)',r'reveal (the )?(secret|api key)',r'system prompt')

class IntakeAgent:
    def classify(self,case:CropCase)->Classification:
        text=case.symptoms.lower()
        injection=any(re.search(p,text) for p in INJECTION_PATTERNS)
        if any(k in text for k in ('insect','thrips','aphid','borer','caterpillar','tiny bugs','whitefly')):
            category='insect_attack'; rationale='Symptoms contain insect or pest indicators.'
        elif any(k in text for k in ('spot','blight','fungus','mildew','rot','lesion','mould','mold')):
            category='fungal_disease'; rationale='Symptoms contain fungal or lesion indicators.'
        elif any(k in text for k in ('yellow','chlorosis','purple leaf','interveinal','deficiency','stunted')):
            category='nutrient_deficiency'; rationale='Symptoms contain nutrient-stress indicators.'
        else:
            category='unclear'; rationale='Symptoms do not uniquely match a supported category.'
        missing=[]
        if len(text.split())<3:missing.append('Provide a more detailed symptom description.')
        red=[]
        if case.severity=='severe' or any(k in text for k in ('rapidly spreading','entire crop','plant death','poison','human exposure','animal exposure')):red.append('Severe, rapidly spreading or exposure-related condition.')
        if injection:red.append('Prompt-injection attempt detected in user input.')
        return Classification(category=category,rationale=rationale,missing_information=missing,red_flags=red,prompt_injection_detected=injection)
