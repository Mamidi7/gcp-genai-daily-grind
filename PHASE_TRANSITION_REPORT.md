# Applied AI Prep — Phase Transition Report for Claude Evaluation

**Date:** 2026-03-24
**Prepared by:** Current Agent Session
**For:** Claude Code Industry-Grade Review

---

## 1. WHERE WE ARE RIGHT NOW

### Active Sprint
**Day 10→24 Execution Directives** (the active track, as of 2026-03-21 session)

### Last Completed Day
- **Day 11** (2026-03-21): Files + JSON + Environment Variables with fail-fast validation
  - Built: `.env` loading, JSON runtime config, `/config-summary` (safe), `/config-validate` (fails on missing `GCP_PROJECT_ID`)
  - Debug: `503` returned when `GCP_PROJECT_ID` absent — fixed by setting it
  - Interview output: 30s + 90s STAR + 3-min walkthrough all written

### Day 10 Cloud Storage work (also 2026-03-21):
- FastAPI + Gemini productionized with tests
- GCS file upload script working
- Deployed to Cloud Run with debug logs
- Committed as `feat(day10): productionize fastapi+gemini with tests and cloud run debug logs`

---

## 2. WHAT PHASE ARE WE EXITING

**Phase 1 (Days 1-10): Python + ML Basics — COMPLETE (rough)**

Evidence:
- Day 1-7: Python fundamentals (variables, lists, dicts, loops, functions, *args, **kwargs, Classes+OOP, JSON, File I/O, pip/venv, REST APIs) — checked off in UNIFIED_SCHEDULE
- Day 8: GCP Console + IAM + WIF — committed
- Day 9: GCP IAM Service Accounts — committed
- Day 10: Cloud Storage + FastAPI + Gemini + Cloud Run — committed + tested
- Day 11: Config/env/JSON validation — committed + interview artifacts written

**What Phase 1 built (concrete outputs):**
- `day1_python_gemini/` — Gemini API notebook
- `day10_cloud_storage/` — Full FastAPI + GCS + Vertex AI service
- `day10_cloud_storage/fastapi-gemini/` — Productionized version
- `day5_sql_joins.py` — SQL practice
- `day11_compute/` — Compute engine exercises
- `day15_langgraph/` — LangGraph agent
- GitHub green streak (last commit: 2026-03-21)
- 2 interview packs written + filed

---

## 3. WHAT PHASE WE ARE ENTERING

**Phase 2 (Days 11-18 in unified plan): GCP Foundations**

But wait — Day 11 is already done. Let me reconcile:

| Directive | Status |
|-----------|--------|
| Day 10 (Python functions, JSON, exceptions) | ✅ Done |
| Day 11 (Files, JSON, .env) | ✅ Done |
| Day 12 (FastAPI basics: /health, /echo, Pydantic) | ⏳ NEXT |
| Day 13 (FastAPI errors + validation) | ⏳ |
| Day 14 (BigQuery mental model: 5 SQL queries, joins, window fns) | ⏳ |
| Day 15 (LLM API wrapper — no framework magic) | ⏳ |
| Day 16 (Embeddings + chunking basics) | ⏳ |
| Day 17 (Retrieval baseline: top-k, print snippets) | ⏳ |
| Day 18 (Citations + no-answer behavior) | ⏳ |
| Day 19 (Evals intro: 10 test questions) | ⏳ |
| Day 20 (Eval harness v1: run 10 cases, log pass/fail) | ⏳ |
| Day 21 (Tool use basics: schema, args, validation) | ⏳ |
| Day 22 (Agent loop control: limit, timeout, trace) | ⏳ |
| Day 23 (GCP proof layer: Cloud Run deployable FastAPI) | ⏳ |
| Day 24 (Integration checkpoint: full architecture diagram) | ⏳ |

**Day 12 starts now.** Topic: FastAPI basics.

---

## 4. PROPOSED NEXT PHASE PLAN (Days 12-18)

### Day 12 — FastAPI Basics
**Learn:** How FastAPI receives a request, validates with Pydantic, and returns a response. What happens between `@app.post` and `return`.

