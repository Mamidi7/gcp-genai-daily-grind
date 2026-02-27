# Day 4: Classes + OOP Solutions

import json


# Exercise 1: Basic Document Class
class Document:
    def __init__(self, title, content, metadata=None):
        self.title = title
        self.content = content
        self.metadata = metadata if metadata is not None else {}

    def word_count(self):
        """Return the number of words in the content"""
        return len(self.content.split())

    def to_dict(self):
        """Convert document to dictionary"""
        return {
            "title": self.title,
            "content": self.content,
            "metadata": self.metadata
        }


# Exercise 2: from_json Class Method
class DocumentWithJson(Document):
    @classmethod
    def from_json(cls, json_str):
        """Create Document from JSON string"""
        data = json.loads(json_str)
        return cls(
            title=data.get("title", ""),
            content=data.get("content", ""),
            metadata=data.get("metadata", {})
        )


# Alternative: add from_json to original class
# Document.from_json = classmethod(lambda cls, json_str: cls(**json.loads(json_str)))


# Exercise 3: DocumentProcessor
class DocumentProcessor:
    def __init__(self):
        self.documents = []

    def add_document(self, doc):
        """Add a document to the processor"""
        self.documents.append(doc)

    def get_by_title(self, title):
        """Find document by title"""
        for doc in self.documents:
            if doc.title == title:
                return doc
        return None

    def total_words(self):
        """Return total words across all documents"""
        return sum(doc.word_count() for doc in self.documents)


# Exercise 4: Testing Your Classes
if __name__ == "__main__":
    # Test Exercise 1 & 2
    doc = Document("RAG Introduction", "Retrieval Augmented Generation combines...", {"author": "Krishna"})
    print(f"Word count: {doc.word_count()}")
    print(f"Document: {doc.to_dict()}")

    # Test from_json
    json_str = '{"title": "Test", "content": "Hello world", "metadata": {"page": 1}}'
    doc2 = DocumentWithJson.from_json(json_str)
    print(f"From JSON: {doc2.title}")

    # Test DocumentProcessor
    processor = DocumentProcessor()
    processor.add_document(doc)
    processor.add_document(doc2)
    words: {processor.total_words()}")
 print(f"Total