# Day 8 — Flask → Cloud Run: CLI Commands Reference

> Manual-first learning. Run each block only after understanding what it does.
> Block by block — no magic.

---

## Block 1: Local Development

```bash
# Install Flask
pip install flask

# Run the app
python main.py

# Test endpoints (separate terminal)
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/info
```

---

## Block 2: Docker — Build & Run Locally

```bash
# Build Docker image from Dockerfile
# (Don't forget the dot at the end — it means "use this folder")
docker build -t flask-cloud-run .

# Run the container
# -p 8080:8080 = map host port 8080 to container port 8080
docker run -p 8080:8080 flask-cloud-run

# Test in another terminal
curl http://localhost:8080/health
```

---

## Block 3: Push to Google Artifact Registry

```bash
# Step 1: Tag local image for Google's registry
# Format: REGION-docker.pkg.dev/PROJECT-ID/REPO-NAME/IMAGE:TAG
docker tag flask-cloud-run us-central1-docker.pkg.dev/gcp-ai-etl/flask-app/flask-app:v1

# Step 2: Authenticate Docker to use Google's registry
gcloud auth configure-docker us-central1-docker.pkg.dev

# Step 3: Create the repository (one-time setup)
gcloud artifacts repositories create flask-app \
  --repository-format=docker \
  --location=us-central1 \
  --project=gcp-ai-etl

# Step 4: Push the image
docker push us-central1-docker.pkg.dev/gcp-ai-etl/flask-app/flask-app:v1
```

---

## Block 4: Deploy to Cloud Run

```bash
# Option A: Deploy from Artifact Registry image
gcloud run deploy flask-app \
  --image us-central1-docker.pkg.dev/gcp-ai-etl/flask-app/flask-app:v1 \
  --region us-central1 \
  --allow-unauthenticated

# Option B: Deploy directly from source (Cloud Build + deploy in one step)
gcloud run deploy flask-app \
  --source . \
  --region us-central1 \
  --allow-unauthenticated

# After deploy — Cloud Run gives you a URL like:
# https://flask-app-xxxxx-uc.a.run.app
```

---

## Block 5: Verify & Test

```bash
# Test the live Cloud Run URL
curl https://YOUR_CLOUD_RUN_URL/health
curl https://YOUR_CLOUD_RUN_URL/
curl https://YOUR_CLOUD_RUN_URL/info

# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=flask-app" --limit 10

# List revisions
gcloud run revisions list --service=flask-app --region=us-central1
```

---

## Key Concepts (Why Not Magic)

| Concept | Why |
|---------|-----|
| `0.0.0.0` instead of `127.0.0.1` | Listen on all interfaces — needed inside containers |
| `PORT` env var instead of hardcoded port | Cloud Run assigns port dynamically |
| gunicorn instead of Flask dev server | Multi-threaded — handles concurrent requests |
| Docker multi-stage build | Smaller final image (no build tools/pip cache) |
| `--allow-unauthenticated` | Makes the service publicly accessible via URL |
| Artifact Registry vs Container Registry | Artifact Registry is the newer, recommended GCP service |

## Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `docker build` requires 1 argument | Add the dot: `docker build -t name .` |
| `docker.sock: connect: no such file or directory` | Start Orbstack/Docker Desktop |
| `Permission denied` on deploy | `gcloud auth login` and `gcloud config set project gcp-ai-etl` |
| `Image not found` | Tag and push the image first with correct name |
