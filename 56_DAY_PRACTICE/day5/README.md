# 📄 Day 5: JSON, File I/O, os module

## Mission
Learn to read/write files and handle JSON — essential for RAG pipelines!

## Today's Topic: Working with Files

### 💾 File I/O Analogy
File = 📚 Book
- `open("file.txt", "r")` = Opening book to read
- `open("file.txt", "w")` = Opening book to write
- `with open()` = Having a friend hold the book, then return it properly

---

## Key Concepts

| Function | What It Does |
|----------|--------------|
| `open("file", "r")` | Read file |
| `open("file", "w")` | Write file (overwrites) |
| `open("file", "a")` | Append to file |
| `json.load(f)` | Read JSON from file |
| `json.dump(obj, f)` | Write JSON to file |
| `os.path.exists()` | Check if file exists |
| `os.listdir()` | List files in folder |

---

## Hands-On Task

**Read a JSON config file and write results:**

```python
import json
import os

# Read JSON config
with open("config.json", "r") as f:
    config = json.load(f)

print(config["model"], config["temperature"])

# Write results to JSON
results = {"answer": "RAG is great", "confidence": 0.9}
with open("results.json", "w") as f:
    json.dump(results, f, indent=2)
```

---

## Interview Punch

> "I use Python's json module to read config files and save outputs. Combined with file I/O, this is how I persist data in my RAG pipeline — configs go in, evaluation results come out."

---

## Resources
- Python Docs: docs.python.org/3/tutorial/inputoutput.html

---

*Mantra: Thaggedhe Le* 🔥
