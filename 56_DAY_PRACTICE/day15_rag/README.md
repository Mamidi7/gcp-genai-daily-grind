# Day 15 Practice — LLM Gateway Wrapper Design

This folder tracks Day 15 execution for a production-style model gateway boundary.

## Plain-English Purpose
Day 15 is about building one clean place where your app talks to the model.
Instead of every route calling the SDK directly, the wrapper standardizes requests, parsing, retries, and debugging metadata.

## Industry Framing
Treat this wrapper like a gateway layer:
- app code sends prompt text
- wrapper calls provider SDK
- wrapper validates structured output
- wrapper owns timeout, retry, and request metadata

## Files
- `DAY_PLAN.md` — execution checklist + evidence links
- `llm_api_wrapper.py` — provider-agnostic gateway wrapper with typed output
- `debug_journal_day15.md` — failure analysis (symptom -> root cause -> fix -> prevention)
- `interview_pack_day15.md` — 30s + 90s STAR + 3-min explanation

## ASCII Architecture
```text
Route / job / service
       |
       v
   LLM wrapper
  - parse JSON
  - validate schema
  - retry transient errors
  - timeout slow calls
  - attach request_id / latency / provider / model
       |
       v
   Provider SDK
```

## What Goes In / Inside / Comes Out
- Goes in: prompt text and gateway config
- Inside: model call, timeout handling, retry logic, schema validation
- Comes out: typed response object with metadata

## Failure Mode to Remember
Not every failure is the same:
- malformed JSON = parse problem
- timeout = latency budget problem
- repeated upstream failure = transport/provider problem

## Run
```bash
python3 llm_api_wrapper.py
```

## Validation
The script runs a local smoke test with a fake client and validates:
- success path parse,
- parse failure path,
- retry recovery,
- timeout classification.

## Practice Exercise
Write one paragraph answering:
"Why is a wrapper safer than calling the model SDK directly from a FastAPI route?"

## Common Interviewer Question
If your team later changes providers, what should stay unchanged in app code and what should change only inside the wrapper?
