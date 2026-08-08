import os
import pytest
import sqlite3
from starlette.testclient import TestClient

# Must override DB path before importing app
os.environ["DATABASE_URL"] = "test.db"

from app.main import app
from app.db.database import init_db, get_connection

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    yield
    if os.path.exists("test.db"):
        try:
            os.remove("test.db")
        except PermissionError:
            pass # Keep it simple for Windows

client = TestClient(app)

def test_init_agent():
    response = client.post("/api/agent/init", json={
        "persona": {
            "name": "TestAda",
            "domain": "AI Testing"
        }
    })
    assert response.status_code == 200
    data = response.json()
    assert "agentId" in data
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agents WHERE id = ?", (data["agentId"],))
    agent = cursor.fetchone()
    conn.close()
    
    assert agent is not None
    assert agent["name"] == "TestAda"
    assert agent["status"] == "ACTIVE"

def test_feed_empty():
    response = client.get("/api/agent/feed?agentId=nonexistent")
    assert response.status_code == 404
    
    init_res = client.post("/api/agent/init", json={"persona": {"name": "A", "domain": "B"}})
    agent_id = init_res.json()["agentId"]
    
    feed_res = client.get(f"/api/agent/feed?agentId={agent_id}")
    assert feed_res.status_code == 200
    assert len(feed_res.json()["posts"]) == 0
