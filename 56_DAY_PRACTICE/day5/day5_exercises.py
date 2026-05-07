"""
Day 5: JSON + File I/O
5 exercises. Each one concept. Each one connected to real GCP/AI work.

Run: python3 exercises.py
All 5 tests pass when you fill every `pass`.
"""

import json
import os

DATA = "data"


# ================================================================
# EXERCISE 1: Read a raw Gemini-style response file
# ================================================================
# Concept: with open("r") + f.read() loads file content as a string
# Why: When you save a Gemini API response to disk for testing/debugging,
#      you reload it with read(). You will do this constantly in Days 10-15
#      when you build offline test suites without hitting the live API.

def read_raw_response(path):
    """
    Read and return the entire content of a file as a string.

    Example:
        raw = read_raw_response("data/gemini_response.json")
        print(type(raw))   # <class 'str'>
        print(raw[:50])    # '{"candidates": [{"content": {"parts": [{"text":'
    """
    with open(path, "r") as f:
        return f.read()


# ================================================================
# EXERCISE 2: Save a model config to disk
# ================================================================
# Concept: json.dump(dict, file, indent=2) saves Python dict as readable JSON
# Why: Your FastAPI service on Cloud Run loads model settings from a config file
#      at startup. You need to be able to write that config from code —
#      not edit JSON by hand every time you change a parameter.

def save_model_config(path, config):
    """
    Save a model configuration dict as a formatted JSON file.

    Example:
        cfg = {
            "model_name": "gemini-1.5-flash",
            "temperature": 0.1,
            "max_output_tokens": 1024,
            "project_id": "my-gcp-project"
        }
        save_model_config("data/model_config.json", cfg)
        # creates a readable, indented JSON file
    """
    with open(path, "w") as f:
        json.dump(config, f, indent=2)


# ================================================================
# EXERCISE 3: Load and extract from a nested JSON response
# ================================================================
# Concept: json.load(f) reads a JSON file into a Python dict.
#          Then you navigate the nested structure with ["key"][index].
# Why: Gemini responses are deeply nested. This is the #1 skill for
#      working with any LLM API. If you can't drill into nested JSON,
#      you can't extract the actual text the model generated.

def extract_generated_text(path):
    """
    Load a Gemini-style JSON response file and return just the generated text.

    The JSON structure looks like this:
    {
      "candidates": [
        {
          "content": {
            "parts": [{"text": "The actual answer here"}]
          }
        }
      ]
    }

    Example:
        text = extract_generated_text("data/gemini_response.json")
        print(text)  # "UPI is Unified Payments Interface..."
    """
    with open(path, "r") as f:
        data = json.load(f)
    return data["candidates"][0]["content"]["parts"][0]["text"]


# ================================================================
# EXERCISE 4: Safe config loader with fallback
# ================================================================
# Concept: os.path.exists() + json.load() with a fallback default
# Why: Production services never crash if a config file is missing.
#      They fall back to safe defaults. This pattern is in EVERY
#      Cloud Run service you will deploy.

def load_config_safe(path, default_config):
    """
    Load config from path if it exists. Return default_config if it doesn't.

    Example:
        defaults = {"model_name": "gemini-1.5-flash", "temperature": 0.1}

        # If file exists:
        cfg = load_config_safe("data/model_config.json", defaults)
        print(cfg["model_name"])   # whatever is in the file

        # If file does NOT exist:
        cfg = load_config_safe("data/nonexistent.json", defaults)
        print(cfg["model_name"])   # "gemini-1.5-flash"  ← fallback
    """
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default_config


# ================================================================
# EXERCISE 5: Scan a folder and load all configs
# ================================================================
# Concept: os.listdir() + filter + json.load in a loop
# Why: In Day 20+ (evals and logging), you'll process folders of
#      saved API responses, eval results, and experiment configs.
#      Batch-loading JSON files from a directory is a daily task.

