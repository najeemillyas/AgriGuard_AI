"""Shared deterministic fixtures."""
from pathlib import Path
import sys,tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import pytest
from agriguard.settings import get_settings
from agriguard.rag.vector_store import ingest

@pytest.fixture
def settings(tmp_path,monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY',raising=False)
    source=Path(__file__).resolve().parents[1]
    s=get_settings(source)
    object.__setattr__(s,'database_path',tmp_path/'test.sqlite3')
    object.__setattr__(s,'generated_dir',tmp_path)
    ingest(s.knowledge_dir,s.database_path)
    return s
