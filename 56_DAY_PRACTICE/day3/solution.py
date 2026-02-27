"""
Day 3: Functions - Solutions
============================
"""


# ============================================
# EXERCISE 1: Basic Function
# ============================================

def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"


# ============================================
# EXERCISE 2: Default Parameters
# ============================================

def create_user(username, role="user", active=True):
    """Create a user dictionary with default values."""
    return {
        'username': username,
        'role': role,
        'active': active
    }


# ============================================
# EXERCISE 3: *args
# ============================================

def calculate_average(*args):
    """Calculate the average of all numbers passed."""
    if not args:
        return 0
    return sum(args) / len(args)


# ============================================
# EXERCISE 4: **kwargs
# ============================================

def build_config(**kwargs):
    """Build a configuration dictionary."""
    return kwargs


# ============================================
# EXERCISE 5: chunk_text (THE IMPORTANT ONE)
# ============================================

def chunk_text(text, size=512):
    """
    Split text into chunks of approximately 'size' characters.

    This is THE foundational function for RAG systems.
    """
    if not text:
        return []

    chunks = []
    for i in range(0, len(text), size):
        chunk = text[i:i + size]
        chunks.append(chunk)

    return chunks


# ============================================
# BONUS: Word-Boundary Chunking
# ============================================

def chunk_text_by_words(text, max_chars=50):
    """
    Split text into chunks at word boundaries.
    Better for RAG systems!
    """
    if not text:
        return []

    words = text.split()
    chunks = []
    current_chunk = ""

    for word in words:
        # Check if adding this word would exceed limit
        if current_chunk and len(current_chunk) + len(word) + 1 > max_chars:
            chunks.append(current_chunk.strip())
            current_chunk = word
        else:
            current_chunk += " " + word if current_chunk else word

    # Don't forget the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# ============================================
# TEST
# ============================================

if __name__ == "__main__":
    print("Testing solutions...")

    # Test 1
    assert greet("Krishna") == "Hello, Krishna!"
    print("✅ Exercise 1: greet()")

    # Test 2
    assert create_user("john") == {'username': 'john', 'role': 'user', 'active': True}
    assert create_user("jane", "admin") == {'username': 'jane', 'role': 'admin', 'active': True}
    print("✅ Exercise 2: create_user()")

    # Test 3
    assert calculate_average(10, 20, 30) == 20.0
    assert calculate_average() == 0
    print("✅ Exercise 3: calculate_average()")

    # Test 4
    config = build_config(model="gemini", temperature=0.7)
    assert config == {'model': 'gemini', 'temperature': 0.7}
    print("✅ Exercise 4: build_config()")

    # Test 5
    assert chunk_text("HelloWorld", size=5) == ['Hello', 'Worl', 'd']
    assert chunk_text("", size=5) == []
    print("✅ Exercise 5: chunk_text()")

    # Bonus
    result = chunk_text_by_words("The quick brown fox jumps", max_chars=10)
    assert len(result) > 0
    print("✅ Bonus: chunk_text_by_words()")

    print("\n🎉 All solutions correct!")
