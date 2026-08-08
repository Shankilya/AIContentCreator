import os
import pytest

os.environ["DATABASE_URL"] = "test_memory.db"

from app.db.database import init_db, get_connection
from app.engine.memory import memory_engine
from app.models.domain import CandidateTopic, EditorialDecision

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    yield
    if os.path.exists("test_memory.db"):
        try:
            os.remove("test_memory.db")
        except:
            pass

def test_duplicate_detection():
    agent_id = "test-agent"
    conn = get_connection()
    conn.execute("INSERT INTO agents (id, name, domain, status, created_at) VALUES (?, ?, ?, ?, ?)", 
                 (agent_id, "Test", "Test", "ACTIVE", "2024-01-01T00:00:00Z"))
    conn.commit()
    conn.close()

    candidate = CandidateTopic(
        title="Test News",
        content_snippet="Content",
        source_url="https://example.com/1",
        source_name="Example",
        fingerprint="testnews"
    )
    
    assert not memory_engine.is_duplicate(candidate, agent_id)
    
    decision = EditorialDecision(decision="ACCEPT", score=0.9, reason="Good")
    memory_engine.record_candidate(agent_id, candidate, decision)
    
    assert memory_engine.is_duplicate(candidate, agent_id)
    
    candidate_diff_url = CandidateTopic(
        title="Test News",
        content_snippet="Content",
        source_url="https://example.com/2",
        source_name="Example",
        fingerprint="testnews"
    )
    assert memory_engine.is_duplicate(candidate_diff_url, agent_id)
