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

## Interview Impact
I can explain not only SQL syntax but data correctness risk in analytics pipelines, which is directly relevant for AI/RAG retrieval pipelines backed by BigQuery.
