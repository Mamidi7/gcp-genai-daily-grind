# Day 4: Classes + OOP Exercises

# Exercise 1: Basic Document Class
# Create a Document class with title, content, and metadata attributes

class Document:
    def __init__(self, title, content, metadata=None):
        self.title = title
        self.content = content
        self.metadata = metadata if metadata is not None else {}

    def word_count(self):
        """Return the number of words in the content"""
        pass

    def to_dict(self):
        """Convert document to dictionary"""
        pass


# Exercise 2: from_json Class Method
# Add a class method to create Document from JSON string

    @classmethod
    def from_json(cls, json_str):
        """Create Document from JSON string"""
        # Hint: import json and use json.loads()
        pass


# Exercise 3: DocumentProcessor
# Create a processor that manages multiple documents

class DocumentProcessor:
    def __init__(self):
        self.documents = []

    def add_document(self, doc):
        """Add a document to the processor"""
        pass

    def get_by_title(self, title):
        """Find document by title"""
        pass

    def total_words(self):
        """Return total words across all documents"""
        pass


# Exercise 4: Testing Your Classes
if __name__ == "__main__":
    # Test Exercise 1 & 2
    doc = Document("RAG Introduction", "Retrieval Augmented Generation combines...", {"author": "Krishna"})
    print(f"Word count: {doc.word_count()}")
    print(f"Document: {doc.to_dict()}")

    # Test from_json
    json_str = '{"title": "Test", "content": "Hello world", "metadata": {"page": 1}}'
    doc2 = Document.from_json(json_str)
    print(f"From JSON: {doc2.title}")

    # Test DocumentProcessor
    processor = DocumentProcessor()
    processor.add_document(doc)
    processor.add_document(doc2)
    print(f"Total words: {processor.total_words()}")
