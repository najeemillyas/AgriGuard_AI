"""Structured knowledge-search tool."""
from agriguard.rag import SQLiteVectorStore

def search_crop_guidance(store:SQLiteVectorStore,crop:str,symptoms:str,stage:str='',limit:int=5)->list[dict]:
    if not crop.strip() or not symptoms.strip():raise ValueError('crop and symptoms are required')
    return store.query(f'{crop} {stage} {symptoms}',crop=crop,limit=limit)
