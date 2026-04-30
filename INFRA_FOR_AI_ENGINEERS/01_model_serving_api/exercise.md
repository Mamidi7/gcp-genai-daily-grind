# Exercise 1: Model Serving API with Tests

## Goal (one line)
Build a FastAPI endpoint that serves an LLM model, with proper tests that verify behavior.

## Why This Matters
Every AI/ML job asks: "How would you serve a model in production?"
If you say "I called the API in a notebook" — you fail.
If you say "I wrapped it in FastAPI with health checks, input validation,
structured logging, and integration tests" — you pass.

## Concept (3-6 lines)
1. A model serving API wraps an LLM call behind an HTTP endpoint
2. The endpoint accepts a prompt, calls the model, returns the response
3. Input validation catches bad requests BEFORE they hit the model (saves money)
4. Health checks let the infra know if the service is alive
5. Structured logging records every call for debugging and cost tracking
6. Tests prove it works — both the happy path AND the failure paths

## Architecture

```
Client Request
     │
     ▼
┌──────────────┐
│  FastAPI      │
│  ┌──────────┐ │   Input Validation (Pydantic)
│  │ /chat    │ │──→ Reject bad input → 422
│  └────┬─────┘ │
│       │       │
│  ┌────▼─────┐ │   Model Call (Gemini via Vertex AI)
│  │ Vertex AI│ │──→ Timeout/API Error → 503
│  └────┬─────┘ │
│       │       │
│  ┌────▼─────┐ │   Structured Log
│  │ Logger   │ │──→ JSON to stdout
│  └────┬─────┘ │
│       │       │
│  ┌────▼─────┐ │   Response Validation
│  │ Response │ │──→ Return validated JSON
│  └──────────┘ │
└──────────────┘
     │
     ▼
Client gets: { "response": "...", "model": "gemini-...", "latency_ms": 234 }
```

## What You Build

### 1. The API (`model_api.py`)
- POST /chat — takes prompt, calls Gemini, returns response
- GET /healthz — alive check (always returns 200)
- GET /readyz — ready check (verifies Gemini credentials exist)
- Input: { "prompt": string, "max_tokens": int (optional) }
- Output: { "response": string, "model": string, "latency_ms": float, "tokens_used": int }

### 2. The Tests (`test_model_api.py`)
- test_healthz_returns_200
- test_readyz_returns_200_when_env_set
- test_chat_rejects_empty_prompt (422)
- test_chat_rejects_too_long_prompt (422)
- test_chat_returns_valid_response (mocked)
- test_chat_handles_model_error (503)

### 3. Structured Logging
- Every /chat call logs: timestamp, latency_ms, tokens_used, prompt_length, status

## Common Mistake + Fix

Mistake: Calling the real Gemini API in every test.
  Why bad: Costs money, slow, flaky (network issues = test failures).
  Fix: Mock the Gemini call in tests. Only test real API in integration tests.

```python
# WRONG — calls real API in tests
def test_chat():
    response = client.post("/chat", json={"prompt": "hello"})
    assert response.status_code == 200

# RIGHT — mock the model call
def test_chat(mocker):
    mocker.patch("model_api.call_gemini", return_value={"text": "hi", "tokens": 5})
    response = client.post("/chat", json={"prompt": "hello"})
    assert response.status_code == 200
```

## Check Question
Why do we have both /healthz and /readyz? What's the difference?
(Answer in interview_answers.md after you think about it.)

## Tiny Exercise
1. Read `solution/model_api.py`
2. Run `pytest test_model_api.py -v`
3. All 6 tests should pass
4. Then break one thing (remove the mock) and see what happens
5. Write the failure in `debug_journal.md`
