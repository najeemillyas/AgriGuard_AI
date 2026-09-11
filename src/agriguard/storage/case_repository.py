"""SQLite persistence for cases and escalation records."""
import json,sqlite3
from pathlib import Path
from agriguard.models import EscalationRecord

class CaseRepository:
    def __init__(self,path:Path):self.path=Path(path);self._init()
    def _connect(self):return sqlite3.connect(self.path)
    def _init(self):
        with self._connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS cases (case_id TEXT PRIMARY KEY, payload TEXT NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS escalations (escalation_id TEXT PRIMARY KEY, case_id TEXT, payload TEXT NOT NULL)')
    def save_case(self,case_id:str,payload:dict):
        with self._connect() as db:db.execute('INSERT OR REPLACE INTO cases VALUES (?,?)',(case_id,json.dumps(payload,default=str)))
    def save_escalation(self,record:EscalationRecord):
        with self._connect() as db:db.execute('INSERT OR REPLACE INTO escalations VALUES (?,?,?)',(record.escalation_id,record.case_id,record.model_dump_json()))
    def get_escalation(self,escalation_id:str)->dict|None:
        with self._connect() as db:row=db.execute('SELECT payload FROM escalations WHERE escalation_id=?',(escalation_id,)).fetchone()
        return json.loads(row[0]) if row else None
