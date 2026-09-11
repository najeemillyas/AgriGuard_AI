"""AGR-TC-041 and AGR-TC-043 secret-handling tests."""
from pathlib import Path
import re
def test_no_plaintext_key_in_repository():
    root=Path(__file__).resolve().parents[2];pattern=re.compile(r'sk-(?:proj-)?[A-Za-z0-9_-]{20,}')
    bad=[]
    for p in root.rglob('*'):
        if not p.is_file() or any(x in p.parts for x in ('.git','.venv','__pycache__')) or p.name in ('.env','.env.local'):continue
        try:
            if pattern.search(p.read_text(encoding='utf-8')):bad.append(p)
        except (UnicodeDecodeError,OSError):pass
    assert not bad
