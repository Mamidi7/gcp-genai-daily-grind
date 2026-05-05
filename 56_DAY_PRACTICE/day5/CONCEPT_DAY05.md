# 📄 Day 5: JSON + File I/O — Your World, Simple Style

---

## Concept 1: What is a File?

A file is data stored on your disk. Your computer has hundreds of files.

**Your world examples:**
- `doctor_profiles.json` — stores Dr. Sunder's profile on disk
- `bank_transactions.json` — stores transaction records on disk
- `leads_response_2024_05.txt` — stores lead data from call center

When Python reads a file, it loads that data into memory (RAM).

```
Disk (permanent storage)          RAM (temporary)
┌─────────────────────┐          ┌─────────────────────┐
│ doctor_profiles.json│  ──read──▶│ doctor = { ... }    │
│ bank_transactions.json│          │                     │
│ leads.txt           │          │                     │
└─────────────────────┘          └─────────────────────┘
```

---

## Concept 2: Opening and Closing Files

Python reads files using `open()`.

**Basic pattern:**
```python
f = open("doctor_profiles.json", "r")  # "r" = read mode
data = f.read()
f.close()  # Must close manually!
```

**Problem:** If an error happens between open and close, the file stays open. After processing 1000 files, your script crashes with "Too many open files."

**Fix:** Use `with open()` — it closes automatically, even if an error happens.

```python
with open("doctor_profiles.json", "r") as f:
    data = f.read()
# f is closed automatically here
```

**Your world:** Reading Dr. Sunder's campaign budget from disk:
```python
with open("doctor_profiles.json", "r") as f:
    content = f.read()
print(content)  # Prints the raw text from the file
```

---

**Check 1:** What happens if you open a file but forget to close it, and you run this in a loop 10,000 times?

---

## Concept 3: JSON — Python Dicts as Text

JSON is a text format for storing structured data. It looks exactly like Python dictionaries.

**Your doctor profile as JSON:**
```json
{
  "name": "Dr. Sunder Narasimhan",
  "specialty": "Vascular Surgery",
  "hospital": "Apollo Bangalore",
  "monthly_budget": 50000
}
```

**Same thing as a Python dict:**
```python
doctor = {
    "name": "Dr. Sunder Narasimhan",
    "specialty": "Vascular Surgery",
    "hospital": "Apollo Bangalore",
    "monthly_budget": 50000
}
```

**Why JSON matters:** JSON is readable by any language — Python, JavaScript, Java, Go. Your bank exports data as JSON. Your AI pipeline reads it.

```
Python dict    ──json.dump()──▶    JSON text file
JSON text file ──json.load()──▶    Python dict
```

---

## Concept 4: Reading JSON — json.load()

`json.load()` reads a JSON file and converts it to a Python dict.

```python
import json

with open("doctor_profiles.json", "r") as f:
    data = json.load(f)

print(data)
# Output:
# {
#   "doctors": [
#     {
#       "id": "DOC001",
#       "name": "Dr. Sunder Narasimhan",
#       "monthly_budget": 50000,
#       "campaign_active": True
#     },
#     ...
#   ]
# }
```

Now `data` is a Python dict. You can use it like any dict:

```python
print(data["doctors"][0]["name"])  # "Dr. Sunder Narasimhan"
```

**Your world use:** Get all doctors who have active campaigns:
```python
for doctor in data["doctors"]:
    if doctor["campaign_active"]:
        print(f"{doctor['name']}: Rs.{doctor['monthly_budget']}")
```

---

**Check 2:** What does this print?
```python
with open("doctor_profiles.json", "r") as f:
    d = json.load(f)
print(d["doctors"][1]["campaign_active"])
```
(Look at the data file — DOC002 has `campaign_active: false`)

---

## Concept 5: Writing JSON — json.dump()

`json.dump()` takes a Python dict and saves it as a JSON text file.

```python
import json

report = {
    "doctor_id": "DOC001",
    "leads_generated": 45,
    "spend": 25000,
    "roi": 1.8
}

with open("campaign_report.json", "w") as f:
    json.dump(report, f, indent=2)
```

**What gets written:**
```json
{
  "doctor_id": "DOC001",
  "leads_generated": 45,
  "spend": 25000,
  "roi": 1.8
}
```

