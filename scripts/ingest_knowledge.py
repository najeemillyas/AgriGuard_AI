"""Command-line entry point for knowledge ingestion."""
from agriguard.settings import get_settings
from agriguard.rag.vector_store import ingest
import json
if __name__=='__main__':
    s=get_settings();print(json.dumps(ingest(s.knowledge_dir,s.database_path),indent=2))
