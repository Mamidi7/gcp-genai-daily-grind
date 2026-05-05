# Session Resume — April 30, 2026

## What Was Done
- Full repo audit of ~/projects/gcp-genai-daily-grind
- Read all 3 plan docs from ~/projects/GCP_GENAI/_INTERVIEW_PREP/applied ai/
- Generated prioritized action plan

## Repo State Summary

### STRONG (real artifacts)
- Day 10: FastAPI + Gemini app + tests + Dockerfile (BEST artifact)
- Day 12/13: FastAPI progression + debug journals
- Day 16-20: Structured output, embeddings, chunking, eval harness

### WEAK (scaffolds/placeholders)
- Day 21-30: READMEs exist, exercises are empty TODOs
- Day 25-30: scaffold only, no solutions

### EMPTY/MISSING
- Day 31-56: NOT BUILT
- revision_sprint/: empty
- _EXTERNAL_REPOS/: uninitialized submodules
- projects/gcp_api_monitor/tests/: empty

## 5 Priority Actions Identified

### 1. Eval Harness (interview weapon #1)
- Extend eval_harness_v1.py with: faithfulness, relevance, citation accuracy, no-answer detection, adversarial tests
- Run on 20 real Q&A pairs, save results JSON

### 2. BQ Vector Search RAG (flagship project)
- Chunk PDFs -> Embed with Gemini -> BQ VECTOR column -> VECTOR_SEARCH -> generate answer -> eval score
- Uses BQ free tier (10GB free)

### 3. Portfolio Repo Cleanup
- Remove empty folders, fix uninitialized submodules
- Delete hermes-workspace nested project (noise)
- Rewrite README with links to best files, architecture diagram, how-to-run
- Add badge: 78 Python files, 5 test suites, 18 notebooks

### 4. Money-Making Cron Jobs
- Job Scraper (daily 8AM): scrape Indeed/LinkedIn for GCP AI/ML roles, auto-generate cover letters
- Doctor Lead Generator (weekly): scrape surgeon directories, competitor analysis, cold outreach
- Interview Q Generator (daily 7AM): pull latest questions, generate answers with project examples
- Content Repurposer (daily 6PM): convert daily learning into LinkedIn posts

### 5. 3 Interview-Ready Projects (from LEAN plan)
- Project 1 (Days 13-25): BQ Vector Search RAG + eval harness + Cloud Run deployment
- Project 2 (Days 26-38): ADK Agent + Memory Bank + MCP integration
- Project 3 (Days 39-47): ETL-to-LLM Pipeline + watermark + data quality

## Decision Pending
Krishna to pick starting point:
  A) Repo cleanup + README rewrite (1-2 hrs)
  B) Extend eval harness with 4 metrics (2-3 hrs)
  C) Set up Job Scraper cron (1 hr)
  D) Start BQ Vector Search RAG (the big one)

## Plan Docs (Source of Truth)
- OPTIMIZED_47_DAY_SPRINT_PLAN.md
- LEAN_47_DAY_PLAN_BASED_ON_REALITY.md
- APPLIED_AI_SHOCK_VALUE_PLAN_V3.md
All in: ~/projects/GCP_GENAI/_INTERVIEW_PREP/applied ai/
