# Day 8 Exercises: Flask + Docker + Cloud Run

"""
These exercises build on the Flask app in main.py.
Complete each function below.

Setup first:
    cd day8
    uv run python main.py    # runs on http://localhost:8080
"""

import requests
import json


# ──────────────────────────────────────────────────
# Exercise 1: Test the Flask app locally
# ──────────────────────────────────────────────────
def test_root(base_url="http://localhost:8080"):
    """
    Send a GET request to the root endpoint (/).
    Return the 'message' field from the JSON response.

    Expected: "Hello from Cloud Run!"
    """
    # TODO: make GET request to base_url + "/"
    pass


def test_health(base_url="http://localhost:8080"):
    """
    Send a GET request to /health.
    Return the response's status code.

    Expected: 200
    """
    # TODO: make GET request to base_url + "/health"
    pass


# ──────────────────────────────────────────────────
# Exercise 2: Add a new endpoint
# ──────────────────────────────────────────────────
"""
Add an endpoint to main.py that returns JSON like:
    GET /version -> {"version": "1.0.0", "app": "Flask on Cloud Run"}

Steps:
    1. Open main.py
    2. Add a new function with @app.route("/version")
    3. Return jsonify with version info

No code needed here — just edit main.py directly.
"""


# ──────────────────────────────────────────────────
# Exercise 3: Docker build and run
# ──────────────────────────────────────────────────
def docker_commands():
    """
    Return the shell commands to:
    1. Build the Docker image (tag: flask-cloud-run)
    2. Run the container locally on port 8080
    3. Test it with curl

    Fill in the blanks below.
    """
    commands = [
        "# Build the image",
        "docker build -t ___ .",

        "# Run the container",
        "docker run -p ___ :8080 ___",

        "# Test it",
        "curl http://localhost:8080/health"
    ]
    return "\n".join(commands)


# ──────────────────────────────────────────────────
# Exercise 4: Cloud Run deploy
# ──────────────────────────────────────────────────
def cloud_run_deploy_command(project_id, service_name="flask-app"):
    """
    Generate the gcloud command to deploy this app to Cloud Run.

    Requirements:
    - Use us-central1 region
    - Allow unauthenticated access
    - Set memory to 256Mi
    - Use source-based deployment (no manual build)

    Return the command as a string.
    """
    # TODO: build gcloud run deploy command
    pass


# ──────────────────────────────────────────────────
# Exercise 5: Fix common mistake
# ──────────────────────────────────────────────────
"""
A colleague wrote this Flask route. Find 2 bugs and fix them.

```python
@app.route("/data")
def get_data():
    data = {"name": "test", "value": 42}
    return data
```
"""
def fix_data_endpoint():
    """
    Return the corrected version of the code above.
    Hint: Flask routes must return a Response object, not a dict.
    """
    # TODO: fix the code
    pass


# ──────────────────────────────────────────────────
# Bonus: Health check chain
# ──────────────────────────────────────────────────
def check_health_chain(base_url="http://localhost:8080"):
    """
    Call /health, then /info, then /.
    Print each response's status code and a key field.
    Return True if all three return 200.
    """
    # TODO: chain three requests
    pass
