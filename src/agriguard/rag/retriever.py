"""Crop, stage and symptom-aware evidence retrieval."""

from agriguard.models import CropCase, Evidence
from .vector_store import SQLiteVectorStore

class Retriever:
    def __init__(self,store:SQLiteVectorStore,minimum_score:float=0.50): self.store=store; self.minimum_score=minimum_score
    def retrieve(self,case:CropCase,limit:int=5)->list[Evidence]:
        query=f"{case.crop} {case.stage} {case.symptoms} severity {case.severity}"
        rows=self.store.query(query,crop=case.crop,limit=limit)
        return [Evidence(**r) for r in rows if r['score']>=self.minimum_score]
