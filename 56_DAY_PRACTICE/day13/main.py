# day13_fastapi_errors.py | python>=3.12 | requires: fastapi[standard]==0.135.1 pydantic==2.7.1 uvicorn[standard]==0.29.0
"""
Day 13: FastAPI Errors and Validation
Extends Day 12 app with input constraints, clean error responses, and custom exception.

Run:
    python3 -m uvicorn main:app --host 127.0.0.1 --port 8013
"""
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator

PORT = int(os.getenv("PORT", 8013))
app = FastAPI(title="Day13 FastAPI Errors & Validation", version="1.0.0")


# ─── Request Model with Input Constraints ────────────────────────────────────

class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=500,
    )
    username: str = Field(
        default="anonymous",
        min_length=1,
        max_length=50,
    )

    @field_validator("question")
    @classmethod
    def question_not_all_whitespace(cls, v: str) -> str:
        stripped = v.strip()
        if len(stripped) < 3:
            raise ValueError("Question must be at least 3 non-whitespace characters")
        return stripped

    @field_validator("username")
    @classmethod
    def username_clean(cls, v: str) -> str:
        # Strip whitespace from username
        return v.strip()


# ─── Custom Exception Handler — Clean 422 Responses ──────────────────────────

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Transform raw Pydantic 422 into a clean, consistent error structure."""
    # exc.errors() returns list of dicts with potential non-JSON objects
    # e.g. ctx: {error: ValueError(...)}. Flatten to strings for safe serialization.
    def _sanitize(error: dict) -> dict:
        return {
            "type": error.get("type", ""),
            "loc": list(error.get("loc", [])),
            "msg": error.get("msg", ""),
        }

    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_failed",
            "message": "One or more fields failed validation",
            "fields": [_sanitize(e) for e in exc.errors()],
        },
    )


# ─── Custom HTTP Exception ───────────────────────────────────────────────────

@app.post("/question")
async def submit_question(payload: QuestionRequest):
    """
    Accept a question, enforce business rules, return clean response.
    Raises:
        HTTPException 400 if question starts with reserved keyword
    """
    # Business rule: reserved keyword
    if payload.question.lower().startswith("ignore"):
        raise HTTPException(
            status_code=400,
            detail="Questions starting with 'ignore' are not allowed",
        )

    # Business rule: check question length after stripping
    clean_len = len(payload.question.strip())
    return {
        "status": "accepted",
        "question": payload.question,
        "username": payload.username,
        "clean_char_count": clean_len,
    }


# ─── Health Check ────────────────────────────────────────────────────────────

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# ─── Debug Endpoint — Echo with Validation ──────────────────────────────────

@app.post("/echo")
def echo(payload: QuestionRequest) -> dict[str, str]:
    """Echo back the question. Proves validation ran before this handler."""
    return {
        "echo": payload.question,
        "username": payload.username,
    }


# ─── Run Note ────────────────────────────────────────────────────────────────
# To test manually:
#   python3 -m uvicorn main:app --host 127.0.0.1 --port 8013
#
# Valid request:
#   curl -X POST http://127.0.0.1:8013/question \
#     -H "Content-Type: application/json" \
#     -d '{"question": "What is Vertex AI?", "username": "krishna"}'
#
# Blank question → 422 via custom handler
# Oversized question → 422 via max_length
# "ignore this" → 400 via HTTPException
