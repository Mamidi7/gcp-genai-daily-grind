# Day 8 Solutions - GCP Cloud Run Deployment

# Exercise 1: Answers
exercise_1_answers = """
1. Region = area, Zone = geographic specific data center within region
2. Cloud Run = serverless container platform that auto-scales
3. gunicorn is a production WSGI server, handles multiple requests better
"""

# Exercise 2: Fixed Dockerfile
fixed_dockerfile = """
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install flask gunicorn
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]

# Fixed: Added EXPOSE and changed CMD to use gunicorn
"""

# Exercise 3: GCP CLI Commands
gcp_answers = """
1. gcloud --version
2. gcloud projects list
3. gcloud services enable run.googleapis.com
4. gcloud run deploy --source . --region us-central1
"""

# Exercise 4: Health Check App Solution
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"message": "Hello"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

# Exercise 5: Pricing Answers
pricing_answers = """
1. $0.24 per 100,000 vCPU-seconds, $0.05 per 100,000 GiB-seconds
2. Costs are ZERO when there are no requests (Cold!)
3. 180,000 vCPU-seconds, 360,000 GiB-seconds per month FREE
"""

print("=" * 50)
print("Day 8 Solutions")
print("=" * 50)
print(exercise_1_answers)
print("\n" + "=" * 50)
print(fixed_dockerfile)
print("\n" + "=" * 50)
print(gcp_answers)
print("\n" + "=" * 50)
print(pricing_answers)
print("\n" + "=" * 50)
