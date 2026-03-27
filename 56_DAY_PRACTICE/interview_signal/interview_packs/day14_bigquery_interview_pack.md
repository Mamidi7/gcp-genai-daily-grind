# Day 14 Interview Pack — BigQuery in AI Apps

## 30-Second Answer
"For Day 14, I built five real BigQuery SQL patterns on public Stack Overflow data: aggregation, join with CTE, window function, subquery, and VECTOR_SEARCH schema preview. I also debugged a duplicate-row issue caused by incorrect join cardinality. This gave me a practical mental model of how BigQuery stores and serves analytics plus retrieval-ready data for AI systems."

## 90-Second STAR
**Situation:** I had BigQuery basics from earlier SQL practice, but no production-style query set tied to AI architecture.

**Task:** Build a Day 14 artifact that proves query fluency and debug discipline, not just theory.

**Action:**
1. Ran 5 query patterns on `bigquery-public-data.stackoverflow`.
2. Implemented an aggregation query for topic trend signals.
3. Implemented CTE + join query for accepted-answer linkage.
4. Implemented a window function query for ranking and temporal comparison.
5. Implemented a subquery for outlier scoring.
6. Added VECTOR_SEARCH table schema preview for upcoming retrieval pipeline work.
7. Captured a real join-duplicate failure and fixed it by aligning join condition with expected one-to-one mapping.

**Result:** I now have a concrete Day 14 proof set: code artifact, debug journal, and interview narrative. I can clearly explain how BigQuery supports both analytics and retrieval foundations in AI applications.

## 3-Minute Technical Walkthrough
### Where BigQuery fits in an AI app
- **Ingest layer:** raw logs, events, and documents are staged in partitioned tables.
- **Preparation layer:** SQL transforms normalize content, compute metrics, and enrich metadata.
- **Retrieval layer:** embeddings and chunk metadata can be stored in BigQuery tables to support vector retrieval workflows.
- **Evaluation layer:** model outputs, pass/fail signals, and latency metrics can be logged for offline evaluation.

### What I built on Day 14
- Aggregation for trend discovery (`COUNT`, `AVG` by tag)
- Join/CTE for relational linkage (question -> accepted answer)
- Window function for ranking and progression (`ROW_NUMBER`, `LAG`)
- Subquery for dynamic thresholding (score > 3x average)
- Vector-search schema preview (`embedding ARRAY<FLOAT64>`) for later retrieval tasks

### Failure path and fix
- **Failure:** duplicate amplification from one-to-many join.
- **Fix:** explicitly join accepted answer ID for one-to-one semantics.
- **Prevention:** validate cardinality assumptions with `COUNT(DISTINCT ...)` checks before shipping queries.

### Interview line
"I treat SQL correctness as model-quality infrastructure. If retrieval or analytics queries are wrong, AI outputs become unreliable even when the model is good."
