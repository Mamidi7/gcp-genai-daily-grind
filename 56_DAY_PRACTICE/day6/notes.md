# Day 6 Notes: Classes + OOP

## What I Learned Today

### Key Concepts

1. **class** - Blueprint for creating objects
2. **__init__** - Constructor that runs when you create an object
3. **self** - Reference to the current object instance
4. **@classmethod** - Alternative constructor, takes cls instead of self

### Your Document Class

The code you wrote:

```python
class Document:
    def __init__(self, title, content, metadata=None):
        self.title = title
        self.content = content
        self.metadata = metadata if metadata else {}

    def to_dict(self):
        return {"title": self.title, "content": self.content, "metadata": self.metadata}

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
```

### Common Mistakes

- ❌ Forgetting `self.` when accessing attributes
- ❌ Putting `@classmethod` before `def` incorrectly
- ❌ Not handling `metadata=None` properly (use `if metadata else {}`)

## Interview Punch

> "A class is a blueprint. Think of it like a movie script — you can cast unlimited actors (objects) from one script!"

## Questions to Review

- [ ] Can you create a class with __init__?
- [ ] Do you understand self?
- [ ] Can you use @classmethod?
- [ ] Can you explain when to use classmethod vs regular method?

## Tomorrow: REST APIs! 🌐

Day 7 = Calling Gemini with requests!
