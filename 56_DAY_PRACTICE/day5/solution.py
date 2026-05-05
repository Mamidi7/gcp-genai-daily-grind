# Day 5 Solution: JSON + File I/O
# Simple style — one concept at a time, your world

import json
import os


# ================================================================
# SOLUTION 1: Read a JSON file
# ================================================================

def read_doctor_profile(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return data


# ================================================================
# SOLUTION 2: Write a JSON file
# ================================================================

def save_campaign_report(filepath, doctor_id, leads, spend):
    report = {
        "doctor_id": doctor_id,
        "leads_generated": leads,
        "spend": spend,
        "roi": round(leads * 500 / spend, 2)  # rough ROI calc
    }
    with open(filepath, "w") as f:
        json.dump(report, f, indent=2)


# ================================================================
# SOLUTION 3: Check if file exists
# ================================================================

def report_ready(filepath):
    return os.path.exists(filepath)


# ================================================================
# SOLUTION 4: List all files in a folder
# ================================================================

def list_campaign_files(folder_path):
    all_files = os.listdir(folder_path)
    data_files = []
    for f in all_files:
        if f.endswith(".json") or f.endswith(".txt"):
            data_files.append(f)
    return data_files


# ================================================================
# SOLUTION 5: Parse pipe-delimited text file
# ================================================================

def count_interested_leads(filepath):
    count = 0
    with open(filepath, "r") as f:
        lines = f.readlines()

    for line in lines[1:]:  # Skip header row
        parts = line.strip().split("|")
        if parts[3] == "yes":
            count += 1

    return count


# ================================================================
# RUNNER
# ================================================================

if __name__ == "__main__":
    DATA_DIR = "data"

    print("=" * 50)
    print("DAY 5 SOLUTION — Your World Edition")
    print("=" * 50)

    # Ex1: Read JSON
    profile = read_doctor_profile(os.path.join(DATA_DIR, "doctor_profiles.json"))
    print(f"\n1. Loaded {len(profile['doctors'])} doctors")
    for doc in profile["doctors"]:
        status = "✅ Active" if doc["campaign_active"] else "❌ Paused"
        print(f"   {status}: {doc['name']} — Rs.{doc['monthly_budget']}")

    # Ex2: Write JSON
    report_path = os.path.join(DATA_DIR, "test_report.json")
    save_campaign_report(report_path, "DOC001", 45, 25000)
    print(f"\n2. Report saved: {report_path}")
    with open(report_path, "r") as f:
        print(f"   Content:\n   {f.read()}")

    # Ex3: Check if exists
    exists = report_ready(report_path)
    print(f"\n3. Report ready: {exists}")

    # Ex4: List files
    files = list_campaign_files(DATA_DIR)
    print(f"\n4. Data files ({len(files)}):")
    for f in files:
        print(f"   - {f}")

    # Ex5: Count interested leads
    interested = count_interested_leads(os.path.join(DATA_DIR, "leads_response_2024_05.txt"))
    print(f"\n5. Interested leads: {interested}")
    print(f"   (Out of 5 total leads)")

    print("\n" + "=" * 50)
    print("ALL 5 EXERCISES COMPLETE!")
    print("=" * 50)
