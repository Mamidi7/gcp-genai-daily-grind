# 🎬 Day 4: Classes + OOP — Session Explainer

**Session date:** 2026-05-04
**Status:** Concepts explained, exercises pre-filled, all 4/4 tests passing
**Next action:** Walk through exercises.py line by line → then SQL track (CTEs + Subqueries) → commit

---

## ✅ Completed This Session (2026-05-04)

- [x] Loaded CONCEPT_DAY04.md and explained all 4 concepts
- [x] Verified solution.py runs — all 4/4 tests pass
- [x] Walked through: Document, DocumentProcessor, DocumentChunk (inheritance), RAGPipeline
- [x] Covered 3 common mistakes: forgetting self, mutable defaults, == vs value comparison
- [x] Prepared interview answers (30s, 90s STAR, 3-min deep dive)
- [x] Saved session state

## ⏳ Pending (Krishna's action items)

- [ ] Read solution.py line by line — understand every `self`, every method
- [ ] Run exercises.py — confirm it passes
- [ ] Modify exercises.py — remove `self` from a method, see it break, fix it back
- [ ] SQL track: CTEs + Subqueries
- [ ] Commit to GitHub

---

## Goal in 1 Line
Learn how to write **Classes** — blueprints that let you model real-world things (documents, pipelines, users) in code.

---

## Concept 1: Class = Blueprint, Object = Actor

**One-liner:** A class is a template. An object is a real thing made from that template.

```
┌─────────────────────────┐           ┌──────────────────────────┐
│  📋 CLASS — The Blueprint │  cast()   │  🎬 OBJECT — The Actor   │
│                         │ ────────► │                          │
│  class Document:        │           │  doc1 = Document(        │
│    title, content       │           │    "RAG Intro",          │
│    def word_count(self) │           │    "Retrieval works..."  │
│                         │           │  )                        │
│  Lives on paper.        │           │                          │
│  Defines rules only.     │           │  Lives in memory.        │
│                         │           │  Has actual data.         │
└─────────────────────────┘           └──────────────────────────┘
```

**Banking analogy (ETL background):**
```
CLASS = Bank Account Template
  ├── Every account has: balance, account_number
  ├── Every account can: deposit(), withdraw(), check_balance()
  └── Rules are the same for everyone

OBJECT = Your Actual Account
  ├── account_number: SBIN0001234
  ├── balance: ₹50,000
  └── deposit ₹5,000 → balance becomes ₹55,000
```
My account and your account follow the SAME class rules, but hold DIFFERENT data.

---

## Concept 2: `__init__` and `self`

**One-liner:** `__init__` fires when the object is born. `self` is the name for the current object.

```
doc = Document("RAG Intro", "Retrieval augmented generation...")

Python actually runs behind the scenes:
Document.__init__(doc, "RAG Intro", "Retrieval augmented generation...")
                       ↑
                   self = doc
```

```
STEP 1: You call                STEP 2: __init__ runs               STEP 3: Object ready
doc = Document(...)            self = brand_new_object             doc now has
                              self.title = "RAG Intro"             doc.title → "RAG Intro"
                              self.content = "Retrieval..."         doc.content → "Retrieval..."
                              ───────────────────────────►
```

**`self` in plain English:**
- `doc1.word_count()` → `self` = doc1
- `doc2.word_count()` → `self` = doc2
- Python automatically passes the object into the method. You just have to accept it.

**Common mistake:**
```python
# WRONG — forgot self
def word_count():
    return len(self.content.split())  # Python error: "self is not defined"

# RIGHT
def word_count(self):
    return len(self.content.split())
```

---

## Concept 3: DocumentProcessor — Aggregation Pattern

**One-liner:** One manager object holds many child objects inside a list.

```python
class DocumentProcessor:
    def __init__(self):
        self.documents = []   # empty list, waiting for Document objects

    def add(self, doc):
        self.documents.append(doc)   # stores the Document object inside

    def total_words(self):
        return sum(d.word_count() for d in self.documents)
```

**Memory model:**
```
DocumentProcessor
│
└── self.documents: [ ]
                       ├── doc (RAG)      → title: "RAG Intro"    word_count: 5
                       ├── doc2 (SQL)     → title: "SQL Guide"    word_count: 3
                       ├── doc3 (GCP)     → title: "Vertex AI"    word_count: 4
                       └── doc4 (API)     → title: "FastAPI"      word_count: 6

processor.total_words()         →  18
processor.find_by_title("SQL Guide") → doc2
```

**Why useful in RAG?**
When you ingest 50 documents, you don't manage 50 separate variables. ONE DocumentProcessor holds all 50 inside one list.

---

## Concept 4: Inheritance — `DocumentChunk(Document)`

**One-liner:** Child class gets everything from parent, then adds its own stuff.

