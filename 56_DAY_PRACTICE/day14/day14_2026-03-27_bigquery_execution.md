# Day 14 — 2026-03-27
## Topic: BigQuery Mental Model (Primary Execution Artifact)

## What Was Built
- `day14/bq_patterns.py` with 5 SQL patterns:
  - aggregation
  - join + CTE
  - window function
  - subquery
  - vector-search schema preview
- `day14/debug_journal_day14.md` for duplicate-row join bug and fix
- `day14/day14_bigquery_interview_pack.md` with 30s/90s/3-min conversion

## A2A Transition (Carry-over)
A short transition update was applied in Day 10 FastAPI app:
- Added `GET /.well-known/agent.json` manifest endpoint
- This supports future ADK discovery while keeping Day 14 focus on BigQuery

## Verification Snapshot
- A2A endpoint shape verified locally via FastAPI test client
- Day 14 artifacts created and linked in tracker/docs

## Notes
- Weekly wrap document (`day14_2026-03-26.md`) remains valid but is marked as supporting evidence only.
- Primary Day 14 proof is BigQuery + debug + interview conversion.
