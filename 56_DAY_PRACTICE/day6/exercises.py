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
        return cls(
            title=json_data.get("title", ""),
            content=json_data.get("content", ""),
            metadata=json_data.get("metadata", {})
        )


# Exercise 2: Create a Car class
class Car:
    """Create a Car class with brand, color, miles"""
    def __init__(self,brand,color,miles=0):
        self.brand=brand
        self.color=color
        self.miles=miles
    def drive(self,distance):
        self.miles+=distance
        return self.miles
    def repaint(self,color):
        self.color=color
    def describe(self):
        return f"{self.brand} {self.color} with {self.miles} miles"
    # TODO: Add __init__(brand, color, miles=0)
    # TODO: Add drive(distance) method - adds to miles
    # TODO: Add repaint(new_color) method - changes color
    # TODO: Add describe() method - returns string with all info


# Exercise 3: Create a Book class
class Book:
    """Create a Book class for a library system"""
    def __init__(self,title,author,pages):
        self.title=title
        self.author=author
        self.pages=pages
    def is_long_read(self):
        return self.pages>300
    def get_info(self):
        return f"{self.title} by {self.author} ({self.pages} pages)"

    @classmethod
    def from_string(cls, text):
        """Parse 'Title by Author (pages pages)' format"""
        # Split on " by " and " (pages)" markers
        parts = text.replace(" by ", "|").replace(" (", "|").replace(" pages)", "").split("|")
        return cls(
            title=parts[0],
            author=parts[1],
            pages=int(parts[2])
        )

