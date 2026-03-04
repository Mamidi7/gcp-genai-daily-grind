# Day 5 Notes: JSON, File I/O, os module

## What I Learned Today

### Key Concepts

1. **File I/O** - Reading and writing files
2. **JSON** - JavaScript Object Notation for data exchange
3. **os module** - File system operations

---

### File Operations

```python
# Read file
with open("file.txt", "r") as f:
    content = f.read()

# Write file
with open("file.txt", "w") as f:
    f.write("Hello!")

# Append
with open("file.txt", "a") as f:
    f.write("\nNew line")
```

---

### JSON Operations

```python
import json

# Write JSON
data = {"name": "Krishna", "age": 25}
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Read JSON
with open("data.json", "r") as f:
    data = json.load(f)
```

---

### os module

```python
import os

os.path.exists("file.txt")  # Check if file exists
os.getcwd()  # Current directory
os.listdir(".")  # List files
os.makedirs("folder")  # Create folder
```

---

## SQL: Window Functions (Today's Track)

### ROW_NUMBER()

```sql
SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) as rank
FROM employees
```

### RANK() vs ROW_NUMBER()

```sql
-- ROW_NUMBER: 1, 2, 3, 4 (always unique)
-- RANK: 1, 1, 3 (same rank for ties, skips numbers)
-- DENSE_RANK: 1, 1, 2 (same rank for ties, no gaps)
```

---

## Interview Punch

> "I use Python's json module to read config files and save evaluation results. Combined with file I/O, this is how I persist data in my RAG pipeline."

---

## Questions to Review

- [ ] Can you read a text file?
- [ ] Can you write JSON to a file?
- [ ] Can you read JSON from a file?
- [ ] Can you check if a file exists?

---

## Next: Day 6 - pip, venv!

Setting up Python environments professionally! 🐍
