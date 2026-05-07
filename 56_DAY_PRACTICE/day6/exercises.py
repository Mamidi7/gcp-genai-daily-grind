# Day 6 Exercises: Classes + OOP

# Exercise 1: Complete the Document class
# Add the missing methods to the class below

class Document:
    def __init__(self, title, content, metadata=None):
        """Initialize document with title, content, and optional metadata"""
        self.title = title
        self.content = content
        self.metadata = metadata if metadata else {}
        # TODO: Handle metadata default to empty dict if None

    def to_dict(self):
        """Convert document to dictionary"""
        # TODO: Return {"title": ..., "content": ..., "metadata": ...}
        return { "title": self.title,"content":self.content,"metadata":self.metadata}

    def word_count(self):
        """Return number of words in content"""
        # TODO: Split by space and count
        return len(self.content.split())    

    def char_count(self):
        """Return number of characters in content"""
        # TODO: Return len(self.content)
        return len(self.content)

    def summary(self, first_n=100):
        """Return first N characters with '...' if truncated"""
        # TODO: If content <= first_n, return full content
        # Otherwise return content[:first_n] + "..."
        if len(self.content) <= first_n:
            return self.content
        return self.content[:first_n] + "..."

    @classmethod
    def from_json(cls, json_data):
        """Create Document from JSON/dictionary"""
        # TODO: Use cls() to create new Document
        # Extract title, content, metadata from json_data
        pass


# Exercise 2: Create a Car class
class Car:
    """Create a Car class with brand, color, miles"""
    # TODO: Add __init__(brand, color, miles=0)
    # TODO: Add drive(distance) method - adds to miles
    # TODO: Add repaint(new_color) method - changes color
    # TODO: Add describe() method - returns string with all info


# Exercise 3: Create a Book class
class Book:
    """Create a Book class for a library system"""
    # TODO: Add __init__(title, author, pages)
    # TODO: Add is_long_read() - returns True if > 300 pages
    # TODO: Add get_info() - returns formatted string
    # TODO: Add @classmethod from_string(text) that parses "Title by Author (pages pages)"
