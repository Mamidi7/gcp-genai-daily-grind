# Day 8 Notes: Flask + Docker + Cloud Run

## Key Takeaways

1. **Flask routing** — `@app.route("/path")` maps URL to function. Return value becomes HTTP response.
2. **jsonify()** — Wraps dict into Flask Response with correct Content-Type: application/json
3. **Gunicorn vs dev server** — Flask's built-in server is single-threaded. gunicorn handles concurrent requests.
4. **Docker layer caching** — Order your COPY commands so requirements.txt is copied BEFORE code. pip install only re-runs when requirements.txt changes.
5. **PORT is dynamic** — Cloud Run sets PORT env var. Never hardcode port numbers. Use `os.getenv("PORT", 8080)`.
6. **0.0.0.0** — Binds to all interfaces. Required for Cloud Run. `127.0.0.1` only allows localhost connections.
7. **Source deploy** — `gcloud run deploy --source .` is the quickest path: it uploads code, triggers Cloud Build, pushes to Artifact Registry, and deploys.

## Key Commands

```bash
# Local dev
uv run python main.py

# Docker
docker build -t flask-cloud-run .
docker run -p 8080:8080 flask-cloud-run

# Cloud Run
gcloud run deploy flask-app --source . --region us-central1 --allow-unauthenticated

# Test deployment
curl https://flask-app-xxxxx-uc.a.run.app/health
```

## Interview Answers

### 30s Pitch
> "Built a Flask API with health checks, containerized with Docker (python:3.11-slim multi-stage build), and deployed to Cloud Run via source deployment. Used gunicorn for production concurrency and PORT env var binding for Cloud Run compatibility."

### 90s STAR
> **S:** Needed a lightweight API service deployable on Cloud Run.
> **T:** Had to handle health checks, serve metadata, and be production-ready (concurrent requests, proper containerization).
> **A:** Built Flask app with jsonify() for structured JSON. Added gunicorn for concurrency. Dockerfile uses multi-stage build with layer caching (120MB image). Deployed with gcloud run deploy --source.
> **R:** All 3 endpoints responding at .run.app URL. Build is fully automated — one command from code to live.
> **I:** Source-based deployment abstracts away Cloud Build and Artifact Registry — ideal for quick prototyping.

## Tomorrow: Cloud Storage (GCS) or move to Day 9-10
