"""
Day 4: Classes + OOP — Exercises
Fill in the blanks. Run: python exercises.py
"""

# ──────────────────────────────────────────────
# Exercise 1: Create a basic Document class
# ──────────────────────────────────────────────
# TODO: Define a class Document with __init__(self, title, content)
# Store title and content on self.
# Add a method summary(self) that returns "Title: <title>, Words: <word_count>"
# Add a method word_count(self) that returns the number of words in content.

class Document:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def word_count(self):
        return len(self.content.split())

    def summary(self):
        return f"Title: {self.title}, Words: {self.word_count()}"


# ──────────────────────────────────────────────
# Exercise 2: DocumentProcessor — Aggregation
# ──────────────────────────────────────────────
# TODO: Define a class DocumentProcessor that:
#   - __init__ creates an empty list self.documents
#   - add(self, doc) appends a Document to self.documents
#   - total_words(self) returns sum of all document word counts
#   - find_by_title(self, title) returns the first matching Document or None

class DocumentProcessor:
    def __init__(self):
        self.documents = []

    def add(self, doc):
        self.documents.append(doc)

    def total_words(self):
        return sum(d.word_count() for d in self.documents)

    def find_by_title(self, title):
        for d in self.documents:
            if d.title == title:
                return d
        return None


# ──────────────────────────────────────────────
# Exercise 3: DocumentChunk — Inheritance
# ──────────────────────────────────────────────
# TODO: Define DocumentChunk that INHERITS from Document.
# It adds chunk_id and page_number in __init__.
# Call super().__init__(title, content) to reuse Document's setup.
# Override summary(self) to include chunk_id and page_number.

class DocumentChunk(Document):
    def __init__(self, title, content, chunk_id, page_number):
        super().__init__(title, content)
        self.chunk_id = chunk_id
        self.page_number = page_number

    def summary(self):
        return (f"Title: {self.title}, Chunk: {self.chunk_id}, "
                f"Page: {self.page_number}, Words: {self.word_count()}")


# ──────────────────────────────────────────────
# Exercise 4: Build a mini RAG pipeline
# ──────────────────────────────────────────────
# TODO: Define RAGPipeline that:
#   - __init__ creates a DocumentProcessor
#   - ingest(self, title, content) creates a Document and adds to processor
#   - search(self, keyword) returns all Documents where keyword in content
#   - stats(self) prints: total docs, total words, avg words per doc

class RAGPipeline:
    def __init__(self):
        self.processor = DocumentProcessor()

    def ingest(self, title, content):
        doc = Document(title, content)
        self.processor.add(doc)

    def search(self, keyword):
        return [d for d in self.processor.documents if keyword in d.content]

    def stats(self):
        docs = len(self.processor.documents)
        words = self.processor.total_words()
        avg = round(words / docs, 1) if docs > 0 else 0
        print(f"Docs: {docs}, Words: {words}, Avg: {avg}")


# ══════════════════════════════════════════════
# TESTS — run this file to check your work
# ══════════════════════════════════════════════
if __name__ == "__main__":
    passed = 0
    total = 0

    # Exercise 1
    total += 1
    try:
        d = Document("RAG", "Hello world")
        assert d.title == "RAG"
        assert d.word_count() == 2
        assert "RAG" in d.summary() and "2" in d.summary()
        passed += 1
        print("  ✅ Ex1: Document")
    except Exception as e:
        print(f"  ❌ Ex1: Document — {e}")

    # Exercise 2
    total += 1
    try:
        dp = DocumentProcessor()
        dp.add(Document("Doc1", "one two"))
        dp.add(Document("Doc2", "three four five"))
        assert dp.total_words() == 5
        found = dp.find_by_title("Doc1")
        assert found is not None and found.title == "Doc1"
        assert dp.find_by_title("Nope") is None
        passed += 1
        print("  ✅ Ex2: DocumentProcessor")
    except Exception as e:
        print(f"  ❌ Ex2: DocumentProcessor — {e}")

    # Exercise 3
    total += 1
    try:
        dc = DocumentChunk("Chunk1", "some text", chunk_id=1, page_number=3)
        assert dc.title == "Chunk1"
        assert dc.word_count() == 2
        assert dc.chunk_id == 1
        assert dc.page_number == 3
        assert "Chunk1" in dc.summary()
        passed += 1
        print("  ✅ Ex3: DocumentChunk")
    except Exception as e:
        print(f"  ❌ Ex3: DocumentChunk — {e}")

    # Exercise 4
    total += 1
    try:
        pipe = RAGPipeline()
        pipe.ingest("RAG", "retrieval augmented generation")
        pipe.ingest("SQL", "structured query language")
        pipe.ingest("GCP", "google cloud platform")
        results = pipe.search("cloud")
        assert len(results) == 1
        assert results[0].title == "GCP"
        passed += 1
        print("  ✅ Ex4: RAGPipeline")
    except Exception as e:
        print(f"  ❌ Ex4: RAGPipeline — {e}")

    print(f"\n{'='*40}")
    print(f"  Score: {passed}/{total}")
    print(f"{'='*40}")
