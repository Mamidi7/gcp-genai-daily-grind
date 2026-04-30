# Interview Answers — Exercise 1: Model Serving API

## 30-Second Version
"I built a FastAPI model serving endpoint with Pydantic input validation,
structured JSON logging, health/readiness probes, and 10 unit tests covering
happy path, input validation, error handling, and response format."

## 90-Second STAR Answer
S: "I needed a production-ready way to serve LLM model predictions."
T: "The endpoint had to validate inputs, handle model failures gracefully,
    log every request, and be testable without calling the real API."
A: "I built it with FastAPI + Pydantic V2 for validation. Every request is
    logged as structured JSON with latency, token count, and status.
    Tests mock the model call so they're fast and free.
    I caught a floating point precision bug in latency measurement."
R: "10 tests pass in 0.18 seconds. The API can be containerized and deployed
    to Cloud Run. Health checks enable autoscaling and monitoring."

## 3-Minute Technical Deep Dive
"The system has 4 layers:

1. INPUT VALIDATION: Pydantic validates prompt length (1-10000 chars) and
   max_tokens (1-8192). Invalid inputs get 422 before they reach the model.
   This saves API costs — a 50,000 char prompt that would cost $0.50 is
   rejected at the edge for free.

2. MODEL ABSTRACTION: call_model() is a separate async function. In tests,
   it's mocked. In production, it calls Vertex AI Gemini via the SDK.
   This separation means I can swap models without touching the API layer.

3. ERROR HANDLING: Model failures return 503 (service unavailable) not 500.
   The distinction matters — 503 tells load balancers 'try another instance'.
   500 means 'this request is broken, don't retry'. Network timeouts,
   API quota errors, and unexpected exceptions all get proper error types.

4. OBSERVABILITY: Every request logs: prompt_length, latency_ms, tokens_used,
   model version, and event type (success/error). This JSON structure means
   I can query logs in production: 'show me all requests where latency > 2s'
   or 'what's my total token spend today?'"

## Check Question Answer
Q: Why both /healthz and /readyz?
A: /healthz = "is the process alive?" Used by Docker/K8s to restart dead processes.
   /readyz = "can it serve requests?" Checks if model credentials exist, DB is connected.
   A service can be alive but not ready — e.g., still loading model weights.
   K8s uses readiness to decide whether to route traffic to a pod.

## Tradeoff: FastAPI vs Flask
FastAPI: async-native, Pydantic validation built-in, auto-generated OpenAPI docs.
Flask: simpler, more mature, but needs manual validation and async support.
For AI serving where every millisecond counts, FastAPI's async is the right choice.

## Tradeoff: Mocking vs Real API in Tests
Mocking: fast (0.18s for 10 tests), free, deterministic.
Real API: slow (30s+), costs money, flaky (network issues).
Decision: mock all unit tests. Add one integration test suite that runs on schedule
with real API, not on every commit.
