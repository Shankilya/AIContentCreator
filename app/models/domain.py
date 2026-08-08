from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class PersonaConfig:
    name: str
    domain: str

@dataclass
class CandidateTopic:
    title: str
    content_snippet: str
    source_url: str
    source_name: str
    published_at: Optional[datetime] = None
    fingerprint: Optional[str] = None

@dataclass
class EditorialDecision:
    decision: str
    score: float
    reason: str

@dataclass
class GeneratedPost:
    text: str
    rationale: str
    sources: List[str]
