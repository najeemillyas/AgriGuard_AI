"""Load approved Markdown documents with YAML front matter."""

from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass(frozen=True)
class SourceDocument:
    path: Path
    title: str
    crop: str
    problem: str
    source: str
    version: str
    content: str

def load_document(path: Path) -> SourceDocument:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        raise ValueError(f"Missing YAML front matter: {path}")
    _, header, body = raw.split("---", 2)
    meta = yaml.safe_load(header) or {}
    required = ("title", "crop", "problem", "source", "version")
    missing = [key for key in required if not meta.get(key)]
    if missing:
        raise ValueError(f"Missing metadata {missing}: {path}")
    return SourceDocument(path, *(str(meta[k]) for k in required), body.strip())

def load_documents(root: Path) -> list[SourceDocument]:
    return [load_document(p) for p in sorted(root.rglob("*.md")) if p.name != "README.md"]
