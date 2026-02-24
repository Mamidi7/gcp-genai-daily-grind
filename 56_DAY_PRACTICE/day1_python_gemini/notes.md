# Day 1: Python + Gemini API

## Task
- Install `google.genai` SDK
- Call Gemini 2.0 Flash API
- Print response

## Key Learnings
- 

## Script Used
```python
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain RAG in one sentence"
)

print("🤖 Gemini says:")
print(response.text)
```

## Output
Paste console output here:
```

```
