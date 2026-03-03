# Day 7 Notes: REST APIs with requests

## What I Learned Today

### Key Takeaways

1. **requests library** - Python's standard way to call HTTP APIs
2. **GET vs POST** - GET fetches data, POST sends data to create something
3. **Headers** - Used for authentication (Bearer tokens, API keys)
4. **Response handling** - Always check status_code, use response.json()

### Important Syntax

```python
# GET request
response = requests.get(url, params={"key": "value"})

# POST request
response = requests.post(url, json={"key": "value"})

# Headers for auth
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get(url, headers=headers)

# Error handling
response.raise_for_status()  # Raises exception for 4xx/5xx
```

### Gemini API (No SDK!)

```python
import requests
import os

API_KEY = os.environ.get("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

data = {
    "contents": [{
        "parts": [{"text": "Your prompt here"}]
    }]
}

response = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
result = response.json()
answer = result['candidates'][0]['content']['parts'][0]['text']
```

### Common Mistakes

- ❌ Not checking status_code
- ❌ Forgetting Content-Type header
- ❌ Not handling JSON parsing errors
- ❌ No timeout on requests

## Questions to Review

- [ ] Can I call Gemini without the SDK?
- [ ] Do I understand GET vs POST?
- [ ] Can I add authentication headers?
- [ ] Can I handle API errors gracefully?

## Tomorrow: GCP Console!

Day 8 = Cloud time! ☁️
