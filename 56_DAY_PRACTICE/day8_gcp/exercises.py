# Day 8 Exercises - GCP Cloud Run Deployment

# Exercise 1: Answer these questions
exercise_1 = """
1. What is the difference between a Region and a Zone in GCP?
2. What is Cloud Run used for?
3. Why use gunicorn instead of running 'python main.py' in production?
"""

# Exercise 2: Fix this Dockerfile
broken_dockerfile = """
# Fix this Dockerfile - it's missing something!
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install flask
CMD ["python", "main.py"]

# What's wrong? What needs to be added?
"""

# Exercise 3: GCP CLI Commands
gcp_questions = """
Fill in the commands:

1. Check gcloud version: _______
2. List GCP projects: _______
3. Enable Cloud Run API: _______
4. Deploy to Cloud Run: _______
"""

# Exercise 4: Create a Simple API
def create_health_check_endpoint():
    """
    Create a Flask app with:
    - GET / → returns {"message": "Hello"}
    - GET /health → returns {"status": "healthy"}

    Write the code below:
    """
    # Your code here:
    pass

# Exercise 5: Cloud Run Pricing
pricing_questions = """
Cloud Run pricing questions:

1. How much does Cloud Run cost?
2. What happens to your costs when there are no requests?
3. What's the free tier limit?
"""

print("=" * 50)
print("Day 8 Exercises - GCP Deployment")
print("=" * 50)
print(exercise_1)
print("\n" + "=" * 50)
print(broken_dockerfile)
print("\n" + "=" * 50)
print(gcp_questions)
print("\n" + "=" * 50)
print(pricing_questions)
print("\n" + "=" * 50)
