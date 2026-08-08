import logging
from app.llm.provider import llm_provider
from app.models.domain import CandidateTopic, EditorialDecision

logger = logging.getLogger("abtalks.editorial")

def evaluate_candidate(candidate: CandidateTopic, agent_name: str, agent_domain: str, recent_context: str) -> EditorialDecision:
    logger.info(f"[EDITORIAL] Evaluating candidate: {candidate.title}")
    
    system_prompt = f"""
You are the Editorial Engine for an autonomous AI persona.
Persona Name: {agent_name}
Domain: {agent_domain}

Decide whether to ACCEPT or REJECT a candidate topic.
Score the topic from 0.0 to 1.0 based on Relevance, Novelty, Quality, and Timeliness.
A score > 0.75 is an ACCEPT. Otherwise REJECT.
Reject if it is substantially similar to recent context.

Schema (JSON keys):
"decision": string (ACCEPT or REJECT)
"score": float
"reason": string
"""

    user_prompt = f"""
CANDIDATE TOPIC:
Title: {candidate.title}
Source Name: {candidate.source_name}
Source URL: {candidate.source_url}
Snippet: {candidate.content_snippet}

RECENT CONTEXT:
{recent_context}
"""
    try:
        decision = llm_provider.generate_structured(system_prompt, user_prompt, EditorialDecision)
        if decision.decision not in ["ACCEPT", "REJECT"]:
            decision.decision = "REJECT"
            
        logger.info(f"[EDITORIAL] Score: {decision.score} | Decision: {decision.decision}")
        if decision.decision == "REJECT":
            logger.info(f"[EDITORIAL] Reason: {decision.reason}")
        return decision
        
    except Exception as e:
        logger.error(f"[EDITORIAL] Error evaluating candidate: {e}")
        return EditorialDecision(decision="REJECT", score=0.0, reason=f"Error: {e}")
