# Applied AI 56-Day Topic Map

This is the corrected high-level topic roadmap for preparing toward an Applied AI Engineer role.

It is based on:

- existing repo structure
- current day trackers
- Day10 FastAPI + Gemini proof work
- industry-grade track files already present in the repo

## Main Learning Path

### 1. Core Python and Data Handling

- Python fundamentals
- files, JSON, env vars
- async basics
- clean functions
- debugging basics
- simple testing

### 2. Backend and API Foundations

- FastAPI request flow
- validation
- error handling
- health and readiness checks
- middleware
- retries and timeouts
- schema contracts

### 3. GCP Foundations

- IAM
- Cloud Storage
- BigQuery mental model
- Cloud Run
- service revisions
- manual console deployment
- Vertex AI basics

### 4. LLM Application Layer

- prompt input/output handling
- LLM wrapper design
- embeddings
- chunking
- retrieval baseline
- citations and no-answer mode
- prompt robustness
- guardrails

### 5. Evaluation Layer

- eval basics
- eval harness
- retrieval evaluation
- prompt failure cases
- measurable quality checks

### 6. Agent Systems

- tool use basics
- tool routing
- agent loop control
- safe tool calling
- constrained agent behavior

### 7. Data and ML Engineering

- batch pipeline skeleton
- incremental loads
- watermark logic
- data quality checks
- feature pipelines
- point-in-time safe joins
- baseline model evaluation

### 8. Production Engineering

- structured logging
- error taxonomy
- monitoring
- drift detection
- postmortem writing
- runbooks
- reliability stories

### 9. GCP Proof and Portfolio

- deploy real mini-services
- show GCP proof
- architecture diagrams
- debug cards
- metrics snapshots
- portfolio README

### 10. Interview Conversion

- 30-second explanation
- STAR stories
- debugging story
- system design walkthrough
- tradeoff explanation
- mock interview answers

## Highest-Value Topics For The Target Role

If the target is Applied AI Engineer, the highest-value areas are:

1. LLM apps and API integration
2. retrieval and RAG plus evals
3. agents and tool use
4. production reliability
5. GCP deployment proof
6. debugging stories explained clearly

## Lower-Priority Areas

- spending many days on very basic FastAPI endpoints
- too much theory without code or debug evidence
- repeated note-making without strong build artifacts

## Important Reality Check

FastAPI should not consume many more days because the repo already shows:

- `/chat`
- `/generate`
- `/healthz`
- `/readyz`
- validation
- retries
- error mapping
- Cloud Run deployment

So from this point, FastAPI should be treated as a tool you use, not the main topic itself.

## Best 56-Day Shape

- Days 1-10: Python + GCP + first deployed API
- Days 11-20: validation, wrappers, embeddings, retrieval, eval basics
- Days 21-30: agents, guardrails, reliability, logging, data contracts
- Days 31-42: pipelines, ML baseline, serving, monitoring, drift
- Days 43-56: portfolio proof, GCP proof, interview drills, postmortems, mocks

## Final Direction

To crack the target role, the path should optimize for:

- LLM systems
- production thinking
- GCP proof
- debugging rigor
- interview clarity

Not for repeating basic API tutorials after those basics are already demonstrated in the repo.
