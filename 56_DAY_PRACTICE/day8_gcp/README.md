# ☁️ Day 8: GCP + Your First Cloud Deployment

## Mission
Deploy your first Python app to Google Cloud Platform!

---

## Today's Topics

### Part 1: GCP Fundamentals (30 min)
- What is GCP? Regions, zones, projects
- Set up your GCP account

### Part 2: Deploy to Cloud Run (60 min) 🚀
**Deploy a container to Cloud Run — serverless!**

---

## ☁️ GCP Basics

| Concept | What It Means |
|---------|---------------|
| **Project** | Container for all your GCP resources |
| **Region** | Geographic location (us-central1, asia-south1) |
| **Zone** | Specific data center within a region |
| **Cloud Run** | Serverless containers - pay only what you use |

---

## 🎯 Hands-On: Deploy to Cloud Run

### Step 1: Install gcloud CLI
```bash
brew install google-cloud-sdk
gcloud init
```

### Step 2: Create a simple Python app
```python
# main.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"message": "Hello from Cloud Run!", "status": "deployed"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

### Step 3: Containerize with Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install flask
EXPOSE 8080
CMD ["python", "main.py"]
```

### Step 4: Deploy!
```bash
gcloud run deploy --source . --region us-central1
```

---

## 📊 Visualization: How Cloud Run Works

```
User Request
     │
     ▼
┌─────────────┐
│   Cloud Run │
│  (Auto-scale│
│   0→1000+)  │
└─────────────┘
     │
     ▼
┌─────────────┐
│  Container  │
│ (your app)  │
└─────────────┘
```

---

## Interview Punch

> "I deployed my first app to Cloud Run last week. It auto-scales from zero to thousands of requests, and I only pay per request. That's serverless containers — no infrastructure management needed."

---

## Today's Checkbox

- [ ] Install gcloud CLI
- [ ] Create GCP project (or use existing)
- [ ] Write simple Flask app
- [ ] Create Dockerfile
- [ ] Deploy to Cloud Run
- [ ] Test your live endpoint!
- [ ] **Tell someone: "I'm deployed on GCP!"**

---

*Mantra: Thaggedhe Le — Cloud is the future!* ☁️🚀
