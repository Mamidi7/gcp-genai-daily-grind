# 🌐 Day 7: Calling REST APIs with Requests

## Mission
Master REST API calls with Python's `requests` library — this is how you'll connect to Gemini!

## Today's Topic: REST APIs + requests

### 🌐 API Analogy
REST API = Restaurant Menu
- You (client) place an order (request)
- Kitchen (server) prepares food (processes)
- Waiter returns your meal (response)
- Menu items = endpoints

---

## Key Concepts

| Concept | What It Does |
|---------|--------------|
| `requests.get()` | Fetch data from server |
| `requests.post()` | Send data to server |
| `requests.headers` | Send authentication tokens |
| `response.json()` | Parse JSON response |
| `response.status_code` | Check if request succeeded |

---

## Hands-On Task

**Call Gemini API directly using `requests` — no SDK:**

```python
import requests
import os

# Get API key from environment
API_KEY = os.environ.get("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

headers = {"Content-Type": "application/json"}

data = {
    "contents": [{
        "parts": [{"text": "Explain RAG in one sentence."}]
    }]
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())
```

---

## Interview Punch

> "I call Gemini REST API directly using Python's requests library — no SDK wrapper. This gives me full control over headers, timeouts, and error handling. The API returns JSON, which I parse and extract the answer from."

---

## Resources
- requests docs: docs.python-requests.org
- Gemini API: ai.google.dev/docs

---

*Mantra: Thaggedhe Le* 🔥