def load_all_configs(folder):
    """
    Load every .json file in folder and return a dict of filename → config.

    Example:
        configs = load_all_configs("data")
        # configs = {
        #     "config.json":      {"theme": "dark", "language": "en", ...},
        #     "todos.json":       {"todos": [...]},
        #     "my_settings.json": {"theme": "dark", "notifications": True}
        # }
        print(configs["config.json"]["language"])  # "en"
    """
    all_files = os.listdir(folder)
    json_files = [f for f in all_files if f.endswith(".json")]
    result = {}
    for filename in json_files:
        with open(f"{folder}/{filename}", "r") as f:
            result[filename] = json.load(f)
    return result


# ================================================================
# TESTS
# ================================================================

if __name__ == "__main__":
    print("=" * 55)
    print("DAY 5 EXERCISES — JSON + File I/O")
    print("=" * 55)

    # Ex 1: read raw file
    try:
        raw = read_raw_response(f"{DATA}/grades.csv")
        if raw and "Alice" in raw:
            print("  ✅ Ex1: read_raw_response works")
        else:
            print("  ❌ Ex1: return f.read() — full file as string")
    except Exception as e:
        print(f"  ❌ Ex1: {e}")

    # Ex 2: save model config
    try:
        test_config = {
            "model_name": "gemini-1.5-flash",
            "temperature": 0.1,
            "project_id": "my-gcp-project"
        }
        save_model_config(f"{DATA}/test_model_config.json", test_config)
        if os.path.exists(f"{DATA}/test_model_config.json"):
            with open(f"{DATA}/test_model_config.json") as f:
                saved = json.load(f)
            if saved.get("model_name") == "gemini-1.5-flash":
                print("  ✅ Ex2: save_model_config works")
            else:
                print("  ❌ Ex2: json not written correctly")
        else:
            print("  ❌ Ex2: file not created — use json.dump(config, f, indent=2)")
    except Exception as e:
        print(f"  ❌ Ex2: {e}")

    # Ex 3: extract text from nested Gemini-style JSON
    # First, create a fake Gemini response file for testing
    fake_response = {
        "candidates": [{
            "content": {
                "parts": [{"text": "UPI is Unified Payments Interface, India's real-time payment system."}]
            },
            "finish_reason": "STOP"
        }],
        "usage_metadata": {"prompt_token_count": 5, "candidates_token_count": 18}
    }
    with open(f"{DATA}/gemini_response.json", "w") as f:
        json.dump(fake_response, f, indent=2)

    try:
        text = extract_generated_text(f"{DATA}/gemini_response.json")
        if text and "UPI" in text:
            print(f"  ✅ Ex3: extract_generated_text works")
            print(f"       → '{text[:60]}...'")
        else:
            print("  ❌ Ex3: navigate data['candidates'][0]['content']['parts'][0]['text']")
    except Exception as e:
        print(f"  ❌ Ex3: {e}")

    # Ex 4: safe loader
    try:
        defaults = {"model_name": "gemini-1.5-flash", "temperature": 0.1}

        # Case A: file exists
        existing = load_config_safe(f"{DATA}/config.json", defaults)
        # Case B: file does not exist
        missing = load_config_safe(f"{DATA}/this_does_not_exist.json", defaults)

        if (existing and isinstance(existing, dict) and
                missing and missing["model_name"] == "gemini-1.5-flash"):
            print("  ✅ Ex4: load_config_safe works — handles missing file")
        else:
            print("  ❌ Ex4: check os.path.exists branch and fallback return")
    except Exception as e:
        print(f"  ❌ Ex4: {e}")

    # Ex 5: batch load
    try:
        configs = load_all_configs(DATA)
        if configs and len(configs) >= 2 and all(isinstance(v, dict) for v in configs.values()):
            print(f"  ✅ Ex5: load_all_configs — loaded {len(configs)} JSON files")
            for fname, cfg in sorted(configs.items()):
                print(f"       {fname}: {list(cfg.keys())[:3]}")
        else:
            print("  ❌ Ex5: return dict of {filename: loaded_dict} for each .json")
    except Exception as e:
        print(f"  ❌ Ex5: {e}")

    print("=" * 55)
    print("Fill every `pass`, run again. All 5 should be ✅")
