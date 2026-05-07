"""
Day 5: JSON + File I/O
5 exercises. Each one concept. No metaphors.

Run: python3 exercises.py
After filling in all 5, all tests should pass.
"""

import json
import os

DATA = "data"


# ================================================================
# EXERCISE 1: Read a text file
# ================================================================
# Concept: with open("r") reads a file safely
# Why: You need to load the content of a file from disk

def read_file(path):
    """
    Read and return the entire content of a text file.

    Example:
        content = read_file("data/notes.txt")
        print(content)  # prints the whole file
    """
    with open(path, "r") as f:
        return f.read()


# ================================================================
# EXERCISE 2: Write a JSON file
# ================================================================
# Concept: json.dump() saves a Python dict as a JSON file
# Why: You want to save settings or data in a readable format

def save_settings(path, settings_dict):
    
    """
    Save settings dict to a JSON file with indent=2.

    Example:
        save_settings("data/config.json", {"theme": "dark", "lang": "en"})
        # Creates readable JSON file
    """
    with open(path, "w") as f:
        json.dump(settings_dict, f, indent=2)


# ================================================================
# EXERCISE 3: Read a JSON file
# ================================================================
# Concept: json.load() reads JSON file -> Python dict
# Why: Load saved settings or data from disk

def load_settings(path):
    """
    Read a JSON file and return as Python dict.

    Example:
        settings = load_settings("data/config.json")
        print(settings["theme"])  # "dark"
    """
    with open(path, "r") as f:
        return json.load(f)


# ================================================================
# EXERCISE 4: Check if a file exists
# ================================================================
# Concept: os.path.exists() returns True if file is on disk
# Why: Don't try to read a file that doesn't exist yet

def file_exists(path):
    """
    Return True if path exists, False otherwise.

    Example:
        if file_exists("data/config.json"):
            settings = load_settings("data/config.json")
        else:
            print("No settings file yet")
    """
    return os.path.exists(path)


# ================================================================
# EXERCISE 5: List files in a folder
# ================================================================
# Concept: os.listdir() returns all filenames in a folder
# Why: See what files are available before processing them

def list_json_files(folder):
    """
    Return list of all .json filenames in the folder.

    Example:
        files = list_json_files("data")
        print(files)  # ["config.json", "todos.json", ...]
    """
    all_files = os.listdir(folder)
    return [f for f in all_files if f.endswith(".json")]


# ================================================================
# TESTS
# ================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("DAY 5 EXERCISES")
    print("=" * 50)

    # Ex 1
    try:
        content = read_file(f"{DATA}/grades.csv")
        if content and "Alice" in content:
            print("  ✅ Ex1: read_file works")
        else:
            print("  ❌ Ex1: return f.read()")
    except Exception as e:
        print(f"  ❌ Ex1: {e}")

    # Ex 2
    try:
        save_settings(f"{DATA}/test_settings.json", {"theme": "light", "font_size": 16})
        if os.path.exists(f"{DATA}/test_settings.json"):
            print("  ✅ Ex2: save_settings works")
        else:
            print("  ❌ Ex2: use json.dump(settings_dict, f, indent=2)")
    except Exception as e:
        print(f"  ❌ Ex2: {e}")

    # Ex 3
    try:
        s = load_settings(f"{DATA}/config.json")
        if s and isinstance(s, dict) and "theme" in s:
            print(f"  ✅ Ex3: load_settings works -- theme is '{s['theme']}'")
        else:
            print("  ❌ Ex3: return json.load(f)")
    except Exception as e:
        print(f"  ❌ Ex3: {e}")

    # Ex 4
    try:
        if file_exists(f"{DATA}/config.json"):
            print("  ✅ Ex4: file_exists works")
        else:
            print("  ❌ Ex4: return os.path.exists(path)")
    except Exception as e:
        print(f"  ❌ Ex4: {e}")

    # Ex 5
    try:
        files = list_json_files(DATA)
        if files and len(files) > 0:
            print(f"  ✅ Ex5: list_json_files -- found {len(files)} files")
            for f in sorted(files):
                print(f"       {f}")
        else:
            print("  ❌ Ex5: return filtered list of .json files")
    except Exception as e:
        print(f"  ❌ Ex5: {e}")

    print("=" * 50)
    print("ALL 5 EXERCISES PASSED ✅")
