# Exercise 4: LLM Observability Stack

## Goal (one line)
Add Prometheus metrics + Grafana dashboard to your model API so you can see latency, token usage, error rate, and request volume in real-time.

## Why This Matters
Interview question: "Your model API is slow. How do you debug it?"
Bad: "I check the logs."
Good: "I look at the p99 latency graph in Grafana, filter by endpoint, check if it's
the model call or our processing, and see if it correlates with token usage spikes."

## Concept
1. Prometheus collects metrics from your app (pull model — it scrapes /metrics)
2. Your app exposes /metrics endpoint with custom counters and histograms
3. Grafana visualizes those metrics with dashboards
4. For AI: the key metrics are latency_ms, tokens_per_request, error_rate, model_version
5. Alerting: if p99 > 2s or error_rate > 5%, trigger an alert

## Architecture

```
┌──────────┐  scrape /metrics   ┌─────────────┐
│ FastAPI   │ ◄──────────────── │ Prometheus   │
│ + /metrics│                    │  :9090       │
└──────────┘                     └──────┬──────┘
                                        │ query
                                 ┌──────▼──────┐
                                 │ Grafana      │
                                 │  :3000       │
                                 │              │
                                 │ Dashboard:   │
                                 │ - req/sec    │
                                 │ - p50/p99    │
                                 │ - tokens     │
                                 │ - error rate │
                                 └──────────────┘
```

## What You Build

### 1. Add /metrics to model_api.py
```python
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('chat_requests_total', 'Total chat requests', ['status'])
REQUEST_LATENCY = Histogram('chat_request_latency_seconds', 'Request latency')
TOKENS_USED = Counter('tokens_used_total', 'Total tokens consumed')

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type="text/plain")
```

### 2. docker-compose.yml
- model-api (your app)
- prometheus (scrapes model-api/metrics)
- grafana (queries prometheus)

### 3. Grafana dashboard JSON
- Pre-configured with 4 panels: latency, throughput, tokens, errors

## Common Mistake
Forgetting to label metrics with model version. When you swap models,
you can't tell which model's latency you're looking at.
Fix: add `model_version` label to every metric.

## Check Question
What's the difference between a Counter and a Histogram in Prometheus?
(Counter only goes up. Histogram tracks distribution — p50, p95, p99.)

## Tiny Exercise
1. `docker-compose up` (in solution/)
2. Open Grafana at http://localhost:3000 (admin/admin)
3. Hit the API a few times: `for i in $(seq 1 20); do curl -s -X POST localhost:8000/chat -H 'Content-Type: application/json' -d '{"prompt":"hello '$i'"}'; done`
4. Watch the dashboard update in real-time
5. Screenshot the dashboard for your portfolio
