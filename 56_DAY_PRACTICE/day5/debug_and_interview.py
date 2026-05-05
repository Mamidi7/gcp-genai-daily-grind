# Day 5 Debug Journal + Interview Pack
# JSON + File I/O errors from YOUR WORLD

# ============================================================
# BUG 1: File Not Found When Reading Doctor Profiles
# ============================================================

"""
SYMPTOM:
    FileNotFoundError: [Errno 2] No such file or directory: 'doctor_profiles.json'

ROOT CAUSE:
    Python looks for file in CURRENT WORKING DIRECTORY.
    You ran script from day5/ but file is in day5/data/.

FIX:
    Use correct path: os.path.join("data", "doctor_profiles.json")
    Or use absolute path.

PREVENTION:
    Always use os.path.exists() before reading.
    Use os.path.join() for cross-platform paths.

STAR STORY:
    "In Dr. Sunder's lead gen system, I once hardcoded a path like
    'data/doctor_profiles.json' which worked on Mac but failed on the
    production Linux server. I fixed it by using os.path.join() and
    adding an exists() check with a clear error message. This taught
    me that file paths are a common source of 'works on my machine' bugs."
"""

# ============================================================
# BUG 2: Using json.dump Instead of json.dumps for API
# ============================================================

"""
SYMPTOM:
    TypeError: dump() missing 1 required positional argument: 'fp'

ROOT CAUSE:
    json.dump() needs a FILE object (writes to file).
    json.dumps() returns a STRING (for APIs, printing).

FIX:
    Use json.dumps() when you need a string.
    Use json.dump() when you have a file to write to.

EXAMPLE:
    # Wrong
    payload = json.dump({"doctor": "Dr. Sunder"})  # Needs file!

    # Right
    payload = json.dumps({"doctor": "Dr. Sunder"})  # Returns string

PREVENTION:
    Remember: dump = file, dumps = string.
    's' = string.
"""

# ============================================================
# BUG 3: Forgetting indent Makes JSON Unreadable
# ============================================================

"""
SYMPTOM:
    Report file is one line:
    {"doctor_id":"DOC001","leads":45,"spend":25000}

ROOT CAUSE:
    json.dump(data, f)  # No indent parameter

FIX:
    json.dump(data, f, indent=2)

IMPACT:
    When Dr. Sunder asks for a report, you open the file and it's
    unreadable. With indent=2, anyone can read it in a text editor.

PREVENTION:
    Always use indent=2 for human-readable JSON files.
    Use indent=None only for machine-to-machine communication.
"""

# ============================================================
# BUG 4: Not Closing File (Memory Leak)
# ============================================================

"""
SYMPTOM:
    After processing 10,000 leads, script crashes with
    'Too many open files' error.

ROOT CAUSE:
    f = open("leads.txt", "r")
    data = f.read()
    # Forgot f.close()!

    In a loop processing thousands of files, each open file handle
    stays open until OS limit is hit.

FIX:
    Use with open():
    with open("leads.txt", "r") as f:
        data = f.read()
    # f is closed automatically, even if error occurs

PREVENTION:
    Never use open() without with.
    If you must (rare), always put close() in finally block.
"""

# ============================================================
# BUG 5: Modifying Dict While Iterating
# ============================================================

"""
SYMPTOM:
    RuntimeError: dictionary changed size during iteration

ROOT CAUSE:
    for doctor in doctors:
        if not doctor["active"]:
            doctors.remove(doctor)  # Changing list while looping

FIX:
    Create new list instead:
    active_doctors = [d for d in doctors if d["active"]]

PREVENTION:
    Never modify a collection while iterating over it.
    Use list comprehensions or create new collections.
"""

# ============================================================
# INTERVIEW QUESTIONS (Anticipated)
# ============================================================

"""
Q: What's the difference between json.load() and json.loads()?
A: load() reads from a file object. loads() parses a string.
   's' in loads means string.

Q: Why use 'with open()' instead of just open()?
A: with guarantees file closure via context managers. Even if an
   exception occurs, the file is closed. Prevents resource leaks.

Q: How do you handle a file that might not exist?
A: Check os.path.exists() first, or use try/except FileNotFoundError.
   Always give a clear error message with the expected path.

Q: What's the difference between 'w' and 'a' mode?
A: 'w' overwrites existing content. 'a' appends to the end.
   Use 'w' for fresh reports, 'a' for transaction logs.

Q: How do you read a 10GB file without running out of memory?
A: Don't use read() or readlines(). Iterate line by line:
   for line in open("huge.txt"):  # Memory efficient
       process(line)
"""

# ============================================================
# VERIFY: Run solution.py to confirm all tests pass
# ============================================================

if __name__ == "__main__":
    print("Debug journal loaded.")
    print("Run: python solution.py")
    print("Then try: python exercises.py (fill in the TODOs first)")
