"""High-risk crop and user-request red-flag detection."""

CHEMICAL_REQUESTS=('exact dose','dosage','mix with','banned chemical','guarantee','100% cure')

def chemical_claim_risk(text:str)->bool:
    value=text.lower()
    return any(term in value for term in CHEMICAL_REQUESTS)
