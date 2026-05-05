# 🎬 Day 4: Classes + OOP — Concept Explainers + Diagrams

## Goal in 1 Line
Learn how to write **Classes** — blueprints that let you model real-world things (documents, pipelines, users) in code.

---

## 🗺️ Concept Map

```
CLASS (Blueprint)
    │
    ├── defines: what data it holds (attributes)
    │
    ├── defines: what it can do (methods)
    │
    └── when called with data → creates → OBJECT (running instance)
                                      │
                                      └── self = this specific object
```

---

## 📋 Diagram 1: Class = Blueprint, Object = Actor

> **See:** `diagram_01_class_blueprint.svg`

```
┌─────────────────────────────────┐         ┌──────────────────────────┐
│ 📋 CLASS — Movie Script         │         │ 🎬 OBJECT — Actors       │
│  "The Hero's Journey"          │  cast() │                          │
│                                │ ───────►│  doc1  doc2  doc3       │
│  class Document:               │         │  each running live,       │
│    title, content             │         │  own data inside         │
│    def word_count(self): ...   │         │                          │
└─────────────────────────────────┘         └──────────────────────────┘

ONE class → MANY objects, each with own data
```

**Banking ETL analogy:** Think of `class` like a bank account template:
- Class = the bank account rules (withdraw, deposit, balance)
- Object = your actual account with ₹50,000 in it
- My account and your account both follow same rules, but different balances

---

## ⚙️ Diagram 2: __init__ and self

> **See:** `diagram_02_self_init.svg`

```
Step 1: CALL          Step 2: __init__ FIRES         Step 3: OBJECT READY
─────────────         ──────────────────────          ────────────────────
doc = Document(       self = brand_new_object          doc now holds:
  "RAG Intro",         saves title + content           doc.title → "RAG Intro"
  "Hello world"      ─────────────────────────►        doc.content → "Hello world"
)

Python actually runs:
Document.__init__(doc, "RAG Intro", "Hello world")
              ↑
          self IS doc — same object, two names
```

**`__init__`** = runs automatically when you create an object, like a director calling "Places everyone!" before a scene starts.

**`self`** = the current actor. When `doc1.word_count()` runs, self = doc1. When `doc2.word_count()` runs, self = doc2.

---

## 🗂️ Diagram 3: DocumentProcessor — Aggregation Pattern

> **See:** `diagram_03_document_processor.svg`

```
class DocumentProcessor:
    def __init__(self):
        self.documents = []   ← empty list, ready to hold Document objects

    def add_document(self, doc):      # doc is a Document object
        self.documents.append(doc)    # stored inside the processor

    def total_words(self):
        return sum(doc.word_count() for doc in self.documents)
                                    ↑
                            loops through each Document inside
```

**Memory model:**

```
DocumentProcessor
├── self.documents: [ ]
│                   ├── doc (RAG Intro)     → word_count: 5
│                   ├── doc2 (SQL Guide)    → word_count: 3
│                   ├── doc3 (GCP Vertex)   → word_count: 4
│                   └── doc4 (API Deploy)   → word_count: 6
│
processor.total_words()  →  18
processor.get_by_title("SQL Guide") → doc2
```

**Real-world use in RAG:** DocumentProcessor holds all document chunks before sending them to Gemini for generation. One manager object, many child document objects.

---

## 🔗 Diagram 4: RAG System = OOP in Action

> **See:** `diagram_04_rag_oop.svg`

```
📄 Document          ✂️ DocumentChunk       💾 ChunkStore         🧠 RAGPipeline
─────────────────   ──────────────────    ──────────────────   ──────────────────
title, content      chunk_id, page_num     embedding: list       retriever, llm
word_count()        overlaps_with()       search_by_vector()    retrieve()→generate()
     │                   │                       │                      │
     │  extends          │                       │                      │
     └──────────────────►│                       │                      │
                         │                       │                      │
                         └──────────────────────►│                      │
                                                │                      │
                              stores chunks     │                      │
                                                └──────────────────────►
                                                 orchestrates the
                                                 whole flow
```

**Why OOP matters in RAG:**
1. **Single Responsibility** — each class does one thing
2. **Easy to test** — test Document separately from ChunkStore
3. **Swap parts** — change Gemini → Claude without rewriting everything
4. **Reuse** — PDFDocument and TextDocument both inherit from Document

---

## 🔍 Common Mistakes

### Mistake 1: Forgetting self
```python
# WRONG
def word_count():
    return len(self.content.split())
# Python doesn't know which object's content to use

# RIGHT
def word_count(self):
    return len(self.content.split())
```

### Mistake 2: Checking object equality with ==
```python
# WRONG — checks if same object in memory
if doc1 == doc2: ...

# RIGHT — checks if same data
if doc1.title == doc2.title: ...
```

### Mistake 3: Modifying class-level defaults
```python
# WRONG — shared across all objects
def __init__(self, title, content, metadata={}):

# RIGHT — each object gets own dict
def __init__(self, title, content, metadata=None):
    self.metadata = metadata if metadata is not None else {}
```

---

## ✅ Check Questions

1. What does `self` point to when `doc.word_count()` is called?
2. What is the difference between a Class and an Object?
3. DocumentProcessor uses what design pattern?
4. What runs automatically when you create a Document object?
5. In the RAG pipeline, which class holds all the chunk objects?

---

## 🎯 Interview Answers

**Q: "What is a class in Python?"**

> "A class is a blueprint for creating objects. Think of it like a movie script — it defines what data an object holds and what methods it can perform. You write the class once, then create as many objects (instances) as you need. Each object has its own independent data, but shares the same behavior defined in the class."

**Q: "What is the difference between __init__ and self?"**

> "__init__ is the constructor — it runs automatically when you create an object, and you use it to set up initial values. self is a reference to the current object instance — it lets you access that object's own data from inside its methods. When I call doc.word_count(), self inside that method is the doc object."

**Q: "How would you design a document ingestion system in OOP?"**

> "I'd create a Document class for the raw data (title, content, metadata). Then a DocumentChunk class that inherits from Document and adds chunk_id and page_number. A DocumentProcessor class would manage a list of Document objects, providing add, search, and aggregate methods. Finally a RAGPipeline class would orchestrate the whole flow — ingest, chunk, embed, retrieve, and generate. Each class has one clear responsibility, making it easy to test and swap components."
