# Vertex AI Endpoint Deployment Guide (Console vs. CLI)

## 1. Creating an Endpoint
**The Goal:** Create a network address (endpoint) that can serve predictions.

### 🌐 Google Cloud Console
1.  Go to **Vertex AI** > **Endpoints** in the sidebar.
2.  Click **+ CREATE ENDPOINT**.
3.  Name it: `resnet-test-endpoint-v2`.
4.  Region: `us-central1` (Match your model's region).
5.  Click **CREATE**.

### 💻 CLI Command
```bash
gcloud ai endpoints create \
    --region=us-central1 \
    --display-name=resnet-test-endpoint-v2
```

---

## 2. Deploying a Model to the Endpoint
**The Goal:** Attach your trained model to the endpoint and allocate compute resources.

### 🌐 Google Cloud Console
1.  Go to **Vertex AI** > **Models**.
2.  Click your model (`resnet_model_v1`).
3.  Click **DEPLOY TO ENDPOINT**.
4.  Select `resnet-test-endpoint-v2`.
5.  **Configure Compute Resources:**
    -   Machine type: `n1-standard-4`.
    -   Traffic split: `100%`.
    -   Min/Max replicas: `1` / `1`.
6.  Click **DEPLOY**.

### 💻 CLI Command
```bash
gcloud ai endpoints deploy-model YOUR_ENDPOINT_ID \
    --region=us-central1 \
    --model=YOUR_MODEL_ID \
    --display-name=resnet-deployment \
    --machine-type=n1-standard-4 \
    --min-replica-count=1 \
    --max-replica-count=1 \
    --traffic-split=0=100
```

---

## 3. Testing the Endpoint
**The Goal:** Send an image and get a prediction.

### 🌐 Google Cloud Console (Limited)
1.  Go to the Endpoint.
2.  Click **TEST MODEL**.
3.  Upload a JSON file (`request.json`). *Painful for images due to manual base64 encoding.*

### 💻 CLI Command (Painful)
```bash
gcloud ai endpoints predict YOUR_ENDPOINT_ID \
    --region=us-central1 \
    --json-request=request.json
```

### 🐍 Python SDK (Proper Way)
```python
from google.cloud import aiplatform

endpoint = aiplatform.Endpoint('YOUR_ENDPOINT_ID')
prediction = endpoint.predict(instances=[{"b64": "..."}])
print(prediction)
```
