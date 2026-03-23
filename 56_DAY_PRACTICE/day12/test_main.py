import unittest

from fastapi.testclient import TestClient

import main


class Day12FastAPITests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_echo_valid(self):
        response = self.client.post("/echo", json={"message": "hello fastapi"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"echo": "hello fastapi"})

    def test_echo_missing_message(self):
        response = self.client.post("/echo", json={})
        self.assertEqual(response.status_code, 422)
        self.assertTrue(response.json()["detail"])
        self.assertEqual(response.json()["detail"][0]["loc"], ["body", "message"])


if __name__ == "__main__":
    unittest.main()
