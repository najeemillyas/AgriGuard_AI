"""JSON Lines trace persistence."""
from pathlib import Path
from agriguard.models import TraceEvent

class TraceRepository:
    def __init__(self,path:Path):self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True)
    def append(self,events:list[TraceEvent]):
        with self.path.open('a',encoding='utf-8') as f:
            for event in events:f.write(event.model_dump_json()+'\n')
