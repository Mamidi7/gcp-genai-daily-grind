# Day 5 Notes: JSON + File I/O

## The Real Reason You're Learning This

Before touching Gemini API, LangChain, or BigQuery — you need to be
comfortable reading and writing files and parsing JSON. Because:

- Every Gemini API response is JSON
- Every Cloud Run service config is a JSON/env file
- Every LangChain memory, agent state, tool output is JSON
- Every Vertex AI API call returns JSON

This isn't "basic Python". This is the plumbing everything else runs on.

---

## The Big Picture

```
WHERE JSON APPEARS IN YOUR 56-DAY JOURNEY
─────────────────────────────────────────

Day 10+  Gemini API response  →  json.loads()  →  extract generated text
Day 11+  RAG pipeline state   →  json.dump()   →  save progress to disk
Day 15+  LangGraph state      →  json.load()   →  reload agent memory
Day 20+  Cloud Run config     →  json.load()   →  load model settings
Day 30+  Eval results         →  json.dump()   →  save scores, compare runs
```

Right now on Day 5, you're building the tool you'll use every single day after this.

---

## with open() — Why the `with` Keyword Exists

Imagine a bank vault. You open it, take what you need, close it.
If you forget to close it → security risk, data corruption.

```python
# BAD — what if line 2 crashes? File stays open.
f = open("config.json", "r")
data = json.load(f)
f.close()          # might never reach this line

# GOOD — Python guarantees close() runs even if json.load() crashes
with open("config.json", "r") as f:
    data = json.load(f)
# file is closed here. guaranteed. no matter what.
```

The `with` block is a context manager. In GCP code you'll see this pattern
constantly — for files, database connections, HTTP sessions, everything.

---

## File Modes — Three You Actually Use

```
Mode    What it does                    Real use case
─────   ─────────────────────────────   ───────────────────────────────
"r"     Read. File must exist.          Load model config before API call
"w"     Write. Erases existing file.    Save Gemini response to disk
"a"     Append. Adds to end of file.    Log every API call to a log file
```

---

## JSON: The Language APIs Speak

Python dict lives in memory. JSON lives on disk or travels over the network.
They look identical but they are NOT the same thing.

```
IN MEMORY (Python dict)              ON DISK / OVER NETWORK (JSON text)
────────────────────────             ──────────────────────────────────
{"theme": "dark",                    '{"theme": "dark",
 "active": True,                      "active": true,
 "count": None}                       "count": null}'

Differences:
  Python True/False  →  JSON true/false   (lowercase!)
  Python None        →  JSON null
  Python tuple       →  JSON array        (becomes a list on reload)
  Keys can be anything → Keys must be strings
```

---

## The Four Operations You'll Use

### 1. File → String
```python
with open("response.json", "r") as f:
    raw_string = f.read()       # entire file as one string
# raw_string = '{"text": "UPI limit is 1 lakh per day"}'
```

### 2. String → Dict  (json.loads — note the s)
```python
data = json.loads(raw_string)
# data = {"text": "UPI limit is 1 lakh per day"}
print(data["text"])  # UPI limit is 1 lakh per day
```

### 3. Dict → File  (json.dump — no s)
```python
config = {"model": "gemini-1.5-flash", "temperature": 0.1, "max_tokens": 1024}
with open("model_config.json", "w") as f:
    json.dump(config, f, indent=2)
# saves human-readable JSON to disk
```

### 4. File → Dict  (json.load — no s, takes file object)
```python
with open("model_config.json", "r") as f:
    config = json.load(f)
# config = {"model": "gemini-1.5-flash", "temperature": 0.1, ...}
```

---

## dump vs dumps — This Trips Everyone Up

```
json.dump(dict, file_object)    →  writes to a FILE
json.dumps(dict)                →  returns a STRING

dump  = dump to file   (needs a file object)
dumps = dump to string (no file needed)
```

```python
# When do you use dumps instead of dump?
# When sending data over the network (APIs, Cloud Run responses)

import json
from fastapi import FastAPI
app = FastAPI()

@app.get("/config")
def get_config():
    config = {"model": "gemini-1.5-flash", "ready": True}
    return json.loads(json.dumps(config))  # ← FastAPI does this internally
    # In practice FastAPI handles it, but you'll see json.dumps in Cloud Run logs
```

