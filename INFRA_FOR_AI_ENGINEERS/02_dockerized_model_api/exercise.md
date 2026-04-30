# Exercise 2: Dockerized Model API

## Goal (one line)
Put your model serving API in a Docker container with proper health checks, networking, and volume mounts.

## Why This Matters
Interviewers ask: "How do you deploy a model?"
If you say "I run python app.py" — junior answer.
If you say "I containerize with Docker, add HEALTHCHECK, expose metrics port,
mount config from volume" — senior answer.

## Concept (3-6 lines)
1. Docker wraps your app + all dependencies into one immutable image
2. HEALTHCHECK instruction lets Docker know if your app is alive
3. Volumes let you inject config (model params, API keys) without rebuilding
4. Multi-stage builds keep images small (builder stage → runtime stage)
5. .dockerignore prevents leaking secrets or bloating the image
6. The container should start in < 5 seconds and respond to /healthz

## Architecture

```
┌─────────────────────────────────────┐
│  Docker Container                   │
│                                     │
│  ┌───────────────┐  Port 8000 ──→  │ ← Client hits this
│  │  FastAPI App   │                  │
│  │  (uvicorn)     │                  │
│  └───────┬───────┘                  │
│          │                          │
│  ┌───────▼───────┐                  │
│  │  Model Call    │                  │
│  │  (stub/Gemini) │                  │
│  └───────────────┘                  │
│                                     │
│  Volume: /app/config  ←── config/  │ ← Mount YAML config here
│                                     │
│  HEALTHCHECK: GET /healthz every 30s│
└─────────────────────────────────────┘
```

## What You Build

### 1. Dockerfile (multi-stage)
- Stage 1 (builder): install Python deps
- Stage 2 (runtime): copy app only, slim image
- HEALTHCHECK curl to /healthz
- Non-root user for security

### 2. .dockerignore
- Exclude .git, __pycache__, .env, tests

### 3. config/config.yaml (mounted as volume)
- Model name, max_tokens default, log level
- App reads this at startup

### 4. docker-compose.yml (optional, for Exercise 4+)
- Brings up the API + Redis together

## Common Mistake + Fix

Mistake: Running as root inside the container.
  Why bad: Security vulnerability — if container is compromised, attacker has root.
  Fix: Create a non-root user and switch to it.

```dockerfile
# WRONG
FROM python:3.13
COPY . /app
CMD ["python", "app.py"]

# RIGHT
FROM python:3.13-slim AS runtime
RUN useradd -m appuser
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
USER appuser
HEALTHCHECK --interval=30s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')"
CMD ["uvicorn", "solution.model_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Check Question
Why multi-stage build? What happens if you don't use it?
(Hint: check image size with `docker images` — compare multi-stage vs single-stage.)

## Tiny Exercise
1. Build: `docker build -t model-api:v1 .`
2. Run: `docker run -p 8000:8000 model-api:v1`
3. Test: `curl http://localhost:8000/healthz`
4. Test: `curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"prompt":"hello"}'`
5. Write the docker build output in debug_journal.md
