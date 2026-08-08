import logging
import uuid
import json
from datetime import datetime, timezone
from app.llm.provider import llm_provider
from app.models.domain import CandidateTopic, GeneratedPost
from app.db.database import get_connection

logger = logging.getLogger("abtalks.publisher")

def generate_and_publish_post(candidate: CandidateTopic, agent_id: str, agent_name: str, agent_domain: str):
    logger.info(f"[GENERATION] Generating post for: {candidate.title}")
    
    system_prompt = f"""
You are the Writer Engine for an autonomous AI persona.
Persona Name: {agent_name}
Domain: {agent_domain}

Write a high-quality, concise social post about a news topic. Write with a clear point of view.
Provide a rationale explaining why this was selected.

Schema (JSON keys):
"text": string
"rationale": string
"sources": list of strings
"""

    user_prompt = f"""
TOPIC TO WRITE ABOUT:
Title: {candidate.title}
Source URL: {candidate.source_url}
Snippet: {candidate.content_snippet}
"""
    
    generated = llm_provider.generate_structured(system_prompt, user_prompt, GeneratedPost)
    
    logger.info("[VALIDATION] Validating generated post...")
    if not generated.text or len(generated.text) < 10:
        raise ValueError("Generated text is empty or too short.")
        
    if candidate.source_url not in generated.sources:
        generated.sources.append(candidate.source_url)
        
    logger.info("[VALIDATION] Post validated successfully.")
    
    post_id = f"post-{uuid.uuid4().hex[:8]}"
    created_at = datetime.now(timezone.utc).isoformat()
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO posts (id, agent_id, created_at, text, rationale, sources) VALUES (?, ?, ?, ?, ?, ?)",
        (post_id, agent_id, created_at, generated.text, generated.rationale, json.dumps(generated.sources))
    )
    conn.commit()
    conn.close()
    
    logger.info(f"[PUBLISH] Post {post_id} published.")
    return post_id
