# Python Fundamentals Cheatsheet
## Days 1-7 | Quick Reference for Interview Recall

---

## DAY 1: Gemini SDK + First API Call

### What you built
Called Gemini 2.0 Flash from Python.

### Key Pattern
```python
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain RAG in one sentence"
)
print(response.text)
```

### Interview Sound Bite
"I can call LLM APIs from Python using the official SDK, load secrets from .env, and handle responses."

---

## DAY 2: Variables + Data Types

### The 5 Core Types
```python
name = 'krishna'           # str
city = 'kadapa'            # str
years_experience = 3       # int
is_employed = True         # bool
current_salary = 100000.0  # float
```

### Type Checking
```python
type(name)         # <class 'str'>
type(years_experience)  # <class 'int'>
```

### F-Strings (THE way to format)
```python
f"Name: {name}, City: {city}"  # fast, readable, Python 3.6+
```

### Interview Trap
Q: What is the difference between `==` and `is`?
A: `==` compares values. `is` compares identity (memory address). Always use `is None`, never `== None`.

---

## DAY 3: Data Structures + Loops

### Lists (ordered, mutable, duplicates OK)
```python
fruits = ["apple", "banana", "cherry"]
fruits.append("date")
fruits[0]        # "apple"
fruits[-1]       # "date" (last)
```

### Dictionaries (key-value pairs)
```python
user = {"name": "krishna", "role": "engineer"}
user["name"]                 # "krishna"
user.get("age", 25)          # 25 (default if key missing)
for key, val in user.items():  # iterate both
```

### Tuples (ordered, IMMUTABLE)
```python
coords = (10, 20)
x, y = coords  # unpacking
```

### Loops
```python
for item in list:       # iterate
for i, item in enumerate(list):  # with index
while condition:        # conditional loop
```

### Comprehensions
```python
[x*2 for x in range(10)]           # list comprehension
{k: v for k, v in items if v > 0}  # dict comprehension
```

---

## DAY 4: Functions + Sets + Comprehensions

### Function Patterns
```python
# Basic
def greet(name):
    return f"Hey {name}"

# Variable positional args
def sum_all(*numbers):
    return sum(numbers)
sum_all(1, 2, 3)  # 6

# Variable keyword args
def introduce(**info):
    for key, value in info.items():
        print(f"{key}: {value}")
introduce(name="krishna", role="engineer")
```

### Sets (unordered, unique elements)
```python
a = {"python", "sql", "bigquery"}
b = {"gcp", "bigquery", "cloud run"}

a & b   # intersection: {"bigquery"}
a | b   # union: all unique
a - b   # difference: in a but not b
```

### Interview Use Case
"Sets are ideal for finding common skills, removing duplicates, or checking membership in O(1)."

---

## DAY 5: JSON + File I/O + os Module

### File I/O Pattern (ALWAYS use `with`)
```python
# Read
with open("config.json") as f:
    data = json.load(f)     # file -> dict

# Write
with open("output.json", "w") as f:
    json.dump(data, f, indent=2)  # dict -> file

# String <-> JSON
text = json.dumps(data)     # dict -> string
data = json.loads(text)     # string -> dict
```

### os Module Essentials
```python
import os
os.getenv("API_KEY")           # read env var
os.path.exists("file.txt")     # check file exists
os.listdir(".")                 # list directory
os.environ["GCP_PROJECT"] = x  # set env var
```

### Interview Sound Bite
"I use context managers for file operations to guarantee cleanup, and env vars via `os.getenv()` for configuration."

---

## DAY 6: Classes + OOP

### Class Blueprint
```python
class Document:
    def __init__(self, title, content):
        self.title = title
        self.content = content
    
    def word_count(self):
        return len(self.content.split())
    
    def __str__(self):
        return f"Document('{self.title}')"
    
    def __repr__(self):
        return f"Document('{self.title}', {len(self.content)} chars)"

doc = Document("resume", "Krishna Vardhan")
doc.word_count()   # 2
print(doc)          # Document('resume')
```

### Inheritance
```python
class PDFDocument(Document):
    def __init__(self, title, content, page_count):
        super().__init__(title, content)
        self.page_count = page_count
```

### Key Terms
- **Encapsulation**: bundling data + methods in a class
- **Inheritance**: child reuses parent code
- **Polymorphism**: same method name, different behavior
- **Abstraction**: hide complexity, expose clean interface

---

## DAY 7: REST APIs with requests

### GET Request
```python
import requests

r = requests.get("https://api.example.com/data")
r.status_code    # 200
r.json()         # parse response body as dict
r.headers        # response headers
```

### POST Request
```python
r = requests.post(
    "https://api.example.com/data",
    json={"name": "krishna", "role": "engineer"},
    headers={"Authorization": "Bearer TOKEN"}
)
r.status_code    # 201 (created)
r.json()         # response body
```

### Error Handling Pattern
```python
try:
    r = requests.get(url, timeout=10)
    r.raise_for_status()  # raises HTTPError for 4xx/5xx
    data = r.json()
except requests.Timeout:
    print("Request timed out")
except requests.HTTPError as e:
    print(f"HTTP error: {e}")
```

### REST Concepts
- **GET**: read data (idempotent)
- **POST**: create data (not idempotent)
- **PUT**: replace data (idempotent)
- **DELETE**: remove data (idempotent)
- **Status codes**: 200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Server Error

---

## QUICK REFERENCE TABLE

| Day | Topic | One Pattern to Remember |
|-----|-------|------------------------|
| 1 | Gemini SDK | `client.models.generate_content(model=..., contents=...)` |
| 2 | Variables | `type(x)` + f-strings `f"{name}"` |
| 3 | Data Structures | Lists `[1,2,3]`, Dicts `{"k":"v"}`, Tuples `(1,2)` |
| 4 | Functions | `*args` (tuple), `**kwargs` (dict), set operations `& | -` |
| 5 | JSON + File I/O | `json.load(f)` from file, `json.loads(s)` from string |
| 6 | OOP | `__init__`, `self`, `super()`, `__str__` |
| 7 | REST APIs | `requests.get(url)`, `r.json()`, `r.raise_for_status()` |

---

## COMMON INTERVIEW TRAPS (Days 1-7)

1. "What happens if you open a file without `with`?" — File may stay open on error
2. "Is Python pass-by-reference or pass-by-value?" — Pass-by-object-reference (mutable objects can be changed)
3. "What is a decorator?" — A function that wraps another function: `@decorator`
4. "List vs Tuple performance?" — Tuples are faster for iteration and safe as dict keys
5. "How do you handle missing dict keys?" — `dict.get(key, default)` or `if key in dict`

---

*From actual repo code | Days 1-7 | April 2026 Revision*
