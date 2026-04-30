# Exercise 5: Request Logging Pipeline

## Goal (one line)
Log every LLM request/response with structured JSON, add PII redaction, and make logs searchable.

## Why This Matters
Interview question: "A user reports the model gave a wrong answer yesterday. How do you find it?"
Bad: "I grep the logs."
Good: "Every request is logged as structured JSON with request_id, timestamp, prompt_hash,
model version, latency, and token count. I query by timestamp range and prompt pattern.
PII is redacted at log time."

## What You Build

### 1. Structured Logging Middleware (FastAPI)
```python
# Every request gets a unique request_id
# Log: {request_id, timestamp, prompt_hash, response_hash, latency_ms, tokens, model, status}
# PII redaction: emails, phone numbers, SSNs replaced with [REDACTED]
```

### 2. Log Storage Options (pick one)
- Option A: Write to file (simplest, rotate with logrotate)
- Option B: Send to Loki (Grafana stack, free)
- Option C: Send to GCP Cloud Logging (production)

### 3. Log Query Script
```python
# query_logs.py -- search logs by time range, prompt pattern, error type
# python query_logs.py --from "2026-04-30" --to "2026-04-30" --filter "error"
```

## Key Insight for AI
Standard apps log: method, path, status_code, latency
AI apps MUST also log: prompt_length, response_length, tokens_used, model_version,
latency_breakdown (validation_time + model_time + serialization_time)

## Common Mistake
Logging the full prompt text. This leaks user data and violates privacy.
Fix: Log prompt_hash (SHA-256 first 8 chars) instead of the actual text.
If you need the full prompt for debugging, store it encrypted separately.

## Check Question
Why is structured JSON logging better than print() for AI systems?
(Answer: JSON is parseable. You can query it, aggregate it, alert on it.
print() is just text — you'd need regex to extract anything.)

## Tiny Exercise
1. Run the model_api with logging middleware
2. Make 5 requests
3. Run `python query_logs.py` and find all requests
4. Run `python query_logs.py --filter "error"` and find failed requests
5. Check that no raw prompt text appears in the logs (only hashes)
