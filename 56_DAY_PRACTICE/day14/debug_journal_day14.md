# Day 14 Debug Journal — BigQuery Join Duplicates

## Symptom
The joined result set had duplicated question rows, and aggregate counts looked inflated.

## Failing Query Pattern (Wrong Join)
```sql
SELECT q.id, q.title, COUNT(*) AS joined_rows
FROM `bigquery-public-data.stackoverflow.posts_questions` q
JOIN `bigquery-public-data.stackoverflow.posts_answers` a
  ON q.id = a.parent_id
WHERE q.score > 100
GROUP BY q.id, q.title
ORDER BY joined_rows DESC
LIMIT 20;
```

## Root Cause
This join is one-to-many by design (one question can have many answers). Counting joined rows as if they represent unique questions causes duplicate amplification.

## Why This Is Dangerous in AI Systems
- Retrieval evaluation can look better or worse than reality.
- Per-question metrics can be inflated.
- Offline analysis can push the team toward the wrong product decision.
- The bug often looks "reasonable," so it survives if you do not check row counts.

## Fix (Corrected Pattern)
If the goal is "accepted answer per question", join on `accepted_answer_id`.

```sql
WITH top_questions AS (
  SELECT id, title, accepted_answer_id, score
  FROM `bigquery-public-data.stackoverflow.posts_questions`
  WHERE score > 100
    AND accepted_answer_id IS NOT NULL
)
SELECT q.id, q.title, q.score, a.id AS accepted_answer_id
FROM top_questions q
JOIN `bigquery-public-data.stackoverflow.posts_answers` a
  ON q.accepted_answer_id = a.id
ORDER BY q.score DESC
LIMIT 20;
```

## Prevention
- Always define expected cardinality before writing join conditions.
- Use `COUNT(DISTINCT q.id)` to verify uniqueness assumptions.
- Add a quick sanity query before and after joins to compare row counts.
- Compare base table row counts, joined row counts, and distinct entity counts.
- Document whether the join is one-to-one, one-to-many, or many-to-many before writing metrics.

## Interview Impact
I can explain not only SQL syntax but data correctness risk in analytics pipelines, which is directly relevant for AI/RAG retrieval pipelines backed by BigQuery.

## Cardinality Sanity Check
```sql
SELECT
  COUNT(*) AS joined_rows,
  COUNT(DISTINCT q.id) AS distinct_questions
FROM `bigquery-public-data.stackoverflow.posts_questions` q
JOIN `bigquery-public-data.stackoverflow.posts_answers` a
  ON q.id = a.parent_id
WHERE q.score > 100;
```

If `joined_rows` is much larger than `distinct_questions`, the join is amplifying rows.
