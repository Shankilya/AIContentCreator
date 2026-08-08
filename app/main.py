import uuid
import json
import logging
from datetime import datetime, timezone

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from app.db.database import init_db, get_connection
from app.engine.runtime import start_agent_worker

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("abtalks.main")

async def init_agent(request):
    try:
        data = await request.json()
        persona = data.get("persona", {})
        name = persona.get("name")
        domain = persona.get("domain")
        
        if not name or not domain:
            return JSONResponse({"error": "Persona name and domain required"}, status_code=400)
            
        agent_id = f"agt-{uuid.uuid4().hex[:8]}"
        created_at = datetime.now(timezone.utc).isoformat()
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO agents (id, name, domain, status, created_at) VALUES (?, ?, ?, 'ACTIVE', ?)",
            (agent_id, name, domain, created_at)
        )
        conn.commit()
        conn.close()
        
        logger.info(f"[AGENT] Agent {agent_id} initialized: {name} ({domain})")
        start_agent_worker(agent_id)
        
        return JSONResponse({"agentId": agent_id})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

async def get_feed(request):
    agent_id = request.query_params.get("agentId")
    if not agent_id:
        return JSONResponse({"error": "agentId required"}, status_code=400)
        
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agents WHERE id = ?", (agent_id,))
    if not cursor.fetchone():
        conn.close()
        return JSONResponse({"error": "Agent not found"}, status_code=404)
        
    cursor.execute("SELECT * FROM posts WHERE agent_id = ? ORDER BY created_at DESC", (agent_id,))
    rows = cursor.fetchall()
    conn.close()
    
    posts = []
    for r in rows:
        posts.append({
            "id": r["id"],
            "createdAt": r["created_at"],
            "text": r["text"],
            "rationale": r["rationale"],
            "sources": json.loads(r["sources"])
        })
        
    return JSONResponse({"posts": posts})

def startup():
    logger.info("[SYSTEM] Initializing database...")
    init_db()
    
    logger.info("[SYSTEM] Restoring active agents...")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM agents WHERE status = 'ACTIVE'")
    active_agents = cursor.fetchall()
    conn.close()
    
    for agent in active_agents:
        logger.info(f"[SYSTEM] Restoring autonomous worker for agent {agent['id']}")
        start_agent_worker(agent['id'])

import contextlib
import os
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse

@contextlib.asynccontextmanager
async def lifespan_handler(app):
    startup()
    yield

async def serve_frontend(request):
    path = request.path_params.get("path", "")
    full_path = os.path.join("frontend/dist", path)
    if os.path.isfile(full_path):
        return FileResponse(full_path)
    return FileResponse("frontend/dist/index.html")

routes = [
    Route("/api/agent/init", init_agent, methods=["POST"]),
    Route("/api/agent/feed", get_feed, methods=["GET"]),
    Route("/{path:path}", serve_frontend)
]

app = Starlette(debug=True, routes=routes, lifespan=lifespan_handler)
