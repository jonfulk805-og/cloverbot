"""
CloverBot - Main FastAPI Application
The backend API server for the CloverBot website AI agent.

Run with:
    python main.py
    -- or --
    uvicorn main:app --host 0.0.0.0 --port 8400 --reload
"""

import logging
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from config import Config
from database import (
    init_db,
    log_message,
    get_conversation_history,
    save_lead,
    get_leads,
    get_recent_conversations,
)
from llm import generate_response
from escalation import escalate_to_slack
from rag import ingest_knowledge_base

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/cloverbot.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("cloverbot")

# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------
limiter = Limiter(key_func=get_remote_address)

# ---------------------------------------------------------------------------
# In-memory session store (maps session_id -> metadata)
# ---------------------------------------------------------------------------
sessions = {}


def get_or_create_session(session_id=None):
    """Get existing session or create a new one."""
    if session_id and session_id in sessions:
        sessions[session_id]["last_active"] = time.time()
        return session_id

    new_id = str(uuid.uuid4())[:12]
    sessions[new_id] = {
        "created": time.time(),
        "last_active": time.time(),
        "lead_info": {},
        "message_count": 0,
    }
    return new_id


def cleanup_sessions():
    """Remove expired sessions."""
    cutoff = time.time() - (Config.SESSION_TIMEOUT_MINUTES * 60)
    expired = [sid for sid, data in sessions.items() if data["last_active"] < cutoff]
    for sid in expired:
        del sessions[sid]


# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown tasks."""
    # Startup
    logger.info("CloverBot starting up...")
    await init_db()

    # Ingest knowledge base
    doc_count = ingest_knowledge_base()
    logger.info("Knowledge base: %d documents ingested", doc_count)

    logger.info(
        "LLM provider: %s (model: %s)",
        Config.LLM_PROVIDER,
        Config.OPENAI_MODEL if Config.LLM_PROVIDER == "openai" else Config.OLLAMA_MODEL,
    )
    logger.info("Server ready on %s:%d", Config.HOST, Config.PORT)

    yield

    # Shutdown
    logger.info("CloverBot shutting down.")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="CloverBot API",
    description="AI Support Agent for MyClover.Tech",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiter
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests. Please slow down."},
    )


# Serve static files (the chat widget)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# ---------------------------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(default="")


class LeadRequest(BaseModel):
    session_id: str
    name: str = ""
    email: str = ""
    company: str = ""


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    escalated: bool = False


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------
@app.get("/")
async def root():
    """Health check."""
    return {"status": "ok", "service": "CloverBot", "version": "1.0.0"}


@app.post("/api/chat", response_model=ChatResponse)
@limiter.limit(f"{Config.RATE_LIMIT_PER_MINUTE}/minute")
async def chat(request: Request, body: ChatRequest):
    """Main chat endpoint."""
    cleanup_sessions()

    session_id = get_or_create_session(body.session_id or None)
    session = sessions.get(session_id, {})

    # Log user message
    await log_message(session_id, "user", body.message)

    # Get conversation history from DB
    history = await get_conversation_history(session_id, limit=20)

    # Make sure the current message is included
    if not history or history[-1].get("content") != body.message:
        history.append({"role": "user", "content": body.message})

    # Generate response
    result = await generate_response(history, session_id=session_id)
    reply = result["content"]
    escalated = result["escalate"]

    # Log bot response
    await log_message(session_id, "assistant", reply)

    # Update session
    if session_id in sessions:
        sessions[session_id]["message_count"] = session.get("message_count", 0) + 1

    # Handle escalation
    if escalated:
        lead_info = session.get("lead_info", {})
        await escalate_to_slack(session_id, body.message, reply, lead_info)

    return ChatResponse(
        reply=reply,
        session_id=session_id,
        escalated=escalated,
    )


@app.post("/api/lead")
async def capture_lead(body: LeadRequest):
    """Capture visitor lead information."""
    if body.session_id in sessions:
        sessions[body.session_id]["lead_info"] = {
            "name": body.name,
            "email": body.email,
            "company": body.company,
        }

    await save_lead(
        session_id=body.session_id,
        name=body.name,
        email=body.email,
        company=body.company,
    )

    return {"status": "ok", "message": "Thanks! How can I help you today?"}


@app.post("/api/ingest")
async def trigger_ingest():
    """Re-ingest the knowledge base (call after updating docs)."""
    count = ingest_knowledge_base()
    return {"status": "ok", "documents_ingested": count}


@app.get("/api/conversations")
async def list_conversations():
    """Admin: list recent conversations."""
    rows = await get_recent_conversations(limit=100)
    return {"conversations": rows}


@app.get("/api/leads")
async def list_leads():
    """Admin: list captured leads."""
    rows = await get_leads(limit=100)
    return {"leads": rows}


@app.get("/widget")
async def serve_widget():
    """Serve the chat widget HTML for testing."""
    widget_path = static_dir / "widget.html"
    if widget_path.exists():
        return FileResponse(str(widget_path))
    return {"error": "Widget not found. Check static/widget.html"}


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)

    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True,
        log_level="info",
    )
