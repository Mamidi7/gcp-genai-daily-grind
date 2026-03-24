# Interview Pack - BigQuery Timeout in Python AI Wrapper

## Problem Context
A FastAPI service receives customer questions, fetches order data from BigQuery, and sends context to an LLM. Under load, BigQuery queries can exceed timeout limits and degrade API reliability.

## Data Flow (Input -> Process -> Output)
Input: `customer_id`, question text.
Process: FastAPI -> query builder -> BigQuery client call -> post-process rows -> LLM response composer.
Output: JSON answer with last 5 orders summary.

## Failure Mode and Recovery
Failure mode:
BigQuery call exceeds timeout or returns deadline exceeded.

Recovery strategy:
Set client timeout, retries with bounded backoff, fallback response with partial context, and clear HTTP mapping (`504` for upstream timeout).

## 30-Second Answer
I treat BigQuery as an upstream dependency. I set explicit timeout and retry policy, catch deadline exceptions, and return deterministic API responses. If query still fails, I send a safe fallback message and log trace IDs for replay.

## 90-Second STAR

Situation:
My AI API depended on BigQuery for customer order context, and occasional timeouts made responses unreliable.
Task:
Make the wrapper resilient so the API does not crash and users get predictable behavior.
Action:
I implemented timeout controls at the query layer, exponential backoff with max attempts, and exception mapping in FastAPI. I also added structured logs with request IDs and separated transient vs non-transient errors.
Result:
Timeouts no longer crashed the service. Failures became observable, retries recovered transient issues, and unresolved cases returned consistent `504` responses with traceable logs.

## 3-Minute Technical Walkthrough
I split reliability into four layers:

1. Validation layer:
Pydantic validates input before query execution, preventing wasted BigQuery calls on bad requests.

2. Query layer:
I enforce timeout per query and use bounded retries only for transient errors. Retry policy is capped to avoid runaway latency.

3. API layer:
FastAPI exception handling maps upstream timeout to `504` and quota/backpressure to `429` where appropriate.

4. Observability layer:
Every request gets a trace/request ID. Logs capture query duration, retry count, and final outcome so I can debug incidents quickly.

Design tradeoff:
Higher timeout can reduce false failures but increases tail latency. I keep a moderate timeout and rely on retries plus fallback to protect user experience.

## Follow-up Questions I Should Expect

1. How do you decide retryable vs non-retryable BigQuery errors?
2. What timeout value did you choose and why?
3. How do you prevent duplicate effects if retries are triggered?
4. What metrics prove reliability improved after the fix?
5. How would you handle a BigQuery timeout in your Python AI wrapper?
