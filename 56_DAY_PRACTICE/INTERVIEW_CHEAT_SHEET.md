# 🚀 MASTER INTERVIEW CHEAT SHEET

> Quick revision - All topics in one page!

---

## 🐍 PYTHON

### Variables
```python
name = "Krishna"    # str
age = 25            # int
salary = 50000.50  # float
is_active = True    # bool
```

### Lists
```python
fruits = ["apple", "banana"]
fruits.append("cherry")
fruits[0]      # "apple"
fruits[-1]     # "cherry"
[x for x in list if x%2==0]  # comprehension
```

### Dictionaries
```python
person = {"name": "Krishna"}
person["name"]     # "Krishna"
person["age"] = 25
```

### Functions
```python
def greet(name="Friend"):
    return f"Hello {name}!"

def sum_all(*args):
    return sum(args)

def info(**kwargs):
    for k, v in kwargs.items(): print(f"{k}: {v}")
```

### Sets
```python
skills = {"python", "sql"}
set1 & set2   # intersection
set1 | set2   # union
set1 - set2   # difference
```

---

## 🤖 AI & LLM

### RAG (Retrieval Augmented Generation)
```
User Query → Search Vector DB → Get chunks → Send to LLM → Answer
```
- LLM gets external context
- Reduces hallucinations
- Uses fresh/specific data

### Embeddings
- Text → Numbers (vectors)
- Similar text = Similar numbers
- Used for similarity search

### Agent
- LLM + Tools + Memory + Loop
- Completes multi-step tasks

### Hallucinations
- LLM giving fake info
- Fix: RAG, better prompts, evals

### Context Caching
- Reuse same context → Save money (50%+)

---

## ☁️ GCP

| Service | Use |
|---------|-----|
| **Cloud Run** | Deploy containers, auto-scale |
| **Vertex AI** | ML platform - train, deploy, inference |
| **BigQuery** | Data warehouse, SQL queries |
| **Cloud Storage** | File storage (GCS) |
| **Cloud Functions** | Serverless functions |
| **Pub/Sub** | Async messaging |
| **Eventarc** | Event-driven triggers |
| **IAM** | Access control |
| **WIF** | Secure access without keys |

---

## 📝 STAR METHOD (Answer Questions)

```
S - Situation: What happened?
T - Task: What you needed to do?
A - Action: What you did?
R - Result: What happened?
```

---

## 🎯 HERO STORIES

### Story 1: CI/CD Security
- Fix WIF failure in production
- Deploy zero-trust IAM

### Story 2: Hallucination Fix
- Reduce 40% hallucination → 80% reduction
- Build Agentic RAG with self-correction

### Story 3: Cost Optimizer
- Cut Gemini costs by 60%
- Context caching + scale-to-zero

---

## ✅ Quick Answers

| Q | A |
|---|---|
| List vs Dict? | List=indexed, Dict=key-value |
| Mutable vs Immutable? | List/Dict=Mutable, Tuple/Str=Immutable |
| RAG? | LLM + external data for accurate answers |
| Embeddings? | Text to numbers for similarity |
| Agent? | LLM + tools + loop |
| Cloud Run? | Container deployment + auto-scale |
| BigQuery? | SQL data warehouse |
| WIF? | Secure access without API keys |

---

*Feb 26, 2026 - All Topics Covered*
