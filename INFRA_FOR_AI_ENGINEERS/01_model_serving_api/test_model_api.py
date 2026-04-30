"""
Tests for Model Serving API — Exercise 1
Run: pytest test_model_api.py -v

All tests mock the model call. No real API calls. Zero cost.
"""

import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

# Import the app
from solution.model_api import app

client = TestClient(app)


# ─── Health Check Tests ────────────────────────────────────────────────

def test_healthz_returns_200():
    """Liveness probe always returns 200."""
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "alive"


def test_readyz_returns_200_in_stub_mode():
    """Readiness probe returns 200 when credentials are available."""
    resp = client.get("/readyz")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ready"
    assert "gemini" in body["model"]


# ─── Input Validation Tests ────────────────────────────────────────────

def test_chat_rejects_empty_prompt():
    """Empty prompt → 422 (Pydantic min_length=1)."""
    resp = client.post("/chat", json={"prompt": ""})
    assert resp.status_code == 422


def test_chat_rejects_missing_prompt():
    """No prompt field → 422."""
    resp = client.post("/chat", json={})
    assert resp.status_code == 422


def test_chat_rejects_too_long_prompt():
    """Prompt > 10000 chars → 422."""
    resp = client.post("/chat", json={"prompt": "x" * 10001})
    assert resp.status_code == 422


def test_chat_rejects_negative_max_tokens():
    """Negative max_tokens → 422."""
    resp = client.post("/chat", json={"prompt": "hello", "max_tokens": -1})
    assert resp.status_code == 422


# ─── Happy Path (Mocked) ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_chat_returns_valid_response():
    """Mocked model call returns valid ChatResponse."""
    fake_result = {"text": "Hello! How can I help?", "tokens": 15}

    with patch("solution.model_api.call_model", new_callable=AsyncMock) as mock_model:
        mock_model.return_value = fake_result
        resp = client.post("/chat", json={"prompt": "hello"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["response"] == "Hello! How can I help?"
    assert body["tokens_used"] == 15
    assert body["model"] == "gemini-2.0-flash-001"
    assert body["latency_ms"] >= 0  # can be 0.0 if mocked call is instant


# ─── Error Handling (Mocked) ──────────────────────────────────────────

@pytest.mark.asyncio
async def test_chat_handles_model_error():
    """When model raises exception → 503 with error detail."""
    with patch("solution.model_api.call_model", new_callable=AsyncMock) as mock_model:
        mock_model.side_effect = RuntimeError("API quota exceeded")
        resp = client.post("/chat", json={"prompt": "hello"})

    assert resp.status_code == 503
    assert "RuntimeError" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_chat_handles_timeout():
    """Timeout from model → 503."""
    with patch("solution.model_api.call_model", new_callable=AsyncMock) as mock_model:
        mock_model.side_effect = TimeoutError("Model took too long")
        resp = client.post("/chat", json={"prompt": "hello"})

    assert resp.status_code == 503


# ─── Response Validation ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_chat_response_has_all_fields():
    """ChatResponse contains all required fields."""
    fake_result = {"text": "test", "tokens": 5}

    with patch("solution.model_api.call_model", new_callable=AsyncMock) as mock_model:
        mock_model.return_value = fake_result
        resp = client.post("/chat", json={"prompt": "test"})

    body = resp.json()
    required_fields = {"response", "model", "latency_ms", "tokens_used"}
    assert required_fields.issubset(set(body.keys()))
