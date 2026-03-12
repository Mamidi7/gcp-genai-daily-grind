"""
FastAPI + Vertex AI (Gemini) App
Run: uvicorn main:app --reload --port 8080
"""

from __future__ import annotations

import asyncio
import logging
import time
import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import google.genai as genai
from google.genai import types

MODEL_NAME = "gemini-2.0-flash-001"
PROJECT_ID = "e2e-etl-project"
LOCATION = "us-central1"
MAX_PROMPT_CHARS = 6000
DEFAULT_TIMEOUT_SECONDS = 20
MAX_RETRIES = 2

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("fastapi-gemini")

app = FastAPI(title="Gemini API", version="1.1.0")


class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=MAX_PROMPT_CHARS)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=256, ge=1, le=2048)


class PromptResponse(BaseModel):
    response: str
    model: str
    request_id: str
    retries_used: int


class ErrorResponse(BaseModel):
    error: str
    request_id: str


# Initialize Vertex AI client once at startup.
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    start = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        latency_ms = int((time.perf_counter() - start) * 1000)
        logger.exception(
            "request_failed request_id=%s method=%s path=%s latency_ms=%s",
            request_id,
            request.method,
            request.url.path,
            latency_ms,
        )
        raise

    latency_ms = int((time.perf_counter() - start) * 1000)
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "request_done request_id=%s method=%s path=%s status=%s latency_ms=%s",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        latency_ms,
    )
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    request_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=str(exc.detail), request_id=request_id).model_dump(),
    )


def _map_upstream_error(err: Exception) -> tuple[int, str]:
    text = str(err).lower()
    if "rate" in text and "limit" in text:
        return 429, "Upstream rate limit exceeded"
    if "timeout" in text or "deadline" in text:
        return 504, "Upstream model timeout"
    return 502, "Upstream model call failed"


async def _generate_with_retry(payload: PromptRequest) -> tuple[str, int]:
    retries_used = 0
    last_error: Optional[Exception] = None

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    client.models.generate_content,
                    model=MODEL_NAME,
                    contents=payload.prompt,
                    config=types.GenerateContentConfig(
                        temperature=payload.temperature,
                        max_output_tokens=payload.max_tokens,
                    ),
                ),
                timeout=DEFAULT_TIMEOUT_SECONDS,
            )
            return (response.text or ""), retries_used
        except Exception as exc:
            last_error = exc
            if attempt < MAX_RETRIES:
                retries_used += 1
                await asyncio.sleep(0.6 * (attempt + 1))
                continue
            break

    if last_error is None:
        raise HTTPException(status_code=500, detail="Unknown model error")

    status, message = _map_upstream_error(last_error)
    raise HTTPException(status_code=status, detail=message)


@app.get("/")
def read_root():
    return {"message": "Gemini API is running", "status": "online", "model": MODEL_NAME}


@app.get("/healthz")
def healthz():
    return {"status": "healthy"}


@app.get("/readyz")
def readyz():
    try:
        # Lightweight readiness signal: client object exists and model string is configured.
        if client is None or not MODEL_NAME:
            raise ValueError("Client not ready")
        return {"status": "ready", "model": MODEL_NAME, "project": PROJECT_ID}
    except Exception:
        raise HTTPException(status_code=503, detail="Service not ready")


@app.post("/chat", response_model=PromptResponse)
async def chat(request: Request, payload: PromptRequest):
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    text, retries_used = await _generate_with_retry(payload)
    return PromptResponse(
        response=text,
        model=MODEL_NAME,
        request_id=request_id,
        retries_used=retries_used,
    )


@app.post("/generate", response_model=PromptResponse)
async def generate(request: Request, payload: PromptRequest):
    # Slightly more creative defaults for this route.
    creative_payload = PromptRequest(
        prompt=payload.prompt,
        temperature=max(payload.temperature, 0.8),
        max_tokens=max(payload.max_tokens, 512),
    )
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    text, retries_used = await _generate_with_retry(creative_payload)
    return PromptResponse(
        response=text,
        model=MODEL_NAME,
        request_id=request_id,
        retries_used=retries_used,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
