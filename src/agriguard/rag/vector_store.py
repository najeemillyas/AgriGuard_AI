"""Persistent SQLite vector store with traceable metadata."""

from __future__ import annotations
import json, sqlite3
from pathlib import Path
from .embeddings import embed, cosine
from .document_loader import load_documents
from .chunker import chunk_document, Chunk

class SQLiteVectorStore:
    def __init__(self, path: Path):
        self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
        self._init()
    def connect(self): return sqlite3.connect(self.path)
    def _init(self):
        with self.connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS chunks (
              chunk_id TEXT PRIMARY KEY, source_name TEXT, title TEXT, crop TEXT,
              problem TEXT, content TEXT, vector TEXT)""")
    def replace_all(self, chunks: list[Chunk]) -> int:
        with self.connect() as db:
            db.execute("DELETE FROM chunks")
            db.executemany("INSERT INTO chunks VALUES (?,?,?,?,?,?,?)",[(c.chunk_id,c.source_name,c.title,c.crop,c.problem,c.content,json.dumps(embed(c.content))) for c in chunks])
        return len(chunks)
    def query(self,text: str,crop: str|None=None,limit: int=5) -> list[dict]:
        q=embed(text); sql="SELECT chunk_id,source_name,title,crop,problem,content,vector FROM chunks"; args=[]
        if crop and crop.lower() not in ("other","unsupported"):
            sql+=" WHERE crop IN (?, 'all')"; args=[crop.lower()]
        with self.connect() as db: rows=db.execute(sql,args).fetchall()
        out=[]
        for row in rows:
            raw=max(-1.0,min(1.0,cosine(q,json.loads(row[6]))))
            score=(raw+1)/2
            keyword_bonus=0.08 if row[4].replace('_',' ') in text.lower() else 0
            out.append(dict(zip(('chunk_id','source_name','title','crop','problem','content'),row[:6]))|{'score':min(1.0,score+keyword_bonus)})
        return sorted(out,key=lambda x:x['score'],reverse=True)[:limit]
    def count(self) -> int:
        with self.connect() as db:return db.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]

def ingest(knowledge_dir: Path,database_path: Path) -> dict:
    docs=load_documents(knowledge_dir); chunks=[c for d in docs for c in chunk_document(d)]
    count=SQLiteVectorStore(database_path).replace_all(chunks)
    return {'documents':len(docs),'chunks':count,'database':str(database_path)}

def cli_ingest():
    from agriguard.settings import get_settings
    s=get_settings(); print(json.dumps(ingest(s.knowledge_dir,s.database_path),indent=2))
