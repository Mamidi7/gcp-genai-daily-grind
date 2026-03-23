-- Day 10 SQL / BigQuery Practice (Public Data, Minimal Prep)
-- Date: 2026-03-20
--
-- Goal:
-- Practice window functions on real BigQuery public datasets with low setup.
--
-- Cost safety tips:
-- 1) In BigQuery UI, turn on "Query settings -> Maximum bytes billed".
-- 2) Run one query at a time.
-- 3) Keep filters (date range/state list) as written.
--
-- Datasets used:
-- A) `bigquery-public-data.thelook_ecommerce.order_items` (business-style practice)
-- B) `bigquery-public-data.samples.natality` (time-series practice)

-- ============================================================
-- SECTION A: TheLook Ecommerce dataset (practical + interview-friendly)
-- Table:
-- `bigquery-public-data.thelook_ecommerce.order_items`
-- Common columns used:
-- order_id INT64, user_id INT64, product_id INT64,
-- status STRING, created_at TIMESTAMP, sale_price FLOAT64
--
-- Filtered to Q1 2022 for lower scan + easier output.
-- ============================================================

-- Q1) Latest order item per user (ROW_NUMBER)
SELECT
  user_id,
  order_id,
  created_at,
  sale_price,
  status,
  ROW_NUMBER() OVER (
    PARTITION BY user_id
    ORDER BY created_at DESC
  ) AS row_num
FROM `bigquery-public-data.thelook_ecommerce.order_items`
WHERE DATE(created_at) BETWEEN '2022-01-01' AND '2022-03-31'
QUALIFY row_num <= 5
ORDER BY user_id, row_num;

-- Q2) Rank users by total spend (RANK)
WITH user_spend AS (
  SELECT
    user_id,
    SUM(sale_price) AS total_spend
  FROM `bigquery-public-data.thelook_ecommerce.order_items`
  WHERE DATE(created_at) BETWEEN '2022-01-01' AND '2022-03-31'
  GROUP BY user_id
)
SELECT
  user_id,
  ROUND(total_spend, 2) AS total_spend,
  RANK() OVER (ORDER BY total_spend DESC) AS spend_rank
FROM user_spend
ORDER BY spend_rank, user_id
LIMIT 100;

-- Q3) Compare RANK vs DENSE_RANK on daily revenue
WITH daily_revenue AS (
  SELECT
    DATE(created_at) AS order_date,
    SUM(sale_price) AS revenue
  FROM `bigquery-public-data.thelook_ecommerce.order_items`
  WHERE DATE(created_at) BETWEEN '2022-01-01' AND '2022-03-31'
  GROUP BY order_date
)
SELECT
  order_date,
  ROUND(revenue, 2) AS revenue,
  RANK() OVER (ORDER BY revenue DESC) AS revenue_rank,
  DENSE_RANK() OVER (ORDER BY revenue DESC) AS revenue_dense_rank
FROM daily_revenue
ORDER BY revenue DESC, order_date
LIMIT 60;

-- Q4) Previous day revenue (LAG)
WITH daily_revenue AS (
  SELECT
    DATE(created_at) AS order_date,
    SUM(sale_price) AS revenue
  FROM `bigquery-public-data.thelook_ecommerce.order_items`
  WHERE DATE(created_at) BETWEEN '2022-01-01' AND '2022-03-31'
  GROUP BY order_date
)
SELECT
  order_date,
  ROUND(revenue, 2) AS revenue,
  ROUND(LAG(revenue) OVER (ORDER BY order_date), 2) AS previous_day_revenue,
  ROUND(revenue - LAG(revenue) OVER (ORDER BY order_date), 2) AS delta_vs_previous_day
FROM daily_revenue
ORDER BY order_date;

-- Q5) Next order date for repeat users (LEAD)
SELECT
  user_id,
  order_id,
  DATE(created_at) AS order_date,
  LEAD(DATE(created_at)) OVER (
    PARTITION BY user_id
    ORDER BY created_at
  ) AS next_order_date
FROM `bigquery-public-data.thelook_ecommerce.order_items`
WHERE DATE(created_at) BETWEEN '2022-01-01' AND '2022-03-31'
QUALIFY COUNT(*) OVER (PARTITION BY user_id) >= 3
ORDER BY user_id, order_date
LIMIT 120;

-- Q6) Most common order status per month (ROW_NUMBER over grouped results)
WITH monthly_status AS (
  SELECT
    FORMAT_DATE('%Y-%m', DATE(created_at)) AS month_key,
    status,
    COUNT(*) AS status_count
  FROM `bigquery-public-data.thelook_ecommerce.order_items`
  WHERE DATE(created_at) BETWEEN '2022-01-01' AND '2022-03-31'
  GROUP BY month_key, status
),
ranked_status AS (
  SELECT
    month_key,
    status,
    status_count,
    ROW_NUMBER() OVER (
      PARTITION BY month_key
      ORDER BY status_count DESC
    ) AS row_num
  FROM monthly_status
)
SELECT
  month_key,
  status,
  status_count
FROM ranked_status
WHERE row_num = 1
ORDER BY month_key;

-- ============================================================
-- SECTION B: Natality dataset (real analytics style)
-- Table:
-- `bigquery-public-data.samples.natality`
-- Core columns used:
-- year INT64, month INT64, state STRING, weight_pounds FLOAT64
-- ============================================================

-- Q7) Year-over-year births by state (LAG)
WITH yearly_births AS (
  SELECT
    state,
    year,
    COUNT(1) AS births
  FROM `bigquery-public-data.samples.natality`
  WHERE year BETWEEN 2010 AND 2015
    AND state IN ('CA', 'TX', 'NY', 'FL')
  GROUP BY state, year
)
SELECT
  state,
  year,
  births,
  LAG(births) OVER (
    PARTITION BY state
    ORDER BY year
  ) AS previous_year_births,
  births - LAG(births) OVER (
    PARTITION BY state
    ORDER BY year
  ) AS delta_births
FROM yearly_births
ORDER BY state, year;

-- Q8) Rank states by average birth weight per year (DENSE_RANK)
WITH avg_weight_by_state AS (
  SELECT
    year,
    state,
    AVG(weight_pounds) AS avg_weight_pounds
  FROM `bigquery-public-data.samples.natality`
  WHERE year BETWEEN 2010 AND 2015
    AND state IN ('CA', 'TX', 'NY', 'FL')
    AND weight_pounds IS NOT NULL
  GROUP BY year, state
)
SELECT
  year,
  state,
  ROUND(avg_weight_pounds, 2) AS avg_weight_pounds,
  DENSE_RANK() OVER (
    PARTITION BY year
    ORDER BY avg_weight_pounds DESC
  ) AS weight_rank
FROM avg_weight_by_state
ORDER BY year, weight_rank, state;

-- ============================================================
-- Interview drill questions (answer after running queries):
-- 1) Why use PARTITION BY user_id or state?
-- 2) Why QUALIFY row_num <= 5 is useful?
-- 3) RANK vs DENSE_RANK difference in one line?
-- 4) What business question does LAG answer?
-- ============================================================