```python
class DocumentChunk(Document):               # (Document) means inherit
    def __init__(self, title, content, chunk_id, page_number):
        super().__init__(title, content)     # calls Document's __init__
        self.chunk_id = chunk_id
        self.page_number = page_number

    def summary(self):                       # OVERRIDE parent's method
        return (f"Title: {self.title}, Chunk: {self.chunk_id}, "
                f"Page: {self.page_number}, Words: {self.word_count()}")
```

**What you get FREE from Document:**
- `title`, `content` attributes
- `word_count()` method

**What you ADD:**
- `chunk_id`, `page_number`
- Better `summary()` (overrides parent)

```
Document (parent)
  ├── title, content
  ├── word_count()
  └── summary()
       ↑
DocumentChunk (child) — inherits ALL of Document
  ├── + chunk_id, page_number
  └── overrides summary()
```

---

## Concept 5: RAGPipeline — Composing Everything

```python
class RAGPipeline:
    def __init__(self):
        self.processor = DocumentProcessor()  # aggregation

    def ingest(self, title, content):
        self.processor.add(Document(title, content))

    def search(self, keyword):
        return [d for d in self.processor.documents if keyword in d.content]

    def stats(self):
        docs = len(self.processor.documents)
        words = self.processor.total_words()
        avg = round(words / docs, 1) if docs > 0 else 0
        print(f"Docs: {docs}, Words: {words}, Avg: {avg}")
```

**How they connect:**
```
RAGPipeline ──has a──► DocumentProcessor ──has many──► Document
  ingest()                 add()                         title
  search()                 total_words()                 content
  stats()                  find_by_title()               word_count()
                                                              ↑
                                                        DocumentChunk
                                                          chunk_id
                                                          page_number
```

---

## Common Mistakes

### Mistake 1: Forgetting self
```python
# WRONG
def word_count():
    return len(self.content.split())

# RIGHT
def word_count(self):
    return len(self.content.split())
```

### Mistake 2: Modifying class-level defaults (shared dict bug)
```python
# WRONG — metadata={} shared across all objects!
def __init__(self, title, content, metadata={}):

# RIGHT — each gets own dict
def __init__(self, title, content, metadata=None):
    self.metadata = metadata if metadata is not None else {}
```

### Mistake 3: == vs value comparison
```python
# WRONG — checks if SAME object in memory
if doc1 == doc2: ...

# RIGHT — check specific attributes
if doc1.title == doc2.title and doc1.content == doc2.content: ...
```

---

## Check Questions

1. What does `self` point to when `doc.word_count()` is called?
2. What is the difference between a Class and an Object?
3. DocumentProcessor uses what design pattern?
4. What runs automatically when you create a Document object?
5. What does `super().__init__()` do in DocumentChunk?

---

## Interview Answers

**Q: "What is a class in Python?" (30 seconds)**

> "A class is a blueprint for creating objects. Think of it like a movie script — it defines what data an object holds and what methods it can perform. You write the class once, then create as many objects as you need. Each object has its own independent data, but shares the same behavior defined in the class."

**Q: "What is the difference between __init__ and self?" (90 seconds — STAR)**

> "Let me explain with a banking analogy from my ETL work. When I process a bank transfer file, each transaction follows the same class rules — validate, compute, write. But each transaction record has its own data — different amounts, different accounts. That's exactly how classes work. The class defines the rules, and __init__ is the constructor that runs when each object is created to set up that object's specific data. Self is a reference to whichever specific object is currently running the method. So when I call doc1.word_count(), self is doc1. When I call doc2.word_count(), self is doc2. Python passes self automatically — you just have to accept it as the first parameter in your method."

**Q: "How would you design a document ingestion system in OOP?" (3 minutes)**

> "I'd layer it by responsibility. First, a Document class for the raw data — title, content, metadata, plus utility methods like word_count and has_keyword. Second, a DocumentChunk class that inherits from Document and adds chunk_id and page_number for tracking where each chunk came from. Third, a DocumentProcessor class that acts as a manager — it holds a list of Document objects and provides add, search, and aggregate methods. In production RAG, this is where I'd handle batching before sending to Gemini. Fourth and top-level, a RAGPipeline that orchestrates the full flow — ingest, chunk, embed into vector store, retrieve relevant chunks, and generate the final answer. The key design principle here is Single Responsibility — each class does one thing. If I need to change how embedding works, I only touch the processor. If I need to swap Gemini for Claude, I only touch the RAGPipeline. This makes the system testable, swappable, and maintainable."

---

## Files in day4/

| File | Purpose |
|------|---------|
| `CONCEPT_DAY04.md` | Full concept reference with diagrams |
| `SESSION_DAY04_EXPLAINER.md` | This file — session tracking |
| `solution.py` | Complete working code (all 4 exercises) |
| `exercises.py` | Exercise file (same as solution, pre-filled) |
| `diagram_01_class_blueprint.svg` | Class vs Object visual |
| `diagram_02_self_init.svg` | __init__ and self flow |
| `diagram_03_document_processor.svg` | Aggregation pattern |
| `diagram_04_rag_oop.svg` | Full RAG as OOP classes |
