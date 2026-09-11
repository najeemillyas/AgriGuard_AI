"""AGR-TC-013 through AGR-TC-018."""
from agriguard.rag import SQLiteVectorStore,Retriever
from agriguard.models import CropCase
def test_retrieval_is_ranked_and_traceable(settings):
    store=SQLiteVectorStore(settings.database_path);rows=store.query('chrysanthemum tiny insects flowers thrips',crop='chrysanthemum')
    assert rows and all(rows[i]['score']>=rows[i+1]['score'] for i in range(len(rows)-1))
    assert all(r['source_name'] and r['chunk_id'] for r in rows)
def test_retriever_returns_evidence(settings):
    case=CropCase(crop='tomato',stage='fruiting',location='X',symptoms='brown leaf spots with concentric rings',severity='medium')
    assert Retriever(SQLiteVectorStore(settings.database_path)).retrieve(case)
