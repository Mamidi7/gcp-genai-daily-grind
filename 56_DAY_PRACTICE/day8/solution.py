# Day 8 Solutions: Flask + Docker + Cloud Run

import requests


# ──────────────────────────────────────────────────
# Exercise 1: Test the Flask app locally
# ──────────────────────────────────────────────────

def test_root(base_url="http://localhost:8080"):
    """GET / and return the 'message' field."""
    response = requests.get(f"{base_url}/")
    response.raise_for_status()
    data = response.json()
    return data["message"]


def test_health(base_url="http://localhost:8080"):
    """GET /health and return the status code."""
    response = requests.get(f"{base_url}/health")
    return response.status_code


# ──────────────────────────────────────────────────
# Exercise 2: Add a new endpoint
# ──────────────────────────────────────────────────
# Add to main.py:
#
# @app.route("/version")
# def version():
#     return jsonify({
#         "version": "1.0.0",
#         "app": "Flask on Cloud Run"
#     })


# ──────────────────────────────────────────────────
# Exercise 3: Docker build and run
# ──────────────────────────────────────────────────

def docker_commands():
    """Return the shell commands to build and run the Docker container."""
    commands = [
        "# Build the image",
        "docker build -t flask-cloud-run .",

        "# Run the container",
        "docker run -p 8080:8080 flask-cloud-run",

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
    Uses source-based deployment (Cloud Build handles containerization).
    """
    cmd = (
        f"gcloud run deploy {service_name} "
        f"--source . "
        f"--region us-central1 "
        f"--allow-unauthenticated "
        f"--memory 256Mi "
        f"--project {project_id}"
    )
    return cmd


# ──────────────────────────────────────────────────
# Exercise 5: Fix common mistake
# ──────────────────────────────────────────────────

def fix_data_endpoint():
    """
    Bug 1: Returning a plain dict — Flask needs jsonify() or a Response object.
    Bug 2: Missing import for jsonify if using Flask directly.
    """
    correct = '''from flask import jsonify

@app.route("/data")
def get_data():
    data = {"name": "test", "value": 42}
    return jsonify(data)'''
    return correct


# ──────────────────────────────────────────────────
# Bonus: Health check chain
# ──────────────────────────────────────────────────

def check_health_chain(base_url="http://localhost:8080"):
    """Call all 3 endpoints and verify each returns 200."""
    endpoints = ["/health", "/info", "/"]
    all_ok = True

    for ep in endpoints:
        try:
            r = requests.get(f"{base_url}{ep}", timeout=5)
            print(f"GET {ep} -> {r.status_code}")
            if r.status_code != 200:
                all_ok = False
            # Show a key field
            data = r.json()
            key = list(data.keys())[0]
            print(f"  {key}: {data[key]}")
        except Exception as e:
            print(f"GET {ep} -> FAILED: {e}")
            all_ok = False

    return all_ok


# ──────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Day 8 Solutions ===\n")

    print("Docker commands:")
    print(docker_commands())

    print("\nCloud Run deploy command:")
    print(cloud_run_deploy_command("my-project-123"))

    print("\nFixed data endpoint:")
    print(fix_data_endpoint())

    print("\nNote: Exercises 1 and Bonus require the Flask app to be running.")
    print("Start it with:  uv run python main.py")
    print("Then test with:")
    print("  python -c \"from exercises import *; print(test_root())\"")
