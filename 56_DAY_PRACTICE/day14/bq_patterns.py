"""
Day 14 BigQuery artifact: 5 real SQL patterns on Stack Overflow public data.

Usage:
  export GOOGLE_CLOUD_PROJECT=<your-project>
  python bq_patterns.py

Notes:
- Queries use LIMIT and recent-date filters to keep cost reasonable.
- Query 5 is a VECTOR_SEARCH schema preview (actual retrieval query is a later-day step).
"""

from __future__ import annotations

import asyncio
import os
from typing import Iterable

from google.cloud import bigquery

PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")

QUERIES: dict[str, str] = {
    "1_aggregation": """
        SELECT
          REGEXP_EXTRACT(tags, r'<([^>]+)>') AS primary_tag,
          COUNT(*) AS question_count,
          AVG(score) AS avg_score
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE creation_date >= '2024-01-01'
        GROUP BY primary_tag
        ORDER BY question_count DESC
        LIMIT 10
    """,
    "2_join_cte": """
        WITH top_questions AS (
          SELECT id, title, accepted_answer_id, score
          FROM `bigquery-public-data.stackoverflow.posts_questions`
          WHERE score > 100
            AND accepted_answer_id IS NOT NULL
          LIMIT 100
        )
        SELECT q.title, q.score, a.body AS answer_preview
        FROM top_questions q
        JOIN `bigquery-public-data.stackoverflow.posts_answers` a
          ON q.accepted_answer_id = a.id
        ORDER BY q.score DESC
        LIMIT 10
    """,
    "3_window_function": """
        SELECT
          title,
          score,
          view_count,
          ROW_NUMBER() OVER (ORDER BY score DESC) AS rank_by_score,
          LAG(score) OVER (ORDER BY creation_date) AS prev_score
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE tags LIKE '%python%'
          AND creation_date >= '2024-01-01'
        LIMIT 20
    """,
    "4_subquery": """
        SELECT title, score
        FROM `bigquery-public-data.stackoverflow.posts_questions`
        WHERE tags LIKE '%python%'
          AND score > (
            SELECT AVG(score) * 3
            FROM `bigquery-public-data.stackoverflow.posts_questions`
            WHERE tags LIKE '%python%'
          )
        LIMIT 10
    """,
    "5_vector_schema_preview": """
        CREATE SCHEMA IF NOT EXISTS `{project}.rag_db`;

        CREATE TABLE IF NOT EXISTS `{project}.rag_db.chunks` (
          id STRING,
          content STRING,
          source_file STRING,
          chunk_index INT64,
          embedding ARRAY<FLOAT64>
        );

        SELECT 'VECTOR_SEARCH schema preview created. Run retrieval on Day 17.' AS note
    """,
}


def _format(sql: str) -> str:
    if "{project}" in sql:
        if not PROJECT:
            raise RuntimeError("Set GOOGLE_CLOUD_PROJECT for schema preview query")
        return sql.format(project=PROJECT)
    return sql


def _print_rows(rows: Iterable[bigquery.table.Row], limit: int = 3) -> None:
    for idx, row in enumerate(rows):
        if idx >= limit:
            print("  ...")
            break
        print(f"  {dict(row)}")


async def run_query(client: bigquery.Client, name: str, sql: str) -> None:
    print(f"\n=== {name} ===")
    job = await asyncio.to_thread(client.query, _format(sql))
    rows = await asyncio.to_thread(job.result)
    _print_rows(rows)


async def main() -> None:
    client = bigquery.Client()
    for name, sql in QUERIES.items():
        await run_query(client, name, sql)


if __name__ == "__main__":
    asyncio.run(main())
