from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import logging
from typing import List

from app.models.domain import InitRequest, InitResponse, FeedResponse, PostResponse
from app.db.database import get_db
from app.db.models import Agent, Post
from app.engine.runtime import start_agent_worker

logger = logging.getLogger("abtalks.api")
router = APIRouter(prefix="/api/agent")

@router.post("/init", response_model=InitResponse)
def init_agent(req: InitRequest, db: Session = Depends(get_db)):
    """Initialize a new autonomous agent and start its worker."""
    agent_id = f"agt-{uuid.uuid4().hex[:8]}"
    
    # Persist the agent in the database
    db_agent = Agent(
        id=agent_id,
        name=req.persona.name,
        domain=req.persona.domain,
        status="ACTIVE"
    )
    db.add(db_agent)
    db.commit()
    
    logger.info(f"[AGENT] Agent {agent_id} initialized: {req.persona.name} ({req.persona.domain})")
    
    # Start the autonomous background worker
    start_agent_worker(agent_id)
    
    return InitResponse(agentId=agent_id)

@router.get("/feed", response_model=FeedResponse)
def get_feed(agentId: str, db: Session = Depends(get_db)):
    """Retrieve the feed for a given agent. Strictly a read endpoint."""
    # Verify agent exists
    agent = db.query(Agent).filter(Agent.id == agentId).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    # Get posts, newest first
    posts = db.query(Post).filter(Post.agent_id == agentId).order_by(Post.created_at.desc()).all()
    
    response_posts = []
    for p in posts:
        # Convert created_at to proper datetime response
        response_posts.append(PostResponse(
            id=p.id,
            createdAt=p.created_at,
            text=p.text,
            rationale=p.rationale,
            sources=p.sources if p.sources else []
        ))
        
    return FeedResponse(posts=response_posts)
