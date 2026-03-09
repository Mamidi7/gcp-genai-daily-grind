# ☁️ GCP Cheat Sheet — 10th Std Level

> GCP = Google Cloud Platform. Cloud computing! 😎

---

## 1. Cloud Run — Deploy Web Apps

**What is it?**
Cloud Run ante - code ni deploy cheyyali ante, Docker container use chesi GCP lo host cheyyi. Auto scale cheyyi (traffic vachina 自动 ga increase).

**Simple:**
```
Your Code → Docker Container → Cloud Run → Live URL!
```

**Key Features:**
- Pay only what you use
- Auto scaling (0 to 1000 instances)
- HTTPS automatic

---

## 2. Vertex AI — Google's ML Platform

**What is it?**
Vertex AI ante - GCP lo ML/AI services complete platform. Models train cheyyi, deploy cheyyi, inference cheyyi - elanti pede Vertex AI use cheyyi.

**Services:**
| Service | Use |
|---------|-----|
| Vertex AI Studio | Prompt experimentation |
| Vertex AI Agent Builder | Build AI agents (no code) |
| Vertex AI Model Garden | Pre-built models |
| Vertex AI Vector Search | Similarity search at scale |

---

## 3. BigQuery — Data Warehouse

**What is it?**
BigQuery ante - massive data store & analyze cheyyali. SQL queries use chesi petabytes of data query cheyyi.

**Simple:**
```
Upload 100GB data → Query with SQL → Get results in seconds!
```

**Key Concepts:**
```sql
-- Select data
SELECT * FROM dataset.table WHERE condition;

-- Aggregate
SELECT COUNT(*), AVG(price) FROM sales;

-- Join tables
SELECT a.name, b.order_id
FROM customers a
JOIN orders b ON a.id = b.customer_id;
```

---

## 4. Workload Identity Federation (WIF) — Secure Access

**What is it?**
WIF ante - without API keys, secure ga access cheyyi. GitHub/GCP之间 direct connection, keys store cheyyaledhu.

**Why?**
- No secrets in code
- More secure
- Automatic rotation

**Flow:**
```
GitHub Actions → WIF → GCP Resources (no keys!)
```

---

## 5. Eventarc — Event-Driven

**What is it?**
Eventarc ante - something happen ani (event), automatically trigger function. No manual monitoring.

**Example:**
```
New file in Cloud Storage
        ↓
Eventarc detects
        ↓
Trigger Cloud Run function
        ↓
Process file automatically!
```

---

## 6. Cloud Storage (GCS) — File Storage

**What is it?**
GCS ante - files store cheyyali. Like Google Drive for developers.

```python
from google.cloud import storage

client = storage.Client()
bucket = client.bucket("my-bucket")

# Upload
blob = bucket.blob("file.txt")
blob.upload_from_string("Hello!")

# Download
content = blob.download_as_text()
```

---

## 7. IAM — Access Control

**What is it?**
IAM (Identity and Access Management) ante - appuke chaani control. Konstant access undho, konstant delete cheyyochu?

**Roles:**
| Role | What it does |
|------|-------------|
| Viewer | View only |
| Editor | View + Edit |
| Owner | View + Edit + Delete + Manage |

---

## 8. Pub/Sub — Messaging

**What is it?**
Pub/Sub ante - publish/subscribe. One service publish message, another service subscribe & process.

```
Service A (Publisher)
        ↓
Message
        ↓
Pub/Sub
        ↓
Service B (Subscriber) → Process
```

---

## 9. Cloud Functions — Serverless Functions

**What is it?**
Small code snippets run cheyyi without managing servers. Trigger based.

```python
def hello_world(request):
    return "Hello, World!"
# Deploy → Runs when triggered
```

---

## 10. Docker — Container

**What is it?**
Docker ante - app + dependencies ni package cheyyi. Ee package elanti machine lo unde, run aipothundi.

**Why?**
- "Works on my machine" problem end!
- Consistent deployment

**Commands:**
```bash
docker build -t myapp .
docker run -p 8080:8080 myapp
docker push gcr.io/project/myapp
```

---

## Quick Interview Answers

| Question | Answer |
|----------|--------|
| Cloud Run? | Deploy containers, auto-scale, pay per use |
| Vertex AI? | GCP ML platform - train, deploy, inference |
| BigQuery? | Petabyte-scale data warehouse, SQL queries |
| WIF? | Secure access without API keys (GitHub → GCP) |
| Eventarc? | Event-driven triggers for Cloud Run |
| GCS? | Object storage (files, blobs) |
| IAM? | Access control (who can do what) |
| Pub/Sub? | Async messaging between services |
| Docker? | Containerize apps + dependencies |

---

*Last Updated: Feb 26, 2026*
