"""
Day 3: Functions - Practice Exercises
=======================================

Complete these challenges to master functions in Python.
These are the skills you need for building RAG systems.
"""

# ============================================
# EXERCISE 1: Basic Function
# ============================================

def greet(name):
    """
    Return a greeting message.

    Args:
        name: The person's name

    Returns:
        str: Greeting message
    """
    # TODO: Return "Hello, {name}!"
    pass


# ============================================
# EXERCISE 2: Default Parameters
# ============================================

def create_user(username, role="user", active=True):
    """
    Create a user dictionary with default values.

    Args:
        username: The username
        role: User role (default: "user")
        active: Is user active? (default: True)

    Returns:
        dict: User dictionary
    """
    # TODO: Return {'username': ..., 'role': ..., 'active': ...}
    pass


# ============================================
# EXERCISE 3: *args
# ============================================

def calculate_average(*args):
    """
    Calculate the average of all numbers passed.

    Args:
        *args: Variable number of numbers

    Returns:
        float: Average of numbers, or 0 if no numbers
    """
    # TODO: Sum all args, divide by count
    pass


# ============================================
# EXERCISE 4: **kwargs
# ============================================

def build_config(**kwargs):
    """
    Build a configuration dictionary.

    Args:
        **kwargs: Variable keyword arguments

    Returns:
        dict: Configuration with all provided options
    """
    # TODO: Return the kwargs dict as-is
    pass


# ============================================
# EXERCISE 5: chunk_text (THE IMPORTANT ONE)
# ============================================

def chunk_text(text, size=512):
    """
    Split text into chunks of approximately 'size' characters.

    This is THE foundational function for RAG systems.
    Every document needs to be split before it can be indexed.

    Args:
        text (str): Input string to chunk
        size (int): Maximum characters per chunk (default 512)

    Returns:
        list: List of text chunks

    Example:
        >>> chunk_text("HelloWorld", size=5)
        ['Hello', 'Worl', 'd']
    """
    chunks = []

    # TODO: Implement chunking logic
    # Hint: Use range(0, len(text), size)
    # Hint: Use text[i:i+size] for slicing

    return chunks


# ============================================
# TEST YOUR SOLUTIONS
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Day 3 Exercises")
    print("=" * 50)

    # Test 1
    print("\n1. greet():")
    result = greet("Krishna")
    print(f"   greet('Krishna') = '{result}'")
    assert result == "Hello, Krishna!", "Test 1 failed"
    print("   ✅ Passed")

    # Test 2
    print("\n2. create_user():")
    user1 = create_user("john")
    user2 = create_user("jane", "admin")
    print(f"   create_user('john') = {user1}")
    print(f"   create_user('jane', 'admin') = {user2}")
    assert user1 == {'username': 'john', 'role': 'user', 'active': True}, "Test 2a failed"
    assert user2 == {'username': 'jane', 'role': 'admin', 'active': True}, "Test 2b failed"
    print("   ✅ Passed")

    # Test 3
    print("\n3. calculate_average():")
    avg1 = calculate_average(10, 20, 30)
    avg2 = calculate_average(5, 15)
    print(f"   average(10, 20, 30) = {avg1}")
    print(f"   average(5, 15) = {avg2}")
    assert avg1 == 20.0, "Test 3a failed"
    assert avg2 == 10.0, "Test 3b failed"
    print("   ✅ Passed")

    # Test 4
    print("\n4. build_config():")
    config = build_config(model="gemini", temperature=0.7)
    print(f"   build_config(model='gemini', temperature=0.7) = {config}")
    assert config == {'model': 'gemini', 'temperature': 0.7}, "Test 4 failed"
    print("   ✅ Passed")

    # Test 5
    print("\n5. chunk_text():")
    chunks1 = chunk_text("HelloWorld", size=5)
    chunks2 = chunk_text("The quick brown fox", size=10)
    print(f"   chunk_text('HelloWorld', size=5) = {chunks1}")
    print(f"   chunk_text('The quick brown fox', size=10) = {chunks2}")
    assert chunks1 == ['Hello', 'Worl', 'd'], f"Test 5a failed: {chunks1}"
    assert len(chunks2) >= 3, f"Test 5b failed: {chunks2}"
    print("   ✅ Passed")

    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 50)
