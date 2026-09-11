"""Typed non-secret settings and environment loading boundary."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import yaml

ROOT = Path(__file__).resolve().parents[2]

def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

@dataclass(frozen=True)
class Settings:
    root: Path
    knowledge_dir: Path
    generated_dir: Path
    database_path: Path
    model: str
    api_key_available: bool
    approve_minimum: float
    warning_minimum: float
    supported_crops: tuple[str, ...]
    supported_categories: tuple[str, ...]

def get_settings(root: Path | None = None) -> Settings:
    project_root = (root or ROOT).resolve()
    _load_env_file(project_root / ".env.local")
    app = yaml.safe_load((project_root / "config/app.yaml").read_text(encoding="utf-8"))
    safety = yaml.safe_load((project_root / "config/safety.yaml").read_text(encoding="utf-8"))
    generated = project_root / "data/generated"
    generated.mkdir(parents=True, exist_ok=True)
    return Settings(
        root=project_root,
        knowledge_dir=project_root / "data/knowledge",
        generated_dir=generated,
        database_path=generated / "agriguard.sqlite3",
        model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        api_key_available=bool(os.getenv("OPENAI_API_KEY")),
        approve_minimum=float(safety["confidence"]["approve_minimum"]),
        warning_minimum=float(safety["confidence"]["warning_minimum"]),
        supported_crops=tuple(app["application"]["supported_crops"]),
        supported_categories=tuple(app["application"]["supported_categories"]),
    )
