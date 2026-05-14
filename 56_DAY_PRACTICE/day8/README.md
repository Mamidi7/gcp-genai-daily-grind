# Day 8: Flask + Docker + Cloud Run

## Mission
Build a Flask web app, package it in a Docker container, and deploy to Cloud Run.

## Topics Covered

| Concept | What it does |
|---------|-------------|
| Flask routing | `@app.route()` maps URLs to functions |
| `jsonify()` | Returns proper JSON responses with Content-Type header |
| gunicorn | Production WSGI server (multi-threaded, unlike Flask dev server) |
| Docker layer caching | COPY requirements.txt before code to avoid reinstalling deps |
| `0.0.0.0` vs `127.0.0.1` | Cloud Run needs 0.0.0.0 to accept external connections |
| `PORT` env var | Cloud Run assigns a port dynamically — never hardcode it |
| Cloud Run source deploy | `gcloud run deploy --source .` — one command from code to live URL |

## Files

| File | Purpose |
|------|---------|
| `main.py` | Flask app with 3 endpoints (/, /health, /info) |
| `requirements.txt` | Flask + gunicorn + requests |
| `Dockerfile` | Multi-stage build, python:3.11-slim |
| `exercises.py` | 5 exercises + bonus |
| `solution.py` | Complete solutions |

## Quick Start

```bash
# 1. Run locally
cd day8
uv run python main.py
# Open http://localhost:8080

# 2. Docker build & run
docker build -t flask-cloud-run .
docker run -p 8080:8080 flask-cloud-run

# 3. Deploy to Cloud Run
gcloud run deploy flask-app --source . --region us-central1 --allow-unauthenticated
```

## Request Flow

```
Browser → Cloud Run proxy → gunicorn → Flask router → handler → JSON response
```

## Interview Punch (30s)

> "I built a Flask API with 3 endpoints, containerized it with Docker using a multi-stage build to keep the image small (python:3.11-slim), and deployed it to Cloud Run with a single gcloud command. The /health endpoint is used by Cloud Run's load balancer for instance health checks — if it returns non-200, the instance is restarted."

## Key Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Using `127.0.0.1` instead of `0.0.0.0` | Cloud Run proxy connects externally |
| Hardcoding `PORT=5000` | Use `os.getenv("PORT", 8080)` |
| Returning a plain dict from route | Use `jsonify()` to get proper Response object |
| Copying all files before pip install | Copy requirements.txt first for Docker layer caching |
| Using Flask dev server in production | Use gunicorn for concurrent request handling |
