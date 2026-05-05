# Day 5 Notes: JSON + File I/O

## The Big Picture

```
File on disk          Python reads it          Python works with it
────────────          ──────────────           ───────────────────
config.json    →    open("r") as f     →     f.read()
                  →    json.load(f)     →     {"theme": "dark"}
                  →    returns dict              ↕
Python saves it      json.dump(dict, f)  →     config.json updated
{"theme": "light"}  open("w") as f
```

---

## with open() — Always Use This

Regular `open()` can leave files open if your code crashes.

```python
# BAD — file stays open if error happens
f = open("config.json", "r")
data = json.load(f)
f.close()  # might never run

# GOOD — always closes automatically
with open("config.json", "r") as f:
    data = json.load(f)
```

The `with` keyword guarantees the file closes, even if an error happens.

---

## File Modes

| Mode | What it does |
|------|-------------|
| `"r"` | Read (file must exist) |
| `"w"` | Write (erases existing content) |
| `"a"` | Append (adds to end) |

---

## JSON — Dicts as Text

JSON looks like a Python dict, but it's stored as text.

```python
# Python dict (in memory)
settings = {"theme": "dark", "font_size": 14}

# JSON (text on disk)
{
  "theme": "dark",
  "font_size": 14
}
```

Key differences: `true/false` (lowercase), no trailing commas, keys always quoted.

---

## json.load() — File to Dict

```python
with open("config.json", "r") as f:
    data = json.load(f)

print(data["theme"])  # "dark"
```

---

## json.dump() — Dict to File

```python
settings = {"theme": "dark", "notifications": True}

with open("settings.json", "w") as f:
    json.dump(settings, f, indent=2)
```

`indent=2` makes it readable. Without it, everything is one long line.

---

## json.dumps() vs json.dump()

```
json.dump(dict, file)  → writes to a file
json.dumps(dict)       → returns a string (for APIs)
```

```python
# For saving to disk
json.dump(my_dict, f, indent=2)

# For sending to an API
string = json.dumps(my_dict)  # '{"theme": "dark", ...}'
```

---

## os.path.exists() — Check Before Reading

```python
import os

if os.path.exists("config.json"):
    with open("config.json") as f:
        data = json.load(f)
else:
    print("File not found")
```

---

## os.listdir() — List Folder Contents

```python
files = os.listdir("data/")
print(files)  # ['config.json', 'grades.csv', ...]

# Filter for specific types
json_files = [f for f in files if f.endswith(".json")]
```

---

## Common Mistakes

**1. Forgetting to close the file**
```python
# BAD
f = open("data.json", "r")
data = json.load(f)

# GOOD
with open("data.json", "r") as f:
    data = json.load(f)
```

**2. json.dump vs json.dumps**
```python
# WRONG — dump needs a file object
result = json.dump({"name": "Alice"})  # TypeError!

# CORRECT
result = json.dumps({"name": "Alice"})  # returns string
json.dump({"name": "Alice"}, f)        # writes to file
```

**3. No indent = unreadable JSON**
```python
# One long line
json.dump(data, f)

# Pretty and readable
json.dump(data, f, indent=2)
```

**4. Using wrong file mode**
```python
# Writing to a file opened in read mode
with open("data.json", "r") as f:
    json.dump(data, f)  # io.UnsupportedOperation: not writable

# Correct mode for writing
with open("data.json", "w") as f:
    json.dump(data, f)
```
