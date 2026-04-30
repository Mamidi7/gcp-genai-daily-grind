"""
Model Serving API — Exercise 1
FastAPI endpoint that wraps Gemini with input validation, health checks,
structured logging, and proper error handling.

Run: uvicorn solution.model_api:app --reload --port 8000
Test: pytest test_model_api.py -v
"""

import os
import time
import json
import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Structured JSON logging
# ---------------------------------------------------------------------------
logger = logging.getLogger("model_api")
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","msg":%(message)s}',
)

# ---------------------------------------------------------------------------
# Pydantic models — Input + Output validation
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    """What the client sends us."""
    prompt: str = Field(..., min_length=1, max_length=10000,
                        description="The user prompt to send to the model")
    max_tokens: Optional[int] = Field(default=256, ge=1, le=8192,
                                       description="Max tokens in response")


class ChatResponse(BaseModel):
    """What we send back."""
    response: str
    model: str
    latency_ms: float
    tokens_used: int = 0


# ---------------------------------------------------------------------------
# Fake model call (replace with real Vertex AI in production)
# ---------------------------------------------------------------------------

# Set USE_REAL_MODEL=1 and configure gcloud auth to use real Gemini.
# Tests should NEVER set this — they mock call_model() directly.

async def call_model(prompt: str, max_tokens: int = 256) -> dict:
    """
    Call the LLM. Returns {"text": "...", "tokens": N}.

    In production, this calls Vertex AI Gemini:
        from google.cloud import aiplatform
        from vertexai.generative_models import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash-001")
        response = model.generate_content(prompt, generation_config=...)
        return {"text": response.text, "tokens": response.usage_metadata.total_token_count}

    For local dev / testing, we return a stub.
    """
    if os.getenv("USE_REAL_MODEL") == "1":
        # Real Vertex AI call (requires gcloud auth)
        from vertexai.generative_models import GenerativeModel
        import asyncio
        model = GenerativeModel("gemini-2.0-flash-001")
        def _sync_call():
            resp = model.generate_content(prompt)
            return {
                "text": resp.text,
                "tokens": resp.usage_metadata.total_token_count,
            }
        return await asyncio.to_thread(_sync_call)
    else:
        # Stub for local dev — simulates model behavior
        await _fake_delay()
        return {
            "text": f"[stub] You said: {prompt[:50]}...",
            "tokens": len(prompt.split()) + 10,
        }


async def _fake_delay():
    """Simulate model latency for local dev."""
    import asyncio
    await asyncio.sleep(0.05)


# ---------------------------------------------------------------------------
# Health check helpers
# ---------------------------------------------------------------------------

def _check_model_credentials() -> bool:
    """Check if we have what we need to call the model."""
    if os.getenv("USE_REAL_MODEL") == "1":
        # In production, check if gcloud auth is configured
        return os.path.exists(os.path.expanduser("~/.config/gcloud/application_default_credentials.json"))
    return True  # stub mode always "ready"


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Model Serving API",
    version="1.0.0",
    description="Exercise 1: Container-ready model serving endpoint",
)

MODEL_NAME = "gemini-2.0-flash-001"


@app.get("/healthz")
async def healthz():
    """Liveness probe — is the process alive?"""
    return {"status": "alive"}


@app.get("/readyz")
async def readyz():
    """Readiness probe — can we serve requests?"""
    if _check_model_credentials():
        return {"status": "ready", "model": MODEL_NAME}
    return {"status": "not_ready", "reason": "model credentials missing"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Main endpoint: send prompt, get model response.

    Input validation: Pydantic handles min_length, max_length, ge, le.
    If validation fails, FastAPI returns 422 automatically.
    """
    start = time.perf_counter()
    prompt_len = len(req.prompt)

    try:
        result = await call_model(req.prompt, req.max_tokens)
        latency_ms = (time.perf_counter() - start) * 1000

        logger.info(json.dumps({
            "event": "chat_success",
            "prompt_length": prompt_len,
            "latency_ms": round(latency_ms, 1),
            "tokens_used": result["tokens"],
            "model": MODEL_NAME,
        }))

        return ChatResponse(
            response=result["text"],
            model=MODEL_NAME,
            latency_ms=round(latency_ms, 1),
            tokens_used=result["tokens"],
        )

    except Exception as e:
        latency_ms = (time.perf_counter() - start) * 1000
        logger.error(json.dumps({
            "event": "chat_error",
            "prompt_length": prompt_len,
            "latency_ms": round(latency_ms, 1),
            "error_type": type(e).__name__,
            "error_detail": str(e)[:200],
        }))
        raise HTTPException(status_code=503, detail=f"Model error: {type(e).__name__}")


# ---------------------------------------------------------------------------
# Run directly for quick testing
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
