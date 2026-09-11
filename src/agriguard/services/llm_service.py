"""OpenAI Responses API boundary with a controlled offline fallback."""

from __future__ import annotations
import json, os

class LLMService:
    def __init__(self,model:str): self.model=model; self.enabled=bool(os.getenv('OPENAI_API_KEY'))
    def generate_json(self,instructions:str,input_data:dict)->dict|None:
        if not self.enabled:return None
        try:
            from openai import OpenAI
            client=OpenAI()
            response=client.responses.create(
                model=self.model,
                instructions=instructions,
                input=json.dumps(input_data,ensure_ascii=False),
            )
            text=response.output_text.strip()
            if text.startswith('```'): text=text.split('\n',1)[1].rsplit('```',1)[0]
            return json.loads(text)
        except Exception:
            # The deterministic grounded draft keeps the application available
            # if the model, account, network or JSON response is unavailable.
            return None
