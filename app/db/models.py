from sqlalchemy import Column, String, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    status = Column(String, default="ACTIVE") # ACTIVE, INACTIVE
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    posts = relationship("Post", back_populates="agent")
    history = relationship("CandidateHistory", back_populates="agent")

class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    text = Column(String, nullable=False)
    rationale = Column(String, nullable=False)
    sources = Column(JSON, nullable=False) # List of strings

    agent = relationship("Agent", back_populates="posts")

class CandidateHistory(Base):
    __tablename__ = "candidate_history"
    
    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Topic details
    title = Column(String, nullable=False)
    source_url = Column(String, nullable=False)
    fingerprint = Column(String, nullable=True)
    
    # Decision details
    decision = Column(String, nullable=False) # ACCEPT or REJECT
    score = Column(Float, nullable=True)
    reason = Column(String, nullable=True)

    agent = relationship("Agent", back_populates="history")
