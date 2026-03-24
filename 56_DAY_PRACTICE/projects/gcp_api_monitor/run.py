#!/usr/bin/env python3
"""
run.py — Unified entry point. Shows how core/ and dashboard/ stay separate.

ARCHITECTURE:
  run.py (this file)
    ├── calls core/analyzer.py  → pure logic, no UI
    └── calls dashboard/       → rich UI, imports from core/

Interviewers will ask: "how does your dashboard connect to your API?"
Answer: "The dashboard layer imports core models, the FastAPI app returns
        core models via HTTP, and the dashboard renders them beautifully."
"""
import sys
sys.path.insert(0, "/tmp/gcp_api_monitor")

from core.models import EndpointHealth
from core.analyzer import compute_summary, get_recommendations
from dashboard.terminal import render_health_dashboard


# ─── Same sample data across all entry points ─────────────────────────────────
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


def main():
    print("=" * 70)
    print("OPTION 1: Raw JSON (what you get WITHOUT dashboard)")
    print("=" * 70)

    # This is what your FastAPI /health endpoint returns
    summary = compute_summary(SAMPLE_ENDPOINTS)
    import json
    print(summary.model_dump_json(indent=2))

    print()
    print("=" * 70)
    print("OPTION 2: Beautiful Dashboard (what dashboard/ adds)")
    print("=" * 70)

    # This is what dashboard/ adds on top
    render_health_dashboard(SAMPLE_ENDPOINTS)

    print()
    print("=" * 70)
    print("KEY INSIGHT: Same compute_summary() call, two completely different outputs")
    print("  • core/analyzer.py  → pure logic, returns HealthSummary (API/Web use)")
    print("  • dashboard/        → rich rendering, ONLY calls core/, no changes to core/")
    print("=" * 70)


if __name__ == "__main__":
    main()
