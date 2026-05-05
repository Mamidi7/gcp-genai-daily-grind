# 13-Day Visual Revision Guide

### Your 13 Days of Applied AI Practice — Quick Reference
### Based on ACTUAL repo content (Days 1-13)

### Source: /Users/krishnavardhan/projects/GCP_GENAI/_INTERVIEW_PREP/applied ai/

### Repo: https://github.com/Mamidi7/gcp-genai-daily-grind

---

## THE BIG PICTURE — 13 Days in One Map

```
    Day 1          Day 2          Day 3          Day 4
    Python +     SQL WHERE    Functions    Classes +
    Gemini API    GROUP BY     def, return   OOP
                  ORDER BY     *args/**kwargs
                  
    Day 5          Day 6          Day 7
    JSON/File IO   Document    REST APIs +
    os module      Class       Gemini direct
                  to_dict()     (requests)
                  from_json()
                  
    Day 8          Day 9          Day 10
    GCP Console    IAM Roles    Cloud Storage
    Cloud Run     Service     FastAPI +
    Flask App     Accounts    Gemini API
    WIF Notes                  BigQuery SQL
                                Dockerfile
                                Deployment
                  
    Day 11         Day 12         Day 13
    Config        FastAPI       FastAPI
    Validation     /health      Errors &
    JSON Config    /echo        Field
    Env vars       Pydantic      Custom
                  Validation   Exception
                               Handler
```

---

## SKILL PROGRESSION CHAIN (What Builds on What)
```
                    ┌─────────────────────┐
                    │  DAY 1-4          │
                    │  Python Basics       │
                    │  (vars, funcs,     │
                    │   classes, JSON)   │
                    └────────┬──────────────┘
                             │
                    ┌──────▼──────────────────┐
                    │  DAY 5-7              │
                    │  APIs + OOP + Files   │
                    │  (requests, agents)│
                    └────────┬──────────────┘
                             │
                    ┌──────▼──────────────────┐
                    │  DAY 8-10             │
                    │  GCP + Deploy         │
                    │  (Cloud Run, IAM,   │
                    │   Storage, BigQuery)│
                    └────────┬──────────────┘
                             │
                    ┌──────▼──────────────────┐
                    │  DAY 11-13            │
                    │  Production API       │
                    │  (Config, Validation │
                    │   Error Handling)  │
                    └─────────────────────┘
```
---

## WHAT YOU ACTUALLY BUILT (Real Artifacts)
```
| Day | Key Artifact | File(s) |
|-----|--------------|--------|
| 1   | Gemini API call script | `day1_python_gemini/script.py` |
| 2   | SQL WHERE + GROUP BY | `day2/day2_variables.py` |
| 3   | Functions + exercises | `day3/day3_loops.py`, `day3/exercises.py` |
| 4   | Classes + OOP exercises | `day4/day04.py`, `day4/solution.py` |
| 5   | JSON read/write + config | `day5/config.json`, `day5/solution.py` |
| 6   | Document class with OOP | `day6/solution.py`, `day6/notes.md` |
| 7   | Gemini API (requests) + LangGraph | `day7/langgraph_gemini_agent.ipynb` |
| 8   | Flask app + Dockerfile + WIF setup | `day8_gcp/my_flask_app/`, `day8_gcp/WIF_NOTES.md` |
| 9   | IAM roles + ARRAY_AGG SQL | `day9_gcp_console_iam/notes.md` |
| 10  | FastAPI + Gemini + Cloud Run deployed | `day10_cloud_storage/fastapi-gemini/main.py` (297 lines!) |
| 11  | Config validation + debug journal | `day11/debug_journal_day11.md`, `day11/interview_pack_day11.md` |
| 12  | FastAPI /health + /echo + tests | `day12/main.py`, `day12/test_main.py` |
| 13  | Pydantic Field + custom exception handler | `day13/main.py`, `day13/test_main.py` |
```
---

## INTERVIEW CONVERSION TABLE (Your STAR Stories)
```
| Day | 30-Second Version | Debug Story |
|-----|-----------------|-------------|
| 8   | "I use WIF for CI/CD -- no service Account keys" | WIF attributeCondition blocked new repo (403) |
| 10  | "FastAPI + Gemini on Cloud Run with retries" | Response type hint caused ResponseValidationError |
| 11  | "Config validation: env + JSON separation" | Missing env var caught by fail-fast check |
| 12  | "FastAPI request lifecycle: route -> validate -> handle -> respond" | 422 vs 500 distinction (validation error vs handler bug) |
| 13  | "Fail-fast validation with Pydantic Field + custom exception handler" | Pydantic exc.errors() not JSON-serializable (ValueError in ctx) |
```
---

## TOP 5 THINGS TO REVISE FIRST (Before Any Interview)
```
1. Day 10 main.py — Your deployed FastAPI + Gemini service (the crown jewel)
2. Day 8 WIF_NOTES.md — Workload Identity Federation (keyless auth story)
3. Day 13 debug journal -- Pydantic serialization gotcha
4. Day 9 IAM roles table — Viewer vs Editor vs Owner
5. Day 6 Document class pattern — OOP with from_json()
```
---

## HOW THIS MAPS TO THE 47-DAY PLAN
```
YOUR 13 DAYS cover the FOUNDATION phase (Days 13-20 in the plan):

    Day 1-7   →  Python + API + Agent basics (you have this)
    Day 8-10  →  GCP + Cloud Run + deployment (you have this)
    Day 11-13 →  Config + Validation + Error handling (you have this)

NEXT UP (from applied ai/ folder):
    Day 14: BigQuery for AI systems (already done in repo)
    Day 15: LLM Wrapper Design (already done in repo)
    Day 16: Structured Output (JSON mode + Pydantic parsing)  -- NEXT TO BUILD
    Day 17: Embeddings Intro
    Day 18: Chunking Strategies
    Day 19-20: Eval Harness (THE #1 hiring signal)
    Day 21: BigQuery Vector Search RAG (the big one!)
```
---

*Next files in this revision:*
- `02_Days1to4_Python_Fundamentals.md` — Deep dive with visuals
- `03_Days5to7_JSON_OOP_Agents.md` — Deep dive with visuals
- `04_Days8to10_GCP_Deployment.md` — Deep dive with visuals
- `05_Days11to13_Config_Validation_Errors.md` — Deep dive with visuals
- `06_Cross-Cut_Concept_Map_+_Quiz.md` -- Final cross-day map + quiz
