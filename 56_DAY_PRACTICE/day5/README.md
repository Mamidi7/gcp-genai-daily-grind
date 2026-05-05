# 📄 Day 5: JSON + File I/O — Your World Edition

## Mission
Master reading/writing files and JSON — the backbone of every data pipeline you will build.

## Your Context (Not Generic BS)
- **Dr. Sunder Narasimhan** — vascular surgeon at Apollo Bangalore
- **Lead generation system** — reads doctor profiles, processes leads, saves reports
- **Banking ETL** — transaction exports in JSON, status filtering
- **Call center data** — pipe-delimited text files with lead responses

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `data/doctor_profiles.json` | 3 doctors, campaign budgets, targets |
| `data/bank_transactions.json` | 5 transactions with status |
| `data/leads_response_2024_05.txt` | 5 leads from call center |
| `exercises.py` | 7 TODOs for you to fill |
| `solution.py` | Complete working solution |
| `CONCEPT_DAY05.md` | Concepts + interview answers |
| `debug_and_interview.py` | 5 real bugs + STAR stories |

---

## Quick Start

```bash
# 1. Run the solution to see what success looks like
cd day5
python solution.py

# 2. Open exercises.py, fill in the 7 TODO functions
# 3. Uncomment the runner at the bottom of exercises.py
# 4. Run your code: python exercises.py

# 5. Read CONCEPT_DAY05.md for interview framing
# 6. Read debug_and_interview.py for common mistakes
```

---

## 7 Exercises (Your World)

1. **get_active_doctors** — Which doctors have active campaigns?
2. **get_total_budget** — Sum all monthly budgets
3. **save_campaign_report** — Write report JSON with indent=2
4. **get_failed_transactions** — Find failed bank payments
5. **report_exists** — Check if file exists before sending to client
6. **list_data_files** — Show all .json and .txt files
7. **count_interested_leads** — Parse pipe-delimited text, count "yes" responses

---

## Key Concepts

| Pattern | Your Use Case |
|---------|---------------|
| `with open(...) as f:` | Read doctor profiles safely |
| `json.load(f)` | Convert JSON file to Python dict |
| `json.dump(data, f, indent=2)` | Save campaign report |
| `os.path.exists()` | Check if report is ready before email |
| `os.listdir()` | List all campaign data files |
| `os.path.join()` | Cross-platform file paths |

---

## Interview Punch

> "For Dr. Sunder's lead generation, I built a data pipeline using Python's json and os modules. I read doctor profiles from JSON, parsed pipe-delimited lead responses from call centers, and saved campaign reports back to JSON. I used `with open()` to prevent file handle leaks and `os.path.exists()` for safe file operations."

---

*Thaggedhe Le* 🔥
