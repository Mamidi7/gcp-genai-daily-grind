# DAY14 - BigQuery for AI Systems

## Goal
Complete this day manually with verified outputs only.

## Syllabus
- Core concept understanding
- Small build artifact
- One debug artifact
- Interview conversion (30s, 90s STAR, 3-min)

## Industry Framing
Use BigQuery as the offline data backbone for AI systems:
- event and usage log store
- document and chunk metadata store
- embedding table store
- eval and result analysis store

## ASCII Architecture
```text
Users / APIs
    |
    v
App Events -----> BigQuery raw/events tables
Documents  -----> BigQuery chunk metadata tables
Embeddings -----> BigQuery vector-ready tables
LLM outputs ----> BigQuery eval / audit tables
    |
    v
SQL analysis -> retrieval prep -> offline evaluation -> interview story
```

## Step-by-Step Plan
1. Write one aggregation query for usage or trend analysis
2. Write one join query for relational enrichment
3. Write one window function query for ranking or temporal analysis
4. Debug one duplicate-row issue from wrong join and validate cardinality
5. Explain where BigQuery fits in AI app architecture and eval loops

## Status Log (Update in this file)

| Block | Status | Start | End | Evidence |
|---|---|---|---|---|
| Step 1 | completed | 2026-03-27 | 2026-03-27 | `day14/bq_patterns.py` query `1_aggregation` |
| Step 2 | completed | 2026-03-27 | 2026-03-27 | `day14/bq_patterns.py` query `2_join_cte` |
| Step 3 | completed | 2026-03-27 | 2026-03-27 | `day14/bq_patterns.py` query `3_window_function` |
| Step 4 | completed | 2026-03-27 | 2026-03-27 | `day14/debug_journal_day14.md` |
| Step 5 | completed | 2026-03-27 | 2026-03-27 | `day14/day14_bigquery_interview_pack.md` |
| Day Closeout | completed | 2026-03-27 | 2026-03-27 | tracker + weekly wrap marked supporting |

## Why This Matters in Real Systems
- If SQL is wrong, dashboards, eval scores, and retrieval inputs become misleading.
- BigQuery lets teams analyze AI behavior without moving data into separate analytics systems.
- Strong BigQuery understanding makes your ETL background useful in Applied AI interviews.

## Completion Criteria
- [x] Code/query artifact done
- [x] Debug artifact done
- [x] Interview artifact done
- [x] Progress files updated (`SESSION_STATE.md`, `DAILY_PROGRESS_LOG.md`, `DAYWISE_EXECUTION_MEMORY.md`)


## Topic Completion Checkboxes

- [x] Step 1: Write one aggregation query
- [x] Step 2: Write one join query
- [x] Step 3: Write one window function query
- [x] Step 4: Debug one duplicate-row issue from wrong join
- [x] Step 5: Explain where BigQuery fits in AI app architecture
- [x] Day Closeout

## Practice Exercise
Take one imagined AI support bot and answer:
1. What would go into BigQuery?
2. What would stay in object storage?
3. What would stay in the online serving layer?

## Common Interview Questions
- Why use BigQuery for AI analytics instead of only logs in files?
- What is the risk of a bad join in an eval or retrieval pipeline?
- When would BigQuery be enough, and when would you add a separate online serving database?
