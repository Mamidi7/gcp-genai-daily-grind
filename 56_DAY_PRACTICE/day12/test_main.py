import json
from unittest import TestCase, main
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestDay12FastAPI(TestCase):

    def test_root(self):
        resp = client.get("/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("message", data)
        self.assertIn("Hello from FastAPI", data["message"])

    def test_health(self):
        resp = client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"status": "healthy"})

    def test_info(self):
        resp = client.get("/info")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("framework", data)
        self.assertEqual(data["framework"], "FastAPI")
        self.assertIn("version", data)
        self.assertIn("hostname", data)

    def test_echo_valid(self):
        resp = client.post("/echo", json={"message": "hello world"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"echo": "hello world"})

    def test_echo_empty_body_returns_422(self):
        resp = client.post("/echo", json={})
        self.assertEqual(resp.status_code, 422)
        data = resp.json()
        self.assertIn("detail", data)
        # Verify it's a validation error about 'message' field
        errors = data["detail"]
        self.assertTrue(any("message" in str(e.get("loc", [])) for e in errors))

    def test_echo_missing_message_returns_422(self):
        resp = client.post("/echo", json={"wrong_field": "xyz"})
        self.assertEqual(resp.status_code, 422)

    def test_echo_blank_message_returns_422(self):
        resp = client.post("/echo", json={"message": ""})
        self.assertEqual(resp.status_code, 422)


if __name__ == "__main__":
    main()
