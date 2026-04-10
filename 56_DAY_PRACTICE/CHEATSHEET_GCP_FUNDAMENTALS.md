# GCP Cloud Fundamentals Cheatsheet
## Days 8-10 | Quick Reference for Interview Recall

---

## DAY 8: GCP Basics + First Cloud Deployment

### GCP Hierarchy
```
Organization
  └── Folder (optional)
       └── Project (billing, IAM, resources)
            ├── Region (e.g. us-central1)
            │    └── Zone (e.g. us-central1-a)
            ├── Services (BigQuery, Cloud Run, GCS, Vertex AI)
            └── IAM Policies
```

### Key GCP Services for AI/ML
| Service | Purpose | AI/ML Use |
|---------|---------|-----------|
| Vertex AI | ML platform | Train, deploy, call LLMs (Gemini) |
| Cloud Run | Serverless containers | Host FastAPI + ML inference |
| BigQuery | Data warehouse | Store/query embeddings, analytics |
| Cloud Storage (GCS) | Object storage | Training data, model artifacts |
| IAM | Access control | Service accounts, WIF |
| Cloud Build | CI/CD | Auto-deploy on git push |

### gcloud CLI Essentials
```bash
# Setup
gcloud auth login
gcloud config set project MY_PROJECT

# Cloud Run
gcloud run deploy --source .
gcloud run services list

# General
gcloud services enable run.googleapis.com
gcloud services list --enabled
```

### Dockerfile for Cloud Run
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Interview Sound Bite
"I deploy FastAPI services to Cloud Run using container images. Cloud Run auto-scales and charges per request."

---

## DAY 9: GCP Console + IAM

### IAM Core Concepts
```
WHO (Identity)  ──can do──>  WHAT (Role)  ──on──>  WHICH (Resource)
   │                              │                        │
   ├── Google Account             ├── roles/owner          ├── project
   ├── Service Account            ├── roles/editor         ├── dataset
   └── WIF (external)             └── roles/viewer         └── bucket
```

### Service Account Pattern
```bash
# Create
gcloud iam service-accounts create my-app \
    --display-name="My App SA"

# Grant role
gcloud projects add-iam-policy-binding MY_PROJECT \
    --member="serviceAccount:my-app@PROJECT.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataViewer"

# Use in Cloud Run
gcloud run deploy my-service \
    --service-account=my-app@PROJECT.iam.gserviceaccount.com
```

### Least Privilege Principle
| Need | Grant This Role | NOT This |
|------|----------------|----------|
| Read BigQuery | `roles/bigquery.dataViewer` | `roles/owner` |
| Write GCS | `roles/storage.objectCreator` | `roles/storage.admin` |
| Call Vertex AI | `roles/aiplatform.user` | `roles/editor` |
| Deploy Cloud Run | `roles/run.developer` | `roles/owner` |

### WIF (Workload Identity Federation)
- OLD way: Download service account JSON key (security risk!)
- NEW way: Configure WIF trust relationship (no keys!)
- Use case: GitHub Actions → GCP without stored credentials

### GCP Console Navigation (Day 9 Practice)
```
console.cloud.google.com
  → Search bar (press / to focus)
  → Navigation menu (top-left hamburger)
  → IAM & Admin → IAM (see all bindings)
  → Cloud Run (see deployments)
  → BigQuery (query editor)
  → Cloud Storage (buckets)
```

---

## DAY 10: Cloud Storage + FastAPI + Gemini Deployment

### GCS Bucket Operations
```python
from google.cloud import storage

client = storage.Client()
bucket = client.bucket("my-bucket-name")

# Upload
blob = bucket.blob("data/file.csv")
blob.upload_from_string("content")

# Download
content = blob.download_as_text()

# List
for blob in bucket.list_blobs(prefix="data/"):
    print(blob.name)
```

### Bucket vs Object
```
Bucket: Container (globally unique name)
  └── Object: File (identified by full path/name)
       ├── Can be up to 5TB
       ├── Immutable (overwrite, don't edit)
       └── "Folders" are just name prefixes (data/file.csv)
```

### Storage Classes
| Class | Use Case | Cost |
|-------|----------|------|
| Standard | Hot data, serving | Higher |
| Nearline | Access ~1x/month | Medium |
| Coldline | Access ~1x/year | Lower |
| Archive | Rare access | Lowest |

### FastAPI + Vertex AI Deployment (Day 10 Main App)
```python
# The actual pattern deployed to Cloud Run
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import google.genai as genai

app = FastAPI()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    model: str = Field(default="gemini-2.0-flash-001")

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=req.model,
            contents=req.message
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
```

### Deployed Endpoints (Day 10 App)
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/chat` | POST | Chat with Gemini |
| `/generate` | POST | Generate text |
| `/healthz` | GET | Liveness probe |
| `/readyz` | GET | Readiness probe |
| `/config-summary` | GET | Safe config display |
| `/config-validate` | GET | Validate configuration |

### Cloud Run Deployment URL
```
https://hello-gemini-279141399436.us-central1.run.app
```

### Key Production Patterns Learned
1. **Retry logic**: `_generate_with_retry()` with exponential backoff
2. **Middleware**: Request timing, logging
3. **Error mapping**: Vertex AI errors → HTTP status codes
4. **Health checks**: Separate liveness (`/healthz`) and readiness (`/readyz`)
5. **Config validation**: Verify env vars at startup, not at request time

---

## GCP COST AWARENESS (Zero-Cost Study)

| Free Tier | Limit |
|-----------|-------|
| Cloud Run | 2M requests/month |
| BigQuery | 1 TB queries/month |
| GCS | 5 GB storage |
| Vertex AI | Gemini Flash has free quota |

**Interview tip**: "I designed my services to work within free tiers during development, with clear cost boundaries for production."

---

## QUICK REFERENCE TABLE

| Day | Topic | One Pattern to Remember |
|-----|-------|------------------------|
| 8 | GCP Basics | Project → Region → Zone → Service |
| 9 | IAM | Least privilege: grant minimum role on specific resource |
| 10 | Cloud Run + Gemini | FastAPI + Dockerfile → `gcloud run deploy` |

---

## COMMON INTERVIEW TRAPS (Days 8-10)

1. "What is the difference between Cloud Run and Cloud Functions?" — Run = container, Functions = single-function
2. "Why not use service account keys?" — Security risk; use WIF or attached service accounts
3. "How does Cloud Run scale?" — 0 to N instances based on concurrent requests
4. "What is the difference between a region and a zone?" — Region = geographic area, Zone = specific data center
5. "How do you reduce latency?" — Deploy to region closest to users, use caching, optimize cold starts

---

*From actual repo code | Days 8-10 | April 2026 Revision*
