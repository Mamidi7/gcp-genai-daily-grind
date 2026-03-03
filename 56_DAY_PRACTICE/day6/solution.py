# Day 6 Solutions: Classes + OOP


# Exercise 1: Document class (COMPLETE)
class Document:
    def __init__(self, title, content, metadata=None):
        self.title = title
        self.content = content
        self.metadata = metadata if metadata else {}

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "metadata": self.metadata
        }

    def word_count(self):
        return len(self.content.split())

    def char_count(self):
        return len(self.content)

    def summary(self, first_n=50):
        if len(self.content) <= first_n:
            return self.content
        return self.content[:first_n] + "..."

    @classmethod
    def from_json(cls, json_data):
        return cls(
            title=json_data.get("title", ""),
            content=json_data.get("content", ""),
            metadata=json_data.get("metadata", {})
        )


# Exercise 2: Car class
class Car:
    def __init__(self, brand, color, miles=0):
        self.brand = brand
        self.color = color
        self.miles = miles

    def drive(self, distance):
        self.miles += distance
        return self.miles

    def repaint(self, new_color):
        self.color = new_color
        return self.color

    def describe(self):
        return f"{self.color} {self.brand} with {self.miles} miles"


# Exercise 3: Book class
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def is_long_read(self):
        return self.pages > 300

    def get_info(self):
        return f"'{self.title}' by {self.author} ({self.pages} pages)"

    @classmethod
    def from_string(cls, text):
        # Parse: "Title by Author (pages pages)"
        # Example: "Harry Potter by J.K. Rowling (500 pages)"
        parts = text.replace(" by ", "|").replace(" (", "|").replace(" pages)", "").split("|")
        title = parts[0]
        author = parts[1]
        pages = int(parts[2])
        return cls(title, author, pages)


# Test all
if __name__ == "__main__":
    print("=== Document Tests ===")
    doc = Document("Test", "Hello world this is a test document")
    print(f"Word count: {doc.word_count()}")
    print(f"Char count: {doc.char_count()}")
    print(f"Summary: {doc.summary(10)}")

    json_doc = Document.from_json({"title": "JSON Doc", "content": "From JSON!"})
    print(f"From JSON: {json_doc.title}")

    print("\n=== Car Tests ===")
    car = Car("Toyota", "Red")
    car.drive(100)
    car.repaint("Blue")
    print(car.describe())

    print("\n=== Book Tests ===")
    book = Book("1984", "George Orwell", 328)
    print(book.get_info())
    print(f"Long read? {book.is_long_read()}")

    book2 = Book.from_string("Sapiens by Yuval Noah Harari (450 pages)")
    print(book2.get_info())
