# ── Stage 1: Builder ──────────────────────────────────────────────
FROM python:3.13-slim AS builder

WORKDIR /build

# Install deps first (cached layer — only rebuilds when requirements change)
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# ── Stage 2: Runtime ─────────────────────────────────────────────
FROM python:3.13-slim AS runtime

# Security: non-root user
RUN useradd -m -s /bin/bash appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY solution/ ./solution/

# Switch to non-root user
USER appuser

# Expose the API port
EXPOSE 8000

# Health check — if /healthz fails 3 times, Docker marks container unhealthy
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')" || exit 1

# Start the server
CMD ["uvicorn", "solution.model_api:app", "--host", "0.0.0.0", "--port", "8000"]
