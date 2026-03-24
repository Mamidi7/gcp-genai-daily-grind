"""
core/analyzer.py — Pure health analysis logic. No UI imports.
This is the ESSENTIAL code: takes raw data, applies rules, returns structured results.
"""
from .models import EndpointHealth, HealthSummary, HealthStatus, SLAThresholds


def determine_status(
    latency_ms: float,
    error_rate: float,
    thresholds: SLAThresholds
) -> HealthStatus:
    """
    Core rule engine — determines health status from metrics.

    ESSENTIAL CONCEPT: This is the same pattern GCP uses:
    - Define thresholds
    - Compare metrics against thresholds
    - Return status enum

    Interview tip: Explain this as "threshold-based alerting logic"
    """
    if latency_ms > 1000 or error_rate > 3.0:
        return HealthStatus.CRITICAL
    elif latency_ms > thresholds.latency_ms or error_rate > thresholds.error_rate:
        return HealthStatus.DEGRADED
    return HealthStatus.HEALTHY


def categorize_endpoints(
    endpoints: list[EndpointHealth],
    thresholds: SLAThresholds
) -> tuple[list[EndpointHealth], list[EndpointHealth], list[EndpointHealth]]:
    """
    Split endpoints into healthy/degraded/critical buckets.
    Pure transformation — no side effects, no UI.
    """
    healthy, degraded, critical = [], [], []

    for endpoint in endpoints:
        status = determine_status(endpoint.latency_ms, endpoint.error_rate, thresholds)
        if status == HealthStatus.HEALTHY:
            healthy.append(endpoint)
        elif status == HealthStatus.DEGRADED:
            degraded.append(endpoint)
        else:
            critical.append(endpoint)

    return healthy, degraded, critical


def compute_summary(
    endpoints: list[EndpointHealth],
    thresholds: SLAThresholds | None = None
) -> HealthSummary:
    """
    Main aggregation function — what your FastAPI /health endpoint calls.

    Takes raw endpoint data → applies rules → returns summary.
    This is the CORE of your health check API.
    """
    if thresholds is None:
        thresholds = SLAThresholds()

    if not endpoints:
        return HealthSummary(
            total_endpoints=0,
            healthy_count=0,
            degraded_count=0,
            critical_count=0,
            total_requests=0,
            avg_latency_ms=0.0,
            avg_error_rate=0.0,
            overall_status=HealthStatus.HEALTHY,
            endpoints=[]
        )

    healthy, degraded, critical = categorize_endpoints(endpoints, thresholds)

    total_requests = sum(e.requests for e in endpoints)
    avg_latency = sum(e.latency_ms for e in endpoints) / len(endpoints)
    avg_error = sum(e.error_rate for e in endpoints) / len(endpoints)

    # Overall status is worst of any endpoint
    if critical:
        overall = HealthStatus.CRITICAL
    elif degraded:
        overall = HealthStatus.DEGRADED
    else:
        overall = HealthStatus.HEALTHY

    return HealthSummary(
        total_endpoints=len(endpoints),
        healthy_count=len(healthy),
        degraded_count=len(degraded),
        critical_count=len(critical),
        total_requests=total_requests,
        avg_latency_ms=round(avg_latency, 1),
        avg_error_rate=round(avg_error, 2),
        overall_status=overall,
        endpoints=endpoints
    )


def get_recommendations(summary: HealthSummary) -> list[str]:
    """
    Generate actionable recommendations based on health summary.
    Pure logic — returns list of strings, no UI.
    """
    recs = []

    for endpoint in summary.endpoints:
        if endpoint.latency_ms > 1000:
            recs.append(
                f"{endpoint.endpoint}: P99 latency exceeds 1s — "
                "consider scaling GPU capacity or adding caching"
            )
        if endpoint.error_rate > 3.0:
            recs.append(
                f"{endpoint.region}: Error rate at {endpoint.error_rate}% — "
                "check firewall rules, quota limits, and upstream dependencies"
            )
        elif endpoint.error_rate > 1.0:
            recs.append(
                f"{endpoint.endpoint}: Error rate at {endpoint.error_rate}% — "
                "monitor closely, set up Cloud Monitoring alerts"
            )

    if summary.avg_latency_ms > 500:
        recs.append(
            f"System average latency ({summary.avg_latency_ms}ms) exceeds SLA — "
            "review慢 endpoints and consider horizontal scaling"
        )

    if not recs:
        recs.append("All endpoints within SLA — continue monitoring")

    return recs
