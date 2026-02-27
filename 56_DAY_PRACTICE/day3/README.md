# 🐍 Day 3: Functions in Python

## 📅 Date: February 26, 2026
## ⏱️ Time: 30-45 minutes

---

## 🎯 Today's Mission

**Topic:** Functions — `def`, parameters, return values, *args, **kwargs

**Why this matters for RAG:**
- You'll write functions to chunk documents (this is how RAG starts!)
- API calls to Gemini are functions
- Every piece of your pipeline will be a function

---

## 📖 What You'll Learn

### 1. Basic Function Syntax
```python
def function_name(parameters):
    # code
    return result
```

### 2. Default Parameters
```python
def chunk_text(text, size=512):
    # size defaults to 512 if not provided
    return chunks
```

### 3. *args — Multiple Arguments
```python
def sum_all(*args):
    # args is a tuple of all arguments
    return sum(args)
```

### 4. **kwargs — Keyword Arguments
```python
def configure(**kwargs):
    # kwargs is a dictionary
    for key, value in kwargs.items():
        print(f"{key}: {value}")
```

---

## ✅ Today's Checkpoint

**Done when you can:**
- [ ] Write a function that takes text and splits it into chunks
- [ ] Use default parameters
- [ ] Explain when to use *args vs **kwargs

---

## 🔗 Related Topics
- **Previous:** Day 2 — Lists, Dicts, Loops
- **Next:** Day 4 — Classes + OOP

---

## 📚 Resources
- Python Docs: docs.python.org/3/tutorial/
- Practice: hackerrank.com/domains/python

---

*Mantra: Thaggedhe Le — Relentless Execution*
