# Day 10 FastAPI + Gemini Learning Path

Goal:
- Understand the topic manually before testing.
- Learn what each part does, why it exists, and what can fail.

## Learning Order

1. Understand the full request flow
2. Understand request validation
3. Understand Gemini client call
4. Understand retry + timeout
5. Understand logs and request IDs
6. Understand endpoints and their roles
7. Understand common failure paths

## Big Picture

```text
User
  |
  v
FastAPI app
  |
  +--> check input
  |
  +--> call Gemini
  |
  +--> return answer or safe error
  |
  v
logs + request_id
```

## What To Read First

1. `fastapi-gemini/main.py`
2. `FASTAPI_GEMINI_INDUSTRY_UPGRADE.md`
3. `notes.md`

## Manual Learning Tasks

### Task 1: Explain the system in 5 lines
Write in your own words:
- what comes in
- what the app checks
- what Gemini does
- what comes out
- what happens if it fails

### Task 2: Draw the flow
Make a small ASCII flow from request to response.

### Task 3: Explain each endpoint
- `/`
- `/healthz`
- `/readyz`
- `/chat`
- `/generate`

### Task 4: Explain validation rules
- prompt cannot be empty
- prompt has max size
- temperature has limits
- max_tokens has limits

### Task 5: Explain reliability features
- timeout
- retry
- request_id
- safe error mapping

## Minimum Understanding Check

You are ready to test only if you can answer:
- Why do we validate before calling Gemini?
- Why is retry useful?
- Why do we need request IDs?
- Why is `/readyz` different from `/healthz`?
- Why should errors return safe messages?

## Manual Output For Today

- one 5-line concept summary
- one ASCII flow
- one list of endpoints and purpose
- one common failure and fix
- one 30-second explanation

## Resume Point

This is where to restart next session.

### What Krishna already understood
- validation stops bad input early
- retries help with temporary failures
- request IDs help debugging
- `healthz` and `readyz` are different
- `/chat` is the normal endpoint
- `/generate` is the more creative endpoint

### Corrected request flow

```text
1. request comes in
2. FastAPI validates input
3. middleware adds request_id and starts timer
4. /chat calls _generate_with_retry()
5. Gemini returns answer or safe error
6. response goes back with logs and X-Request-ID
```

### Next topic to study
- Explain `/chat` line by line
- Then explain `_generate_with_retry()` line by line

### First question to restart with
- "What exactly happens inside `/chat` from first line to return statement?"