**Build:**
- `/health` endpoint — returns `{"status": "ok"}`
- `/echo` endpoint — accepts JSON body, returns same shape
- Pydantic model for a "MathOperation" (operation: str, a: float, b: float)
- One endpoint using that model

**Debug:** What happens when you send wrong types? `{"a": "hello", "b": 2}` instead of numbers.

**Interview:** Explain request → validation → response flow in 30s / 90s.

---

### Day 13 — FastAPI Errors + Validation
**Learn:** Fail-fast validation, custom error responses, input constraints (min_length, gt, regex).

**Build:**
- Custom error response format: `{"error": "code", "message": "human readable", "field": "optional"}`
- Input constraint on MathOperation: operation must be one of ["add", "subtract", "multiply", "divide"]
- Divide by zero handling returning clean error

**Debug:** Blank string for operation, oversized input string — what does FastAPI return?

**Interview:** Explain fail-fast validation design.

---

### Day 14 — BigQuery Mental Model
**Learn:** What does a query engine store? Why do AI apps need analytics tables? Window functions for ranking/aggregation.

**Build:**
- 5 SQL queries on a mock/public dataset:
  1. Simple aggregation (COUNT, GROUP BY)
  2. JOIN between events and users table
  3. Window function (ROW_NUMBER, RANK, or LAG)
  4. Subquery or CTE
  5. UNION of two result sets
- Save each query with what it does + what could go wrong

**Debug:** Wrong join causing duplicate rows — how to detect + fix.

**Interview:** How would BigQuery fit into an AI app? (feedback events, eval results, context tables)

---

### Day 15 — LLM API Wrapper
**Learn:** What is a wrapper function vs direct SDK call? Why does it matter for testing and swapping models?

**Build:**
- One Python module `llm_wrapper.py`
- Function: `def generate(prompt: str) -> str` — calls Gemini API
- Function: `def generate_structured(prompt: str, schema: dict) -> dict` — returns Pydantic-parseable dict
- No FastAPI, no framework — just clean Python

**Debug:** What if the API returns malformed JSON? What if the key is wrong?

**Interview:** Wrapper vs direct SDK — why abstraction matters.

---

### Day 16 — Embeddings + Chunking
**Learn:** What is an embedding? How does chunking affect retrieval quality? What are the failure modes?

**Build:**
- Take 3 sample documents (or Lorem Ipsum paragraphs)
- Manually chunk them 3 ways: too small, too large, just right
- For each chunking strategy, explain: what would a semantic search get right/wrong?

**Debug:** Chunks that cut mid-sentence vs semantic boundaries.

**Interview:** How does chunking change answer quality?

---

### Day 17 — Retrieval Baseline
**Learn:** Keyword vs vector retrieval. Top-k selection. Why you should print retrieved docs before generating final answer.

**Build:**
- Simple embedding of 5 sample texts
- Top-2 retrieval by cosine similarity (can use numpy or just manual scoring)
- Print retrieved chunks before "generating answer"
- This separates retrieval quality check from generation

**Debug:** Relevant-sounding answer but wrong retrieved docs — how to detect.

**Interview:** Separate retrieval quality from generation quality.

---

### Day 18 — Citations + No-Answer Behavior
**Learn:** Why forcing citations prevents hallucinations. When to return "I don't know" instead of guessing.

**Build:**
- Modify Day 17's output to include citation of which chunk was used
- Add a "confidence threshold" — if top similarity score is below 0.5, return "Not enough context"
- Write the behavior into the wrapper

**Debug:** Answer given without sufficient evidence — detect and fix.

**Interview:** Why abstaining can be better than answering.

---

## 5. 14-DAY INTERVIEW SIGNAL TRACK (Days 12-25)

From the 14-Day Execution Tracker, next tools:

