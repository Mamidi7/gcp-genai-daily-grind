# Day 10 Closeout

## Day
- `day10_cloud_storage`

## Topic
- Cloud Storage basics plus FastAPI + Gemini request flow and reliability framing

## What I Finished
- understood GCS bucket and object basics
- learned storage class decision logic
- connected GCS to an applied AI backend architecture
- captured two real FastAPI/Gemini failure cases
- completed SQL/BQ window-function practice pack (ROW_NUMBER, RANK, DENSE_RANK, LAG/LEAD)
- prepared manual-first packet, SQL/BQ track artifacts, and debug template

## What I Understood Well
- bucket vs object
- why storage class depends on access frequency
- why validation should happen before model call
- why retries and request IDs matter
- why `healthz` and `readyz` are different

## What Is Still Confusing
- no blocker for Day 10 closure
- deeper line-by-line endpoint walkthrough can be done later as optional revision

## Exact Next Step
- mark Day 10 as complete
- move to Day 11 topic track as per course flow
- carry forward one daily artifact habit:
  - one build action
  - one debugging artifact
  - one interview answer

## Debug Summary
- symptom: `/chat` returned `422` on empty prompt
- root cause: schema validation rejected invalid payload before model call
- fix: keep strict pydantic validation
- prevention: validate early, fail fast, avoid wasteful upstream calls
- impact: safer and more predictable API behavior

- symptom: `/chat` returned `502` on valid prompt
- root cause: upstream model invocation failure path
- fix: safe error mapping plus request tracing and retry wrapper
- prevention: keep timeout, retries, and request IDs in place
- impact: graceful degradation and easier debugging

## Interview Artifacts
- 30-second version:
  I studied how Cloud Storage, FastAPI, Gemini, and BigQuery-style analytics fit together in one applied AI backend. I focused on why each block exists, not just how to call the tools, and I documented real failure paths like validation errors and upstream model failures.

- 90-second STAR:
  I was improving a learning project from a simple AI demo into something closer to production behavior. My task was to understand the architecture clearly and make failures interview-worthy instead of random. I mapped out how Cloud Storage holds artifacts, how FastAPI handles validated requests, and how Gemini sits behind retry and error-handling logic. During testing, I captured real `422` and `502` failure cases, documented root causes, and linked them to prevention steps like strict schema validation and safe upstream error mapping. The result was a much clearer mental model and stronger interview evidence because I could explain both the system and the failures calmly.

- 3-minute technical walkthrough:
  Start with the user request. Files and supporting artifacts should live outside the app in Cloud Storage because the API container is ephemeral. FastAPI receives the request, validates the payload with schema rules, adds request-level tracing, and then calls Gemini through a retry wrapper. If the payload is invalid, the request fails early with a clear client error. If the upstream model fails, the app returns a safe mapped error like `502` instead of leaking raw failure details. BigQuery does not need to be fully integrated yet, but it is the right place to analyze request logs, retries, feedback, and later evaluation-style metrics. This makes the architecture useful for both learning and interviews because it shows storage, API flow, model integration, observability, and debugging in one system.

## Day 10 Interview Insights (Final)
- architecture insight: interviewers care that you connect storage, API, model, and analytics as one production story
- reliability insight: showing real `422` and `502` with root cause and prevention gives stronger signal than only happy-path demo
- data insight: BigQuery window functions are directly useful for request analytics, retry trends, and feedback ranking
- communication insight: explain in layers (30s, 90s STAR, 3min deep dive) instead of memorizing each line
- judgment insight: move forward when objective is achieved; keep deep line-by-line review as optional revision, not a blocker

## Quality Score
- `10/10` (Day 10 closed on 2026-03-20)

Reason:
- simple explanation exists
- visual packet exists
- block-wise why exists
- manual-first flow exists
- same example exists
- real error paths exist
- SQL/BQ artifact exists
- interview answers exist
- handoff files are updated
- today’s commit-ready artifacts exist

## Restart Prompt
- Day 10 complete. Start Day 11 according to course track and capture one debug-to-interview artifact.
