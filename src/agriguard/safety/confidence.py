"""Confidence score validation and threshold policy."""

def clamp(value:float)->float:return round(max(0.0,min(1.0,value)),2)

def overall(grounding:float,diagnosis:float,safety:float)->float:
    return clamp(grounding*.40+diagnosis*.30+safety*.30)
