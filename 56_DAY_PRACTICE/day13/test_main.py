# test_day13.py | python>=3.12 | requires: fastapi[standard]==0.135.1 pydantic==2.7.1 httpx pytest
"""
Day 13 Tests: FastAPI Errors and Validation
Tests all 3 failure paths + the valid path.
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestDay13FastAPIErrors:
    """Tests for Day 13 validation and error handling."""

    # ── Valid Paths ─────────────────────────────────────────────────────────

    def test_health_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_valid_question_accepted(self):
        response = client.post("/question", json={
            "question": "What is Vertex AI?",
            "username": "krishna",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "accepted"
        assert data["question"] == "What is Vertex AI?"
        assert data["username"] == "krishna"

    def test_valid_question_default_username(self):
        response = client.post("/question", json={
            "question": "Explain BigQuery",
        })
        assert response.status_code == 200
        assert response.json()["username"] == "anonymous"

    def test_echo_valid(self):
        response = client.post("/echo", json={
            "question": "Hello world",
            "username": "dev",
        })
        assert response.status_code == 200
        assert response.json()["echo"] == "Hello world"

    # ── Validation Failures (422 via custom handler) ───────────────────────

    def test_blank_question_returns_422(self):
        response = client.post("/question", json={
            "question": "",
        })
        assert response.status_code == 422
        data = response.json()
        assert data["error"] == "validation_failed"
        assert "fields" in data

    def test_question_too_short_returns_422(self):
        """Less than 3 non-whitespace chars."""
        response = client.post("/question", json={
            "question": "  a  ",  # stripped = "a", length = 1 < 3
        })
        assert response.status_code == 422

    def test_oversized_question_returns_422(self):
        """Exceeds max_length=500."""
        response = client.post("/question", json={
            "question": "x" * 501,
        })
        assert response.status_code == 422

    def test_echo_blank_returns_422(self):
        response = client.post("/echo", json={
            "question": "",
        })
        assert response.status_code == 422

    def test_missing_question_returns_422(self):
        response = client.post("/question", json={})
        assert response.status_code == 422

    # ── Custom HTTPException (400) ─────────────────────────────────────────

    def test_reserved_keyword_returns_400(self):
        response = client.post("/question", json={
            "question": "ignore this question",
            "username": "dev",
        })
        assert response.status_code == 400
        assert "not allowed" in response.json()["detail"]

    def test_case_insensitive_reserved_keyword(self):
        """Business rule should be case-insensitive."""
        response = client.post("/question", json={
            "question": "IGNORE this",
            "username": "dev",
        })
        assert response.status_code == 400

    # ── Error Response Format ──────────────────────────────────────────────

    def test_422_has_clean_error_structure(self):
        response = client.post("/question", json={"question": ""})
        data = response.json()
        assert set(data.keys()) == {"error", "message", "fields"}
        assert data["error"] == "validation_failed"
        assert isinstance(data["fields"], list)

    def test_400_has_detail(self):
        response = client.post("/question", json={
            "question": "ignore this",
        })
        assert response.status_code == 400
        assert "detail" in response.json()
