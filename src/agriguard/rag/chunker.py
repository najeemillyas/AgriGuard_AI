"""Create traceable chunks while preserving source identifiers."""

from dataclasses import dataclass
import hashlib
from .document_loader import SourceDocument

@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source_name: str
    title: str
    crop: str
    problem: str
    content: str

def chunk_document(doc: SourceDocument, max_words: int = 160, overlap: int = 25) -> list[Chunk]:
    words = doc.content.split()
    if not words:
        return []
    chunks=[]; step=max(1,max_words-overlap)
    for start in range(0,len(words),step):
        text=" ".join(words[start:start+max_words])
        digest=hashlib.sha1(f"{doc.path}:{start}".encode()).hexdigest()[:12]
        chunks.append(Chunk(digest,doc.source,doc.title,doc.crop.lower(),doc.problem.lower(),text))
        if start+max_words>=len(words): break
    return chunks
