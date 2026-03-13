# FastAPI + Gemini Continuation (2026-03-13)

## Goal (1 line)
Understand exactly what `/chat` does and how `_generate_with_retry()` protects reliability.

## 1) `/chat` Flow in Simple English

```text
Client -> POST /chat -> validate payload -> get request_id -> call retry wrapper
      -> model text back -> return structured JSON response
```

Inside `/chat`:
1. Get `request_id` from middleware (`request.state.request_id`).
2. Call `_generate_with_retry(payload)`.
3. Receive `(text, retries_used)`.
4. Return `PromptResponse` with `response`, `model`, `request_id`, `retries_used`.

Input:
- `prompt` (required, 1..6000 chars)
- `temperature` (0.0..1.0)
- `max_tokens` (1..2048)

Output:
- model response text + tracing info for debugging.

## 2) `_generate_with_retry()` Flow in Simple English

```text
Try model call
  -> success: return text
  -> fail: if retries left, wait and retry
  -> fail after max retries: map to safe HTTP error
```

What it does:
1. Starts with `retries_used = 0`.
2. Loops up to `MAX_RETRIES + 1` attempts.
3. Runs model call in a thread with timeout (`asyncio.wait_for + to_thread`).
4. On failure, waits with small backoff (`0.6 * (attempt + 1)`), then retries.
5. If all retries fail, maps error to `429/504/502` safely.

Why this matters:
- Prevents hanging requests.
- Handles temporary upstream glitches.
- Gives deterministic error responses.

## Minimal Example

Request:
```json
{
  "prompt": "Explain overfitting in 3 lines",
  "temperature": 0.4,
  "max_tokens": 120
}
```

Response shape:
```json
{
  "response": "...",
  "model": "gemini-2.0-flash-001",
  "request_id": "uuid",
  "retries_used": 0
}
```

## Common Mistake + Fix

Mistake:
- Treating `/generate` as fallback for `/chat`.

Fix:
- `/chat` and `/generate` are separate product behaviors.
- `/generate` intentionally pushes creativity (higher temperature/tokens).

## Debug Artifact (Interview-ready)

Symptom:
- `/chat` returns `502` on valid prompt.

Root cause:
- Upstream model invocation failed after retry window.

Fix:
- `_generate_with_retry()` + `_map_upstream_error()` returns safe, explicit status.

Prevention:
- Keep timeout, retries, and request-id logs enabled.

Impact:
- Predictable failures and faster incident triage.

## 30-second Interview Version

"I built a FastAPI endpoint for Gemini and productionized it with strict input validation, request tracing, timeout, and retry logic. The `/chat` route is thin and delegates reliability to a retry wrapper, which maps upstream failures into safe HTTP responses like 502/504/429. This made behavior deterministic under failure and improved debuggability through request IDs."

## Check Question

Why is it better to keep retry logic in `_generate_with_retry()` instead of writing retries directly inside `/chat`?

## Tiny Exercise

Change `MAX_RETRIES` from `2` to `1`, run one failure scenario, and record:
1. new `retries_used`
2. latency difference
3. user-facing status code
