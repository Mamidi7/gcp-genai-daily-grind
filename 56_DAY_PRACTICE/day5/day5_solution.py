"""
Day 5: Solutions — JSON + File I/O
Run: python3 solution.py
"""

import json
import os

DATA = "data"


def read_raw_response(path):
    with open(path, "r") as f:
        return f.read()


def save_model_config(path, config):
    with open(path, "w") as f:
        json.dump(config, f, indent=2)


def extract_generated_text(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data["candidates"][0]["content"]["parts"][0]["text"]


def load_config_safe(path, default_config):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default_config


def load_all_configs(folder):
    all_files = os.listdir(folder)
    json_files = [f for f in all_files if f.endswith(".json")]
    result = {}
    for filename in json_files:
        with open(f"{folder}/{filename}", "r") as f:
            result[filename] = json.load(f)
    return result


if __name__ == "__main__":
    print("=" * 55)
    print("DAY 5 SOLUTIONS")
    print("=" * 55)

    # 1. Read raw file
    raw = read_raw_response(f"{DATA}/grades.csv")
    lines = raw.strip().split("\n")
    print(f"\n1. read_raw_response → {len(lines)} lines")
    print(f"   First line: {lines[0]}")

    # 2. Save model config
    config = {
        "model_name": "gemini-1.5-flash",
        "temperature": 0.1,
        "max_output_tokens": 1024,
        "project_id": "my-banking-ai-project"
    }
    save_model_config(f"{DATA}/model_config.json", config)
    print(f"\n2. save_model_config → model_config.json written")
    print(f"   model: {config['model_name']}, temp: {config['temperature']}")

    # 3. Extract text from nested Gemini response
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

    text = extract_generated_text(f"{DATA}/gemini_response.json")
    print(f"\n3. extract_generated_text → '{text}'")

    # 4. Safe config loader
    defaults = {"model_name": "gemini-1.5-flash", "temperature": 0.1}
    loaded = load_config_safe(f"{DATA}/config.json", defaults)
    missing = load_config_safe(f"{DATA}/does_not_exist.json", defaults)
    print(f"\n4. load_config_safe:")
    print(f"   config.json found → {list(loaded.keys())}")
    print(f"   missing file      → fell back to defaults: {list(missing.keys())}")

    # 5. Batch load all JSON files
    configs = load_all_configs(DATA)
    print(f"\n5. load_all_configs → {len(configs)} JSON files in data/")
    for fname, cfg in sorted(configs.items()):
        print(f"   {fname}: {list(cfg.keys())}")

    print(f"\n{'='*55}")
    print("All working. Day 5 complete.")
    print()
    print("Next: Day 6 — these patterns appear inside every")
    print("function you write from here on. Open any Gemini")
    print("example online and you'll see json.loads() in the")
    print("first 10 lines.")
