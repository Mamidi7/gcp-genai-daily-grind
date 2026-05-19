# Day 12: FastAPI Basics — Ported from Flask Day 8
"""
Compare with Day 8 Flask version:
  Flask: from flask import Flask, jsonify
  FastAPI: from fastapi import FastAPI

  Flask: @app.route("/health")
  FastAPI: @app.get("/health")

  Flask: return jsonify({"status":"ok"})
  FastAPI: return {"status":"ok"}  # auto-converts to JSON

  Flask: python main.py
  FastAPI: uvicorn main:app --port 8012

Run:
    uvicorn main:app --host 0.0.0.0 --port 8012
"""

import os
import socket
import sys
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="FastAPI Basics (ported from Flask Day 8)", version="1.0.0")

PORT = int(os.getenv("PORT", 8012))


# ─── Pydantic Model for POST input ──────────────────────────────────
# Flask lo: data = request.get_json() + manual field check
# FastAPI lo: Pydantic checks automatically → 422 if invalid

class EchoRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=200)


# ─── Routes ─────────────────────────────────────────────────────────

@app.get("/")
def root():
    """Root endpoint — same as Day 8 Flask '/'."""
    return {
        "message": "Hello from FastAPI!",
        "ported_from": "Flask Day 8",
        "platform": "FastAPI + Uvicorn"
    }


@app.get("/health")
def health():
    """Health check — same as Day 8 Flask '/health'."""
    return {"status": "healthy"}


@app.get("/info")
def info():
    """Info endpoint — same as Day 8 Flask '/info'."""
    return {
        "app": "FastAPI Basics",
        "framework": "FastAPI",
        "version": app.version,
        "port": PORT,
        "hostname": socket.gethostname(),
        "python_version": sys.version,
    }


@app.post("/echo")
def echo(payload: EchoRequest):
    return {"echo": payload.message}
