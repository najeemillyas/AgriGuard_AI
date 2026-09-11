"""Requirement-driven system checks."""
from pathlib import Path
import json
def test_gold_dataset_has_minimum_scenarios():
    root=Path(__file__).resolve().parents[2];cases=json.loads((root/'data/eval/gold_cases.json').read_text())
    assert len(cases)>=10
    ids={x['test_case_id'] for x in cases}
    assert {'AGR-TC-001','AGR-TC-004','AGR-TC-034','AGR-TC-045'}.issubset(ids)
