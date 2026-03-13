import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

import main


class _FakeResponse:
    def __init__(self, text: str):
        self.text = text


class _FakeModels:
    def __init__(self, side_effects):
        self._side_effects = list(side_effects)

    def generate_content(self, **kwargs):
        effect = self._side_effects.pop(0)
        if isinstance(effect, Exception):
            raise effect
        return effect


class _FakeClient:
    def __init__(self, side_effects):
        self.models = _FakeModels(side_effects)


class FastAPIGeminiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app)

    def test_healthz(self):
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_chat_validation_error_for_empty_prompt(self):
        response = self.client.post("/chat", json={"prompt": ""})
        self.assertEqual(response.status_code, 422)

    def test_chat_success_without_retry(self):
        fake = _FakeClient([_FakeResponse("hello")])
        with patch("main.get_client", return_value=fake):
            response = self.client.post(
                "/chat",
                json={"prompt": "say hi", "temperature": 0.2, "max_tokens": 32},
            )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["response"], "hello")
        self.assertEqual(payload["retries_used"], 0)
        self.assertIn("request_id", payload)

    def test_chat_retries_then_succeeds(self):
        fake = _FakeClient([Exception("timeout"), _FakeResponse("after retry")])
        with patch("main.get_client", return_value=fake):
            response = self.client.post("/chat", json={"prompt": "retry test"})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["response"], "after retry")
        self.assertEqual(payload["retries_used"], 1)

    def test_chat_maps_rate_limit_to_429(self):
        fake = _FakeClient(
            [Exception("rate limit exceeded"), Exception("rate limit exceeded"), Exception("rate limit exceeded")]
        )
        with patch("main.get_client", return_value=fake):
            response = self.client.post("/chat", json={"prompt": "test rate limit"})
        self.assertEqual(response.status_code, 429)
        payload = response.json()
        self.assertEqual(payload["error"], "Upstream rate limit exceeded")


if __name__ == "__main__":
    unittest.main()
