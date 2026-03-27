# Day 14 Practice Folder

This folder is the single source of truth for Day 14 work.

## Plain-English Purpose
Day 14 is not just "SQL practice." It is about learning how BigQuery supports real AI systems:
- analytics on user and model events
- preparation for retrieval pipelines
- offline evaluation and debugging

## Industry Framing
Think of BigQuery as the warehouse where AI teams inspect behavior after the model call:
- what users asked
- what chunks were retrieved
- what answers were returned
- which evals passed or failed

## ASCII Architecture
```text
User traffic / docs / model outputs
              |
              v
        BigQuery tables
   raw -> transformed -> eval
              |
              v
   SQL analysis and retrieval prep
```

## Execution Order
1. Read `DAY_PLAN.md`
2. Run/review `bq_patterns.py`
3. Review failure analysis in `debug_journal_day14.md`
4. Practice speaking from `day14_bigquery_interview_pack.md`
5. Keep weekly summary docs as supporting context only

## Files
- `DAY_PLAN.md` — task checklist and completion evidence
- `bq_patterns.py` — 5 BigQuery SQL patterns mapped to AI-system use cases
- `debug_journal_day14.md` — duplicate join bug, root cause, fix, prevention, and cardinality checks
- `day14_bigquery_interview_pack.md` — 30s, 90s STAR, 3-min walkthrough
- `day14_2026-03-27_bigquery_execution.md` — primary day execution summary
- `day14_2026-03-26.md` — supporting weekly wrap
- `day14_best_story_week.md` — supporting weekly interview story wrap

## What Goes In / Inside / Comes Out
- Goes in: events, documents, chunk metadata, embeddings, eval results
- Inside: SQL joins, ranking, aggregation, validation, and sanity checks
- Comes out: analytics, retrieval-ready tables, and interview stories grounded in real data work

## Failure Mode to Remember
Bad joins do not crash loudly. They often return believable but wrong results.
That is why cardinality checks and `COUNT(DISTINCT ...)` sanity queries matter.

## Practice Exercise
Write 3 short bullets for an AI chatbot:
- what belongs in BigQuery
- what belongs in GCS
- what should stay in the online application database

## Common Interviewer Question
Why would an enterprise AI team use BigQuery for embeddings metadata and eval analysis instead of keeping everything only in app memory or flat files?

## Transition Note
A2A manifest transition is implemented in:
- `../day10_cloud_storage/fastapi-gemini/main.py` via `GET /.well-known/agent.json`
