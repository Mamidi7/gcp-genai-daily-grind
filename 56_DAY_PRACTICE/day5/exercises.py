# Day 5 Exercises: JSON + File I/O
# Simple style — one concept at a time, your world
# Build these one by one. Each function = one concept.

import json
import os

# ================================================================
# EXERCISE 1: Read a JSON file
# Concept: with open() + json.load()
# Your world: Read Dr. Sunder's profile from disk
# ================================================================

def read_doctor_profile(filepath):
    """
    Read a JSON file and return the full dict.

    Usage:
        data = read_doctor_profile("data/doctor_profiles.json")
        print(data["doctors"][0]["name"])  # Dr. Sunder Narasimhan
    """
    # Step 1: Open the file in read mode
    # Step 2: json.load() to convert to dict
    # Step 3: Return the dict
    pass


# ================================================================
# EXERCISE 2: Write a JSON file
# Concept: with open("w") + json.dump(indent=2)
# Your world: Save Dr. Sunder's campaign report
# ================================================================

def save_campaign_report(filepath, doctor_id, leads, spend):
    """
    Save a campaign report to JSON file with indent=2.

    The report dict should look like:
    {
        "doctor_id": "DOC001",
        "leads_generated": 45,
        "spend": 25000,
        "roi": 1.8
    }

    Usage:
        save_campaign_report("report.json", "DOC001", 45, 25000)
        # Creates report.json with readable JSON inside
    """
    # Step 1: Build the report dict
    # Step 2: Open filepath in write mode ("w")
    # Step 3: json.dump() with indent=2
    pass


# ================================================================
# EXERCISE 3: Check if file exists
# Concept: os.path.exists()
# Your world: Before emailing report to Dr. Sunder
# ================================================================

def report_ready(filepath):
    """
    Return True if file exists, False otherwise.

    Usage:
        if report_ready("report_doc001.json"):
            send_email("Dr. Sunder")
        else:
            print("Still generating...")
    """
    # One line: return os.path.exists(filepath)
    pass


# ================================================================
# EXERCISE 4: List all files in a folder
# Concept: os.listdir() + filtering
# Your world: See all campaign data files
# ================================================================

def list_campaign_files(folder_path):
    """
    Return list of all .json and .txt files in the folder.

    Usage:
        files = list_campaign_files("data")
        print(files)
        # ['doctor_profiles.json', 'bank_transactions.json', ...]
    """
    # Step 1: os.listdir(folder_path) to get all files
    # Step 2: Filter for .json or .txt
    # Step 3: Return the filtered list
    pass


# ================================================================
# EXERCISE 5: Parse pipe-delimited text file
# Concept: readlines() + split() + skip header
# Your world: Process call center lead responses
# ================================================================

def count_interested_leads(filepath):
    """
    Read a pipe-delimited text file and count leads who said "yes".

    File format:
    LEAD_ID|NAME|PHONE|INTERESTED|DOCTOR_ID
    L001|Ramesh|9876543210|yes|DOC001

    Usage:
        count = count_interested_leads("data/leads_response_2024_05.txt")
        print(count)  # 3
    """
    # Step 1: with open() read all lines
    # Step 2: Skip first line (header) with lines[1:]
    # Step 3: For each line, split by "|"
    # Step 4: If parts[3] == "yes", count += 1
    # Step 5: Return the count
    pass


# ================================================================
# RUNNER
# ================================================================

if __name__ == "__main__":
    DATA_DIR = "data"

    print("=" * 50)
    print("DAY 5 EXERCISES — Your World Edition")
    print("=" * 50)

    # Exercise 1: Read JSON file
    print("\n--- Exercise 1: Read JSON file ---")
    try:
        profile = read_doctor_profile(os.path.join(DATA_DIR, "doctor_profiles.json"))
        if profile and isinstance(profile, dict) and "doctors" in profile:
            print(f"  ✅ Loaded {len(profile['doctors'])} doctors")
            print(f"     First: {profile['doctors'][0]['name']}")
        else:
            print("  ❌ Fix: return the dict from json.load()")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # Exercise 2: Write JSON file
    print("\n--- Exercise 2: Write JSON file ---")
    try:
        report_path = os.path.join(DATA_DIR, "test_report.json")
        save_campaign_report(report_path, "DOC001", 45, 25000)
        if os.path.exists(report_path):
            print(f"  ✅ Report saved at {report_path}")
        else:
            print("  ❌ Fix: use json.dump(data, f, indent=2)")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # Exercise 3: Check file exists
    print("\n--- Exercise 3: os.path.exists ---")
    try:
        if report_ready(report_path):
            print(f"  ✅ report_ready() returned True correctly")
        else:
            print("  ❌ Fix: return os.path.exists(filepath)")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # Exercise 4: List files in folder
    print("\n--- Exercise 4: List files in folder ---")
    try:
        files = list_campaign_files(DATA_DIR)
        if files is None:
            print("  ❌ Fix: return the filtered list")
        elif len(files) > 0:
            print(f"  ✅ Found {len(files)} data files:")
            for f in sorted(files):
                print(f"     - {f}")
        else:
            print("  ❌ Fix: filter for .json or .txt files")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # Exercise 5: Parse pipe-delimited text
    print("\n--- Exercise 5: Parse pipe-delimited text ---")
    try:
        interested = count_interested_leads(os.path.join(DATA_DIR, "leads_response_2024_05.txt"))
        if interested == 3:
            print(f"  ✅ Counted {interested} interested leads (correct!)")
        else:
            print(f"  ❌ Got {interested}, expected 3")
            print("  💡 Hint: skip header with lines[1:], split by '|'")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    print("\n" + "=" * 50)
    print("Fill in the pass statements and test again!")
    print("=" * 50)
