# ---- Build stage ----
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Runtime stage ----
FROM python:3.11-slim

WORKDIR /app

# Copy only what's needed from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY main.py .

# Cloud Run provides PORT env var (default 8080)
ENV PORT=8080

# Run with gunicorn for production concurrency
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
