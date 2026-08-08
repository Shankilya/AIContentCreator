import json
import logging
import re
import httpx
from typing import TypeVar, Type, Any
from app.core.config import settings
from app.models.domain import EditorialDecision, GeneratedPost

logger = logging.getLogger("abtalks.llm")

class LLMProvider:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model = settings.LLM_MODEL
        logger.info(f"[LLM] Initialized provider: {self.provider}, model: {self.model}")

    def _extract_json(self, text: str) -> str:
        match = re.search(r'```(?:json)?(.*?)```', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            return text[start:end+1]
        return text

    def generate_structured(self, system_prompt: str, user_prompt: str, schema_cls: Type[Any]) -> Any:
        if self.provider == "mock":
            return self._mock_generate(schema_cls)
            
        full_system_prompt = f"""
{system_prompt}

You must respond ONLY with valid JSON. Do not include markdown formatting, just the raw JSON object.
"""
        full_user_prompt = f"""
--- START UNTRUSTED EXTERNAL DATA ---
{user_prompt}
--- END UNTRUSTED EXTERNAL DATA ---

Analyze the untrusted external data above. Respond ONLY with JSON.
"""
        try:
            with httpx.Client() as client:
                response = client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://abtalks.local",
                        "X-Title": "ABTalks Autonomous AI Creator"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": full_system_prompt},
                            {"role": "user", "content": full_user_prompt}
                        ],
                        "temperature": 0.2
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
                
            json_str = self._extract_json(content)
            parsed_data = json.loads(json_str)
            
            # Simple instantiation since it's a dataclass
            return schema_cls(**parsed_data)
            
        except Exception as e:
            logger.error(f"[LLM] Error generating structured output: {e}")
            raise ValueError(f"Failed to generate structured output: {e}")

    def _mock_generate(self, schema_cls: Type[Any]) -> Any:
        logger.info(f"[LLM] Using mock generation for {schema_cls.__name__}")
        if schema_cls.__name__ == "EditorialDecision":
            return schema_cls(decision="ACCEPT", score=0.9, reason="Mock accept")
        elif schema_cls.__name__ == "GeneratedPost":
            return schema_cls(
                text="This is a mock generated post.",
                rationale="Mock rationale.",
                sources=["https://example.com"]
            )
        raise NotImplementedError(f"Mock not implemented")

llm_provider = LLMProvider()
