"""Deterministic local hashing embeddings for offline vector retrieval."""

import hashlib, math, re

DIMENSIONS=384

def embed(text: str) -> list[float]:
    vector=[0.0]*DIMENSIONS
    for token in re.findall(r"[a-z0-9]+", text.lower()):
        raw=hashlib.blake2b(token.encode(),digest_size=8).digest()
        idx=int.from_bytes(raw[:4],"big")%DIMENSIONS
        sign=1.0 if raw[4]%2==0 else -1.0
        vector[idx]+=sign
    norm=math.sqrt(sum(v*v for v in vector)) or 1.0
    return [v/norm for v in vector]

def cosine(a: list[float], b: list[float]) -> float:
    return sum(x*y for x,y in zip(a,b))
