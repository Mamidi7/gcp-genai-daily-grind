"""
app/main.py — FastAPI application. This is your CORE web framework skill.
This is ESSENTIAL interview material — FastAPI routing, dependencies, response models.
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional

import sys
sys.path.insert(0, "/tmp/gcp_api_monitor")

from core.models import EndpointHealth, HealthSummary, SLAThresholds
from core.analyzer import compute_summary, get_recommendations

app = FastAPI(
    title="GCP API Health Monitor",
    version="1.0.0",
    description="Production-style health check API — same pattern used in real GCP deployments"
)

# ─── Sample data (in production, this comes from Cloud Monitoring / Synthetics) ───
SAMPLE_ENDPOINTS = [
    EndpointHealth(endpoint="/v1/gemini/generate", region="us-central1",
                    latency_ms=245, error_rate=0.2, requests=15234),
    EndpointHealth(endpoint="/v1/text/embeddings", region="us-east1",
                    latency_ms=89, error_rate=0.1, requests=28456),
    EndpointHealth(endpoint="/v1/images/generate", region="europe-west1",
                    latency_ms=1203, error_rate=4.7, requests=4521),
    EndpointHealth(endpoint="/v1/audio/transcribe", region="asia-east1",
                    latency_ms=567, error_rate=1.2, requests=8923),
    EndpointHealth(endpoint="/v1/models/list", region="us-central1",
                    latency_ms=45, error_rate=0.0, requests=67890),
    EndpointHealth(endpoint="/v1/moderation/classify", region="us-east1",
                    latency_ms=312, error_rate=0.8, requests=12345),
]


@app.get("/", tags=["root"])
async def root():
    """Root endpoint — basic API info."""
    return {
        "name": "GCP API Health Monitor",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthSummary, tags=["health"])
async def get_health(thresholds: Optional[SLAThresholds] = None) -> HealthSummary:
    """
    Main health check endpoint.

    ESSENTIAL PATTERN: This is EXACTLY how production health checks work:
    1. Fetch metrics (from Cloud Monitoring, Datadog, etc.)
    2. Apply business logic (thresholds, aggregations)
    3. Return structured response

    Interview answer: "My /health endpoint aggregates endpoint metrics,
    applies SLA thresholds, and returns a HealthSummary with status + recommendations"
    """
    thresholds = thresholds or SLAThresholds()
    summary = compute_summary(SAMPLE_ENDPOINTS, thresholds)
    return summary


@app.get("/health/{endpoint_path}", tags=["health"])
async def get_endpoint_health(endpoint_path: str):
    """
    Get health for a specific endpoint.
    Returns 404 if endpoint not found.
    """
    for ep in SAMPLE_ENDPOINTS:
        if ep.endpoint == endpoint_path:
            summary = compute_summary([ep])
            return {
                **ep.model_dump(),
                "status": summary.overall_status.value,
                "recommendations": get_recommendations(summary)
            }
    raise HTTPException(status_code=404, detail=f"Endpoint '{endpoint_path}' not found")


@app.post("/recommendations", tags=["insights"])
async def get_recommendations_endpoint(thresholds: Optional[SLAThresholds] = None):
    """
    Get actionable recommendations for all endpoints.
    Pure insight layer — same compute_summary logic, just focused output.
    """
    thresholds = thresholds or SLAThresholds()
    summary = compute_summary(SAMPLE_ENDPOINTS, thresholds)
    recommendations = get_recommendations(summary)
    return {"recommendations": recommendations, "overall_status": summary.overall_status.value}


# ─── ESSENTIAL: These are the same patterns used in production FastAPI apps ───
# Interviewers will ask about: response_model, HTTPException, Query params, tags

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
