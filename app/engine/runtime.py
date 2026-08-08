import asyncio
import logging
from typing import Dict

from app.core.config import settings
from app.db.database import get_connection
from app.engine.discovery import discover_candidates
from app.engine.memory import memory_engine
from app.engine.editorial import evaluate_candidate
from app.engine.publisher import generate_and_publish_post
from app.models.domain import EditorialDecision

logger = logging.getLogger("abtalks.runtime")

active_workers: Dict[str, asyncio.Task] = {}

async def agent_loop(agent_id: str):
    logger.info(f"[RUNTIME] Starting autonomous worker for agent {agent_id}")
    await asyncio.sleep(2)
    
    try:
        while True:
            logger.info(f"[RUNTIME] Agent {agent_id} waking up for cycle")
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name, domain, status FROM agents WHERE id = ?", (agent_id,))
            agent_row = cursor.fetchone()
            conn.close()
            
            if not agent_row or agent_row['status'] != 'ACTIVE':
                logger.warning(f"[RUNTIME] Agent {agent_id} is inactive or missing. Stopping loop.")
                break
                
            try:
                candidates = discover_candidates()
                published_in_cycle = False
                
                for candidate in candidates:
                    if published_in_cycle:
                        break
                        
                    try:
                        if memory_engine.is_duplicate(candidate, agent_id):
                            decision = EditorialDecision(decision="REJECT", score=0.0, reason="Duplicate topic or source")
                            memory_engine.record_candidate(agent_id, candidate, decision)
                            continue
                            
                        recent_context = memory_engine.get_recent_context(agent_id)
                        
                        decision = evaluate_candidate(candidate, agent_row['name'], agent_row['domain'], recent_context)
                        memory_engine.record_candidate(agent_id, candidate, decision)
                        
                        if decision.decision == "ACCEPT":
                            generate_and_publish_post(candidate, agent_id, agent_row['name'], agent_row['domain'])
                            published_in_cycle = True
                            
                    except Exception as loop_e:
                        logger.error(f"[RUNTIME] Error processing candidate {candidate.title}: {loop_e}")
                        continue
                        
            except Exception as e:
                logger.error(f"[RUNTIME] Fatal error in cycle for agent {agent_id}: {e}")
                
            interval_sec = settings.DISCOVERY_INTERVAL_MINUTES * 60
            logger.info(f"[RUNTIME] Cycle complete. Next cycle in {interval_sec} seconds.")
            await asyncio.sleep(interval_sec)
            
    except asyncio.CancelledError:
        logger.info(f"[RUNTIME] Worker for agent {agent_id} was cancelled")
    except Exception as e:
        logger.error(f"[RUNTIME] Worker for agent {agent_id} encountered fatal outer error: {e}")

def start_agent_worker(agent_id: str):
    if agent_id in active_workers and not active_workers[agent_id].done():
        logger.warning(f"[RUNTIME] Worker for agent {agent_id} is already running.")
        return
        
    task = asyncio.create_task(agent_loop(agent_id))
    active_workers[agent_id] = task
    logger.info(f"[RUNTIME] Task created for agent {agent_id}")
