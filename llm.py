"""
CloverBot - LLM Interface
Supports both OpenAI API and Ollama with a unified interface.
Switch between providers via LLM_PROVIDER env var.
"""

import logging
import httpx
from openai import AsyncOpenAI

from config import Config
from rag import query_knowledge, format_context

logger = logging.getLogger("cloverbot.llm")

# OpenAI client (lazy init)
_openai_client = None


def get_openai_client():
    """Get or create the async OpenAI client."""
    global _openai_client
    if _openai_client is None:
        _openai_client = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)
    return _openai_client


async def generate_response(messages, session_id="unknown"):
    """
    Generate a response from the LLM.

    Args:
        messages: List of {"role": ..., "content": ...} dicts (conversation history)
        session_id: Session ID for logging

    Returns:
        dict with "content" (response text) and "escalate" (bool)
    """
    # Get the latest user message for RAG query
    user_message = ""
    for msg in reversed(messages):
        if msg["role"] == "user":
            user_message = msg["content"]
            break

    # Retrieve relevant knowledge
    rag_chunks = query_knowledge(user_message) if user_message else []
    rag_context = format_context(rag_chunks)

    # Build the system prompt with RAG context
    system_prompt = Config.SYSTEM_PROMPT
    if rag_context:
        system_prompt += "\n\n" + rag_context

    # Add escalation instruction
    system_prompt += (
        "\n\nIMPORTANT: If the visitor asks to speak with a human, requests a callback, "
        "or asks a question you truly cannot answer, end your response with the exact tag "
        "[ESCALATE] on its own line. Do not include this tag in normal responses."
    )

    # Build full message list
    full_messages = [{"role": "system", "content": system_prompt}] + messages

    # Route to the appropriate provider
    if Config.LLM_PROVIDER == "ollama":
        response_text = await _call_ollama(full_messages, session_id)
    else:
        response_text = await _call_openai(full_messages, session_id)

    # Check for escalation
    escalate = False
    if "[ESCALATE]" in response_text:
        escalate = True
        response_text = response_text.replace("[ESCALATE]", "").strip()

    return {"content": response_text, "escalate": escalate}


async def _call_openai(messages, session_id):
    """Call the OpenAI API."""
    try:
        client = get_openai_client()
        response = await client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        logger.error("[%s] OpenAI API error: %s", session_id, e)
        return (
            "I'm having a bit of trouble right now. "
            "Please try again in a moment, or reach out to our team directly at myclover.tech."
        )


async def _call_ollama(messages, session_id):
    """Call the Ollama API (local or remote)."""
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{Config.OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": Config.OLLAMA_MODEL,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 1024,
                    },
                },
            )
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "")
    except Exception as e:
        logger.error("[%s] Ollama API error: %s", session_id, e)
        return (
            "I'm having a bit of trouble right now. "
            "Please try again in a moment, or reach out to our team directly at myclover.tech."
        )
