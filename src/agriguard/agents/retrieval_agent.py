"""Request grounded evidence for the structured crop case."""
from agriguard.models import CropCase, Evidence
from agriguard.rag import Retriever

class RetrievalAgent:
    def __init__(self,retriever:Retriever):self.retriever=retriever
    def run(self,case:CropCase)->list[Evidence]:return self.retriever.retrieve(case)
