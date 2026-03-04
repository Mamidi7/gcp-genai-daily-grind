# Day 5 Solutions: JSON, File I/O, os module
import json
import os


# Exercise 1: Read a text file
def read_file(filename):
    """Read and return content of a text file"""
    with open(filename, "r") as f:
        return f.read()


# Exercise 2: Write to a text file
def write_file(filename, content):
    """Write content to a text file"""
    with open(filename, "w") as f:
        f.write(content)


# Exercise 3: Read JSON config
def load_config(filename):
    """Load JSON config from file and return model name"""
    with open(filename, "r") as f:
        config = json.load(f)
    return config.get("model", "gemini-2.0-flash")


# Exercise 4: Save JSON results
def save_results(filename, data):
    """Save data as JSON to file with indent=2"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


# Exercise 5: List all JSON files in folder
def list_json_files(folder_path):
    """Return list of all .json files in folder"""
    files = os.listdir(folder_path)
    return [f for f in files if f.endswith(".json")]


# Exercise 6: Check if file exists
def file_exists(filename):
    """Return True if file exists, False otherwise"""
    return os.path.exists(filename)


# Test all functions
if __name__ == "__main__":
    print("=== Testing Exercises ===\n")

    # Create test files
    write_file("test.txt", "Hello, World!")
    print("Exercise 1: Read file")
    print(read_file("test.txt"))

    print("\nExercise 3: Load JSON config")
    # Create a test config
    test_config = {"model": "gemini-pro", "temperature": 0.5}
    save_results("test_config.json", test_config)
    print("Model:", load_config("test_config.json"))

    print("\nExercise 5: List JSON files")
    print("JSON files:", list_json_files("."))

    print("\nExercise 6: File exists")
    print("test.txt exists?", file_exists("test.txt"))
    print("fake.txt exists?", file_exists("fake.txt"))
