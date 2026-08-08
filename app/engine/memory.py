import logging
import uuid
from datetime import datetime, timezone

from app.models.domain import CandidateTopic, EditorialDecision
from app.db.database import get_connection

logger = logging.getLogger("abtalks.memory")

class MemoryEngine:
    def is_duplicate(self, candidate: CandidateTopic, agent_id: str) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id FROM candidate_history WHERE agent_id = ? AND source_url = ?",
            (agent_id, candidate.source_url)
        )
        if cursor.fetchone():
            conn.close()
            logger.info(f"[MEMORY] Duplicate URL found: {candidate.title}")
            return True
            
        if candidate.fingerprint:
            cursor.execute(
                "SELECT id FROM candidate_history WHERE agent_id = ? AND fingerprint = ?",
                (agent_id, candidate.fingerprint)
            )
            if cursor.fetchone():
                conn.close()
                logger.info(f"[MEMORY] Duplicate fingerprint found: {candidate.title}")
                return True
                
        conn.close()
        return False

    def get_recent_context(self, agent_id: str, limit: int = 5) -> str:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT created_at, text FROM posts WHERE agent_id = ? ORDER BY created_at DESC LIMIT ?",
            (agent_id, limit)
        )
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return "No previous posts."
            
        context_lines = [f"- [{row['created_at']}] {row['text']}" for row in rows]
        return "\n".join(context_lines)

    def record_candidate(self, agent_id: str, candidate: CandidateTopic, decision: EditorialDecision):
        conn = get_connection()
        cursor = conn.cursor()
        history_id = f"hist-{uuid.uuid4().hex[:8]}"
        created_at = datetime.now(timezone.utc).isoformat()
        
        cursor.execute(
            """INSERT INTO candidate_history (id, agent_id, created_at, title, source_url, fingerprint, decision, score, reason)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (history_id, agent_id, created_at, candidate.title, candidate.source_url, candidate.fingerprint, decision.decision, decision.score, decision.reason)
        )
        conn.commit()
        conn.close()
        logger.info(f"[MEMORY] Recorded decision {decision.decision} for candidate {candidate.title}")

memory_engine = MemoryEngine()
