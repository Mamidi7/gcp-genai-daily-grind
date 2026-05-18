# Day 8: Flask App + Docker + Cloud Run
"""
A simple Flask API with 3 endpoints, containerized with Docker,
ready for Cloud Run deployment.

Endpoints:
  GET /       — Welcome message
  GET /health — Health check for Cloud Run load balancer
  GET /info   — App metadata
"""

from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────

@app.route("/")
def hello():
    """Root endpoint — returns a welcome message."""
    return jsonify({
        "message": "Hello from Cloud Run!",
        "status": "deployed",
        "platform": "Google Cloud Run"
    })


@app.route("/health")
def health():
    """Health check endpoint — Cloud Run uses this to verify the instance is alive."""
    return jsonify({"status": "healthy"})


@app.route("/info")
def info():
    """Info endpoint — returns app metadata."""
    return jsonify({
        "app": "Flask on Cloud Run",
        "port": os.getenv("PORT", "8080"),
        "hostname": socket.gethostname(),
        "python_version": os.sys.version,
        "message": "I love you Threeja, lovee of my life ❤️"
    })


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