---

## os.path — Checking Before You Open

```
Scenario: Your Cloud Run service starts up.
It tries to load model_config.json.
If file doesn't exist → crash on startup → 500 error for all users.

Fix: check first.
```

```python
import os

config_path = "model_config.json"

if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config = json.load(f)
else:
    # fallback to defaults — service still works
    config = {"model": "gemini-1.5-flash", "temperature": 0.1}
```

This pattern — check → load or fallback — appears in literally every
production service you'll build on GCP.

---

## os.listdir — Batch Processing

```python
# You have a folder of Gemini API responses saved as JSON files
# Process all of them

import os, json

response_folder = "gemini_responses/"
files = os.listdir(response_folder)
json_files = [f for f in files if f.endswith(".json")]

for filename in json_files:
    with open(f"{response_folder}/{filename}", "r") as f:
        response = json.load(f)
    text = response["candidates"][0]["content"]["parts"][0]["text"]
    print(f"{filename}: {text[:50]}...")
```

---

## Common Mistakes

**1. json.load vs json.loads confusion**
```python
# WRONG — load() needs a file object, not a string
data = json.load('{"key": "value"}')   # TypeError

# WRONG — loads() needs a string, not a file object
with open("data.json") as f:
    data = json.loads(f)               # AttributeError

# CORRECT
data = json.loads('{"key": "value"}')  # string → dict
with open("data.json") as f:
    data = json.load(f)                # file → dict
```

**2. Writing to "r" mode file**
```python
# WRONG
with open("config.json", "r") as f:
    json.dump(data, f)    # io.UnsupportedOperation: not writable

# CORRECT
with open("config.json", "w") as f:
    json.dump(data, f, indent=2)
```

**3. No indent — unreadable, hard to debug**
```python
json.dump(data, f)           # {"model":"gemini-1.5-flash","temperature":0.1}
json.dump(data, f, indent=2) # readable, diffable in git, debuggable
```

---

## Why This Matters for GCP/AI  ← THE SECTION THAT WAS MISSING

### Real Gemini API response structure

When you call Gemini in Python, the SDK gives you a response object.
But under the hood it's JSON. Knowing JSON structure lets you debug
when things look wrong.

```python
import vertexai
from vertexai.generative_models import GenerativeModel
import json

vertexai.init(project="your-project", location="us-central1")
model = GenerativeModel("gemini-1.5-flash")

response = model.generate_content("What is UPI?")

# response.text is the shortcut — but what's actually in the raw response?
# It's a JSON object that looks like this:

raw_structure = {
    "candidates": [
        {
            "content": {
                "parts": [{"text": "UPI is Unified Payments Interface..."}],
                "role": "model"
            },
            "finish_reason": "STOP",
            "safety_ratings": [...]
        }
    ],
    "usage_metadata": {
        "prompt_token_count": 5,
        "candidates_token_count": 120
    }
}

# response.text is just this shortcut:
text = raw_structure["candidates"][0]["content"]["parts"][0]["text"]
```

### Saving and loading model configs (Day 10 pattern)

```python
# You'll write this exact pattern in your FastAPI service on Cloud Run

import json, os

CONFIG_PATH = "model_config.json"

def load_model_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {
        "model_name": "gemini-1.5-flash",
        "temperature": 0.1,
        "max_output_tokens": 1024
    }

def save_model_config(config: dict):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

# In your FastAPI startup event:
# config = load_model_config()
# model = GenerativeModel(config["model_name"])
```

### Logging API calls to disk (real production pattern)

```python
import json, os
from datetime import datetime

def log_api_call(prompt: str, response_text: str, tokens_used: int):
    """Save every Gemini call to a log file for debugging and billing tracking."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "response": response_text,
        "tokens": tokens_used
    }
    log_path = "logs/api_calls.jsonl"  # .jsonl = one JSON object per line
    os.makedirs("logs", exist_ok=True)
    with open(log_path, "a") as f:     # "a" = append, not overwrite
        f.write(json.dumps(log_entry) + "\n")
```
