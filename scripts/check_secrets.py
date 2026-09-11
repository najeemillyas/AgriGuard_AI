"""Repository secret-safety check used before submission."""
from pathlib import Path
import re,sys
root=Path(__file__).resolve().parents[1];pattern=re.compile(r'sk-(?:proj-)?[A-Za-z0-9_-]{20,}')
bad=[]
for path in root.rglob('*'):
    if not path.is_file() or any(x in path.parts for x in ('.git','.venv','__pycache__')) or path.name in ('.env','.env.local'):continue
    try:
        if pattern.search(path.read_text(encoding='utf-8')):bad.append(str(path.relative_to(root)))
    except (UnicodeDecodeError,OSError):pass
print('Secret scan passed.' if not bad else 'Potential secrets: '+', '.join(bad));sys.exit(bool(bad))
