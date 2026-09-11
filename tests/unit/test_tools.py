"""AGR-TC-019 through AGR-TC-023 and AGR-TC-038."""
import pytest
from agriguard.tools.knowledge_tool import search_crop_guidance
from agriguard.rag import SQLiteVectorStore
def test_knowledge_tool_validation(settings):
    with pytest.raises(ValueError):search_crop_guidance(SQLiteVectorStore(settings.database_path),'','spots')
def test_knowledge_tool_success(settings):
    assert search_crop_guidance(SQLiteVectorStore(settings.database_path),'chilli','thrips curl','flowering')
