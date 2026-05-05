"""
Day 5: Solutions — JSON + File I/O
Run: python3 solution.py
"""

import json
import os

DATA = "data"


def read_file(path):
    with open(path, "r") as f:
        return f.read()


def save_settings(path, settings_dict):
    with open(path, "w") as f:
        json.dump(settings_dict, f, indent=2)


def load_settings(path):
    with open(path, "r") as f:
        return json.load(f)


def file_exists(path):
    return os.path.exists(path)


def list_json_files(folder):
    all_files = os.listdir(folder)
    return [f for f in all_files if f.endswith(".json")]


if __name__ == "__main__":
    print("=" * 50)
    print("DAY 5 SOLUTIONS")
    print("=" * 50)

    # 1. Read grades.csv
    content = read_file(f"{DATA}/grades.csv")
    lines = content.strip().split("\n")
    print(f"\n1. Read file — {len(lines)} lines")
    print(f"   Line 1: {lines[0]}")
    print(f"   Line 2: {lines[1]}")

    # 2. Save settings
    save_settings(f"{DATA}/my_settings.json", {"theme": "dark", "notifications": True})
    print(f"\n2. Saved my_settings.json")

    # 3. Load settings
    s = load_settings(f"{DATA}/config.json")
    print(f"\n3. Loaded config.json:")
    for key, val in s.items():
        print(f"   {key}: {val}")

    # 4. Check exists
    print(f"\n4. file_exists checks:")
    print(f"   config.json exists: {file_exists(f'{DATA}/config.json')}")
    print(f"   nonexistent.json exists: {file_exists(f'{DATA}/nonexistent.json')}")

    # 5. List json files
    files = list_json_files(DATA)
    print(f"\n5. JSON files in data/:")
    for f in sorted(files):
        print(f"   {f}")

    print(f"\n{'='*50}")
    print("ALL WORKING!")
