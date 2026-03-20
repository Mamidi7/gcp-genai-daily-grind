-- Day 10 SQL / BigQuery Track
-- Theme: analyze an applied AI backend using window functions
--
-- Imaginary table:
-- `project.dataset.request_events`
--
-- Columns:
-- request_id STRING
-- user_id STRING
-- event_ts TIMESTAMP
-- endpoint STRING
-- status_code INT64
-- latency_ms INT64
-- retries_used INT64
-- feedback STRING

-- ============================================================
-- Q1. Latest request per user
-- Why this matters:
-- in AI systems, you often want the most recent request from each user
-- ============================================================

SELECT *
FROM (
  SELECT
    request_id,
    user_id,
    event_ts,
    endpoint,
    status_code,
    latency_ms,
    ROW_NUMBER() OVER (
      PARTITION BY user_id
      ORDER BY event_ts DESC
    ) AS row_num
  FROM `project.dataset.request_events`
)
WHERE row_num = 1;

-- ============================================================
-- Q2. Rank the slowest requests
-- Why this matters:
-- helps identify bad latency outliers
-- ============================================================

SELECT
  request_id,
  user_id,
  endpoint,
  latency_ms,
  RANK() OVER (ORDER BY latency_ms DESC) AS latency_rank
FROM `project.dataset.request_events`;

-- ============================================================
-- Q3. Compare RANK vs DENSE_RANK on retries
-- Why this matters:
-- useful for understanding repeated retry patterns
-- ============================================================

SELECT
  request_id,
  retries_used,
  RANK() OVER (ORDER BY retries_used DESC) AS retry_rank,
  DENSE_RANK() OVER (ORDER BY retries_used DESC) AS retry_dense_rank
FROM `project.dataset.request_events`;

-- ============================================================
-- Q4. Previous request latency for each user
-- Why this matters:
-- lets you compare current performance with previous performance
-- ============================================================

SELECT
  user_id,
  event_ts,
  latency_ms,
  LAG(latency_ms) OVER (
    PARTITION BY user_id
    ORDER BY event_ts
  ) AS previous_latency_ms
FROM `project.dataset.request_events`
ORDER BY user_id, event_ts;

-- ============================================================
-- Q5. Next request timestamp for each user
-- Why this matters:
-- can help you analyze user activity gaps
-- ============================================================

SELECT
  user_id,
  event_ts,
  LEAD(event_ts) OVER (
    PARTITION BY user_id
    ORDER BY event_ts
  ) AS next_event_ts
FROM `project.dataset.request_events`
ORDER BY user_id, event_ts;

-- ============================================================
-- Q6. Most common failure status per endpoint
-- Step 1: aggregate counts
-- Step 2: rank within endpoint
-- ============================================================

WITH error_counts AS (
  SELECT
    endpoint,
    status_code,
    COUNT(*) AS error_count
  FROM `project.dataset.request_events`
  WHERE status_code >= 400
  GROUP BY endpoint, status_code
),
ranked_errors AS (
  SELECT
    endpoint,
    status_code,
    error_count,
    ROW_NUMBER() OVER (
      PARTITION BY endpoint
      ORDER BY error_count DESC
    ) AS row_num
  FROM error_counts
)
SELECT
  endpoint,
  status_code,
  error_count
FROM ranked_errors
WHERE row_num = 1;

-- ============================================================
-- Q7. Day-over-day latency trend
-- Why this matters:
-- basic production monitoring mindset
-- ============================================================

WITH daily_latency AS (
  SELECT
    DATE(event_ts) AS event_date,
    AVG(latency_ms) AS avg_latency_ms
  FROM `project.dataset.request_events`
  GROUP BY event_date
)
SELECT
  event_date,
  avg_latency_ms,
  LAG(avg_latency_ms) OVER (ORDER BY event_date) AS previous_day_latency,
  avg_latency_ms - LAG(avg_latency_ms) OVER (ORDER BY event_date) AS delta_latency
FROM daily_latency
ORDER BY event_date;

-- ============================================================
-- Q8. Feedback analysis with ranking
-- Why this matters:
-- helps identify which users or endpoints need attention
-- ============================================================

SELECT
  endpoint,
  feedback,
  COUNT(*) AS feedback_count,
  DENSE_RANK() OVER (
    PARTITION BY endpoint
    ORDER BY COUNT(*) DESC
  ) AS feedback_rank
FROM `project.dataset.request_events`
GROUP BY endpoint, feedback
ORDER BY endpoint, feedback_rank;

-- ============================================================
-- Interview check questions
-- 1. Why use PARTITION BY user_id?
-- 2. Why does ROW_NUMBER work for "latest per user"?
-- 3. When would you choose RANK over DENSE_RANK?
-- 4. Why is LAG useful in backend analytics?
-- ============================================================
