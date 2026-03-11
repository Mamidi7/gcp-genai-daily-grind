# Day 10: GCP Python + Cloud Deployments

## What We Built Today

Hands-on experience with GCP Python libraries and deploying serverless functions.

---

## 1. Installed Google Cloud Libraries

```bash
pip install google-cloud-aiplatform google-cloud-storage google-cloud-bigquery
```

**Libraries used:**
- `google-cloud-aiplatform` - For Vertex AI (Gemini)
- `google-cloud-storage` - For GCS file operations
- `google-cloud-bigquery` - For BigQuery queries

---

## 2. Called Vertex AI (Gemini) from Python

**Script:** `vertex_ai_demo.py`

```python
import google.genai as genai
from google.genai import types

client = genai.Client(
    vertexai=True,
    project="e2e-etl-project",
    location="us-central1"
)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="Explain what Vertex AI is",
    config=types.GenerateContentConfig(temperature=0.7)
)
```

**Key points:**
- Uses new `google.genai` client (not deprecated `vertexai.generative_models`)
- Project: `e2e-etl-project`
- Region: `us-central1`
- Model: `gemini-2.0-flash-001`

---

## 3. Uploaded File to Google Cloud Storage

**Script:** `gcs_upload_demo.py`

```python
from google.cloud import storage

client = storage.Client(project="e2e-etl-project")
bucket = client.bucket("krishna-genai-storage-1234")
blob = bucket.blob("uploaded_demo.py")
blob.upload_from_filename("vertex_ai_demo.py")
```

**Bucket:** `krishna-genai-storage-1234`

---

## 4. Deployed Cloud Function (Cloud Run Functions)

**Function name:** `hello-gemini`

**URL:** `https://hello-gemini-279141399436.us-central1.run.app`

**Source code:** `gemini-function/main.py`

```python
import google.genai as genai
from google.genai import types
import functions_framework

@functions_framework.http
def hello_gemini(request):
    client = genai.Client(
        vertexai=True,
        project="e2e-etl-project",
        location="us-central1"
    )

    request_json = request.get_json(silent=True)
    prompt = request_json.get("prompt", "Hello!")

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.7)
    )

    return response.text, 200
```

**requirements.txt:**
```
functions-framework==3.*
google-genai==1.64.0
```

**Deployment via Console:**
1. Go to Cloud Run → Write a function
2. Runtime: Python 3.11
3. Entry point: `hello_gemini`
4. Allow unauthenticated access
5. Deploy!

---

## Interview Talking Points

### Q: How do you call Gemini from Python code?

**Answer:**
Use the `google.genai` client. Initialize with your GCP project and location, then call `client.models.generate_content()` with the model name and prompt.

```python
client = genai.Client(vertexai=True, project="my-project", location="us-central1")
response = client.models.generate_content(model="gemini-2.0-flash-001", contents="prompt")
```

### Q: How do you upload files to GCS from Python?

**Answer:**
Use `google-cloud-storage` library. Create a client, get the bucket, create a blob, and upload.

```python
bucket = storage.Client().bucket("bucket-name")
bucket.blob("file-name").upload_from_filename("local-file")
```

### Q: How do you deploy a serverless function on GCP?

**Answer:**
Two options:
1. **Cloud Run Functions** (formerly Cloud Functions) - for simple Python/Node.js functions
2. **Cloud Run** - for containers (Flask, FastAPI, etc.)

For Cloud Run Functions: use Console or `gcloud functions deploy`. The function must have `@functions_framework.http` decorator and entry point specified.

### Q: What is the difference between Cloud Functions and Cloud Run?

| Feature | Cloud Functions | Cloud Run |
|---------|-----------------|-----------|
| Scope | Simple functions | Full containers |
| Runtime | Python, Node, Go, Java | Any language |
| Scaling | Auto | Auto |
| Networking | Simpler | More control |

---

## Files Created

```
day10_cloud_storage/
├── vertex_ai_demo.py       # Call Gemini from local Python
├── gcs_upload_demo.py      # Upload file to GCS
├── gemini-function/        # Cloud Function source
│   ├── main.py
│   └── requirements.txt
└── DEPLOYMENT_NOTES.md    # This file
```

---

## Useful Commands

```bash
# Authentication
gcloud auth application-default login

# List GCS buckets
gsutil list buckets

# Deploy Cloud Function (CLI)
gcloud functions deploy hello-gemini \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1 \
  --project e2e-etl-project \
  --source .

# Get function URL
gcloud functions describe hello-gemini --region us-central1

# Test function
curl -X POST "URL" -H "Content-Type: application/json" -d '{"prompt": "Hello!"}'
```

---

## Notes

- Gemini 2.0 Flash is available in `us-central1`
- Use `google.genai` client (not deprecated `vertexai.generative_models`)
- Cloud Functions → now called "Cloud Run functions"
- Authentication via Application Default Credentials (ADC)
