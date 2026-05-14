# Day 7: REST APIs with requests

## Mission
Master calling REST APIs using Python's `requests` library — GET, POST, error handling, query params, and raw Gemini API calls without SDK.

## Topics Covered

| Concept | What it does |
|---------|-------------|
| `requests.get()` | Fetch data from a server |
| `requests.post()` | Send data to create a resource |
| `response.json()` | Parse JSON response body |
| `response.status_code` | Check if request succeeded |
| `response.raise_for_status()` | Raise exception on 4xx/5xx |
| `params=` | Query parameters for filtering |
| `timeout=` | Prevent hanging requests |

## Exercises

| # | Function | What you learn |
|---|----------|---------------|
| 1 | `fetch_post()` | GET request to JSONPlaceholder |
| 2 | `create_post()` | POST request with JSON body |
| 3 | `fetch_with_error_handling()` | Try/except for ConnectionError, Timeout, HTTPError |
| 4 | `call_gemini()` | Call Gemini 2.0 Flash without the SDK — just raw HTTP |
| 5 | `search_posts()` | Query parameters with `params=` |

## Key Patterns

```python
# GET with query params
response = requests.get(url, params={"q": "search_term"})

# POST with JSON
response = requests.post(url, json={"key": "value"})

# Error handling
response.raise_for_status()  # raises for 4xx/5xx
```

## Interview Punch

> "I can call any REST API — including Gemini — directly with Python's requests library. No SDK dependency. This matters because production systems often can't use client libraries due to version conflicts or custom auth flows."

## Files
- `exercises.py` — 5 exercises to complete
- `solution.py` — Complete solutions
- `notes.md` — Quick reference
