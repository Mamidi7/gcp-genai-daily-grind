# Day 4: Notes

## What I Learned

### Class Basics
- `__init__` is called when you create an instance: `doc = Document(title, content)`
- `self` refers to the instance — always the first parameter of instance methods
- Class methods use `@classmethod` and receive `cls` instead of `self`

### Key Patterns
- `to_dict()` — convert object to dictionary for JSON serialization
- `from_json()` — class method to create object from JSON
- Store metadata in a dict for flexibility

### OOP in RAG Systems
- Document class stores: title, content, chunk_id, source_file, page_number
- DocumentProcessor manages a collection of documents
- Later: inherit from Document for specialized types (PDFDocument, TextDocument)

## SQL Notes
- CTE = Common Table Expression: `WITH x AS (SELECT ...) SELECT * FROM x`
- Subqueries go in WHERE or FROM clause
- CTEs make complex queries readable

## Tomorrow
- Day 5: JSON, File I/O, os module
- Read JSON config files, write results to JSON