**Why indent=2?** Without it, the file is one unreadable line:
```json
{"doctor_id": "DOC001", "leads_generated": 45}
```
With `indent=2`, Dr. Sunder can open the file and read it.

**Your world use:** Save campaign results after processing leads:
```python
with open("report_doc001.json", "w") as f:
    json.dump(report, f, indent=2)
```

---

**Check 3:** You run this code:
```python
with open("output.json", "w") as f:
    json.dump({"leads": 45}, f)
```
Then you open `output.json` in a text editor. What do you see?

---

## Concept 6: Checking If File Exists — os.path.exists()

Before reading a file, check if it exists to avoid crashes.

```python
import os

if os.path.exists("doctor_profiles.json"):
    with open("doctor_profiles.json", "r") as f:
        data = json.load(f)
else:
    print("File not found!")
```

**Your world use:** Before emailing Dr. Sunder his report, check it exists:
```python
if os.path.exists("report_doc001.json"):
    send_email("Dr. Sunder", "report_doc001.json")
else:
    print("Report not ready yet!")
```

---

## Concept 7: Listing Files — os.listdir()

```python
import os

files = os.listdir("data/")
print(files)
# ['doctor_profiles.json', 'bank_transactions.json', 'leads_response_2024_05.txt']
```

**Filter for specific types:**
```python
json_files = [f for f in os.listdir("data/") if f.endswith(".json")]
print(json_files)
# ['doctor_profiles.json', 'bank_transactions.json']
```

---

## Concept 8: Reading Text Files Line by Line

Some data comes as plain text, not JSON. Like your call center lead responses:

```
LEAD_ID|NAME|PHONE|INTERESTED|DOCTOR_ID
L001|Ramesh|9876543210|yes|DOC001
L002|Suresh|9876543211|no|DOC001
```

```python
with open("leads_response_2024_05.txt", "r") as f:
    lines = f.readlines()  # Returns list of lines

for line in lines:  # Loop through each line
    print(line.strip())  # strip() removes \n at the end
```

**Split by pipe (|):**
```python
for line in lines[1:]:  # Skip header (first line)
    parts = line.strip().split("|")
    # parts = ["L001", "Ramesh", "9876543210", "yes", "DOC001"]
    print(f"{parts[1]} is interested: {parts[3]}")
```

**Your world use:** Count how many leads said "yes":
```python
interested = 0
for line in lines[1:]:
    parts = line.strip().split("|")
    if parts[3] == "yes":
        interested += 1
print(f"Interested leads: {interested}")  # 3
```

---

**Check 4:** What happens if you do `lines` instead of `lines[1:]` in the loop above?

---

## Summary Table

```
┌─────────────────────┬──────────────────────────────────────────┐
│      Concept        │              Your World Use              │
├─────────────────────┼──────────────────────────────────────────┤
│ with open("f","r")  │ Read doctor profiles from disk            │
├─────────────────────┼──────────────────────────────────────────┤
│ with open("f","w")  │ Save campaign report to disk             │
├─────────────────────┼──────────────────────────────────────────┤
│ json.load(f)        │ Convert JSON file → Python dict          │
├─────────────────────┼──────────────────────────────────────────┤
│ json.dump(d, f,     │ Convert Python dict → JSON file           │
│      indent=2)      │ indent=2 makes it readable               │
├─────────────────────┼──────────────────────────────────────────┤
│ os.path.exists()    │ Check if report exists before emailing   │
├─────────────────────┼──────────────────────────────────────────┤
│ os.listdir()        │ List all data files in folder            │
├─────────────────────┼──────────────────────────────────────────┤
│ .split("|")         │ Parse pipe-delimited lead responses      │
├─────────────────────┼──────────────────────────────────────────┤
│ lines[1:]           │ Skip header row when reading text files   │
└─────────────────────┴──────────────────────────────────────────┘
```

---

## Check Answers

**Check 1:** After 10,000 files, your OS runs out of file handles. Error: "Too many open files." Fix: always use `with open()`.

**Check 2:** `False` — DOC002 (Dr. Priya) has `campaign_active: false`.

**Check 3:**
```json
{"leads": 45}
```
One line, no indent.

**Check 4:** The first line is the header `"LEAD_ID|NAME|PHONE|INTERESTED|DOCTOR_ID"`. You'd try to split it and count it as a lead. Use `lines[1:]` to skip the header.
