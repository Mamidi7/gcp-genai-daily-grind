# Day 10 FastAPI + Gemini Industry Upgrade

You already completed:
- Vertex Gemini call from Python
- GCS upload script
- Cloud Function deployment
- FastAPI Gemini starter app

Now upgrade this into interview-grade quality.

## 1) Production Gaps to Close

1. Request/response schema validation
2. Timeout and retry around model calls
3. Structured logs with request_id
4. Error mapping (400/429/500)
5. Basic rate limiting guard
6. Health/readiness endpoints

## 2) Implementation Tasks (Today/Next 2 Days)

1. Add Pydantic models for input/output payloads.
2. Add timeout and retry wrapper for `client.models.generate_content`.
3. Add `X-Request-ID` propagation and log in every request.
4. Add exception classes:
- `ValidationError` -> 400
- `RateLimitError` -> 429
- `UpstreamModelError` -> 502
5. Add `/healthz` and `/readyz` endpoints.
6. Add simple request logging middleware (latency + status code).

## 3) Debug Drills (Must Perform)

1. Empty prompt request
- Expected: 400 with clear message

2. Very long prompt causing upstream failure
- Expected: handled error path, no stacktrace leak

3. Simulated timeout
- Expected: retry attempts then 504/502 mapped response

4. Missing env/project config
- Expected: clear startup failure message

## 4) Interview Leverage Story

"I started with a working FastAPI + Gemini prototype. Then I productionized it by adding strict request validation, retry/timeout control, and structured observability. During debugging, I identified unhandled upstream timeout paths and fixed them with deterministic error mapping and request-level tracing, which improved reliability and diagnosability."

## 5) Metrics to Capture

- p50/p95 endpoint latency
- success/error rate
- timeout count
- retry success rate

Even if small scale, these metrics make your explanation industry-grade.

## 6) Deliverables Checklist

- [ ] Updated `main.py` with validation and error handling
- [ ] Middleware logging added
- [ ] 4 debug cases documented in `notes.md`
- [ ] 1 postmortem note for worst failure
- [ ] 90-second and 3-minute interview versions prepared
