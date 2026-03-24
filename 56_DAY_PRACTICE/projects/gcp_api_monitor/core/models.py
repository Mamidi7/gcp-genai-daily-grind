"""
core/models.py — Pure data models. No UI dependencies.
These are the essential Pydantic models you MUST know for FastAPI/GCP work.
"""
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import Optional


class HealthStatus(str, Enum):
    """Three states — same pattern GCP Cloud Monitoring uses."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"


class EndpointHealth(BaseModel):
    """
    Core model for a single endpoint health record.
    This is what FastAPI returns from health check endpoints.
    """
    endpoint: str = Field(..., description="API endpoint path")
    region: str = Field(..., description="GCP region")
    latency_ms: float = Field(..., ge=0, description="Response time in milliseconds")
    error_rate: float = Field(..., ge=0, le=100, description="Error rate as percentage")
    requests: int = Field(..., ge=0, description="Total request count")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"str_strip_whitespace": True}


class SLAThresholds(BaseModel):
    """
    Configurable SLA thresholds — defines what "healthy" means.
    Adjust these based on your GCP SLA requirements.
    """
    latency_ms: float = Field(default=500.0, gt=0)
    error_rate: float = Field(default=1.0, ge=0, le=100)


class HealthSummary(BaseModel):
    """
    Aggregated health summary — computed from list of EndpointHealth.
    This is what your FastAPI endpoint would return.
    """
    total_endpoints: int
    healthy_count: int
    degraded_count: int
    critical_count: int
    total_requests: int
    avg_latency_ms: float
    avg_error_rate: float
    overall_status: HealthStatus
    endpoints: list[EndpointHealth]