| Day | Tool 1 | Tool 2 | Purpose |
|-----|--------|--------|---------|
| 12 | `bundlephobia.com` | `caniuse.com` | Dependency size + browser API support check |
| 13 | `getfluently.app` | `overapi.com` | Speaking practice + revision |
| 14 | `roadmap.sh` | `regex101.com` | Gap map update + SQL regex bug |
| 15 | `httpie.io/app` | `webhook.site` | LLM API timeout test |
| 16 | `jsoncrack.com` | `carbon.now.sh` | Chunking visual + code card |
| 17 | `explainshell.com` | `shortcuts.design` | Terminal command breakdown |
| 18 | `bundlephobia.com` | `caniuse.com` | Dependency audit |
| 19 | `getfluently.app` | `overapi.com` | Speaking improvement log |
| 20 | `roadmap.sh` | `carbon.now.sh` | Updated gap map |
| 21 | `httpie.io/app` | `transform.tools` | API validation |
| 22 | `jsoncrack.com` | `regex101.com` | Architecture visual + regex |
| 23 | `explainshell.com` | `webhook.site` | Command breakdown + webhook |
| 24 | Any highest ROI | Final summary | Best artifact highlight |

---

## 6. WHAT I NEED CLAUDE TO EVALUATE

### Questions for Claude Code Review:

1. **Day 12 FastAPI scope**: Is building `/health`, `/echo`, and one Pydantic model enough, or should we add query parameters and path parameters too?

2. **BigQuery on Day 14**: Should we use the actual GCP BigQuery free sandbox / public dataset, or is writing the SQL queries against a local SQLite mock sufficient for interview signal?

3. **Day 15 LLM wrapper**: Direct Gemini API calls vs using LangChain/LangGraph for the wrapper — which produces better interview evidence?

4. **Days 16-18 (RAG chain)**: Should these three days be ONE integrated build (chunk → embed → retrieve → cite), or is splitting them into separate days better for learning?

5. **Eval harness timing**: The current plan puts evals on Days 19-20. But some would argue evals should come BEFORE building the RAG chain. Does the order in this plan make sense?

6. **Cloud Run / GCP proof layer (Day 23)**: Is this redundant with Day 10's Cloud Run work, or should Day 23 specifically focus on a second, different service (like Cloud Functions vs Cloud Run)?

7. **Integration checkpoint (Day 24)**: What exactly should the architecture diagram show? Should it be the full Day 10-23 stack combined, or a fresh clean design?

8. **GitHub commit hygiene**: Currently committing by day标签. Should we switch to conventional commits (feat/fix/docs)? Does it matter for interview signal?

9. **Interview packs**: We have 2 written. At what pace should we build these — one per completed directive day, or batched at end of phase?

10. **Day numbering mismatch**: The Unified Schedule shows Day 4 in progress (Classes + OOP) from Feb 27, but execution directives show Day 11 complete on March 21. How should we resolve this naming conflict for clarity?

---

## 7. WHAT GOOD LOOKS LIKE BY END OF DAY 24

| Artifact | Count | Where |
|----------|-------|-------|
| FastAPI endpoints | 5+ | day12-13/ |
| SQL queries | 5+ | day14/ + debug journal |
| LLM wrapper module | 1 | day15/ |
| Chunking experiments | 3 strategies | day16/ |
| Retrieval baseline | working top-k | day17/ |
| Citation system | with no-answer fallback | day18/ |
| Eval harness | 10 test cases + pass/fail log | day19-20/ |
| Tool schema | 1 defined + validated | day21/ |
| Agent loop | with limit + trace | day22/ |
| Cloud Run deployable | FastAPI service | day23/ |
| Architecture diagram | full stack | day24/ |
| Debug journal entries | 14 | interview_signal/ |
| Interview packs | 6+ | interview_signal/interview_packs/ |
| Commits | 14 | GitHub |

---

## 8. BLOCKERS / RISKS

1. **BigQuery access**: Need to confirm free-tier BigQuery is accessible or switch to SQLite mock
2. **Embedding model for Day 16-17**: Need to confirm whether to use Gemini embeddings API (free tier) or a local model
3. **Day numbering confusion**: Unified Schedule says Day 4, Execution Directives say Day 11. Needs one authoritative label.
4. **Interview packs pace**: 2 packs in ~1 month is slow. Need to sustain 1 per day minimum through Day 24.

---

*End of report. Ready for Claude Code evaluation and industry-grade course correction.*
