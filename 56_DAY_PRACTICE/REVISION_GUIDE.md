# 🐍 Python Revision Guide — 10th Std Level
## Krishna's GCP AI Journey — Day 1 to [Current Day]

> *"Simple language. Clear concepts. No jargon."*

---

## 📚 Table of Contents

1. [Variables & Data Types](#1-variables--data-types)
2. [f-strings — Putting variables in text](#2-f-strings--putting-variables-in-text)
3. [Lists — Ordered collections](#3-lists--ordered-collections)
4. [Dictionaries — Key-Value pairs](#4-dictionaries--key-value-pairs)
5. [Tuples — Protected lists](#5-tuples--protected-lists)
6. [Mutable vs Immutable](#6-mutable-vs-immutable)
7. [If/Else — Making decisions](#7-ifelse--making-decisions)
8. [For Loop — Repeating items](#8-for-loop--repeating-items)
9. [While Loop — Repeating until false](#9-while-loop--repeating-until-false)
10. [Functions — Reusable code blocks](#10-functions--reusable-code-blocks)
11. [Common Errors & Fixes](#11-common-errors--fixes)
12. [Interview Questions](#12-interview-questions)

---

## 1. Variables & Data Types

### What's a Variable?

Think of a variable as a **box with a label**.

```
┌─────────────────┐
│      BOX        │
│   ┌─────────┐   │
│   │ "Krishna"│   │
│   └─────────┘   │
│        ↑        │
│    name (label) │
└─────────────────┘
```

You put something inside and give it a name.

---

### How to Create

```python
name = "Krishna"        # Text → String (str)
age = 25                # Whole number → Integer (int)
height = 5.9            # Decimal → Float (float)
is_employed = True      # Yes/No → Boolean (bool)
```

---

### 4 Main Data Types

| Type | Name | Example | What it is |
|------|------|---------|------------|
| `str` | String | `"Krishna"` | Text |
| `int` | Integer | `25` | Whole number |
| `float` | Float | `99.99` | Decimal |
| `bool` | Boolean | `True`, `False` | Yes or No |

---

### How to Check Type

```python
name = "Krishna"
print(type(name))  # <class 'str'>

age = 25
print(type(age))   # <class 'int'>
```

---

## 2. f-strings — Putting variables in text

### What is f-string?

`f` means **fast** or **format**. It lets you put variables inside text.

```python
name = "Krishna"
city = "Kadapa"

print(f"My name is {name} and I live in {city}")
# Output: My name is Krishna and I live in Kadapa
```

### Why use f-string?

Before f-strings, people did this:
```python
# Old way (complicated)
print("My name is " + name + " and I live in " + city)

# New way (easy)
print(f"My name is {name} and I live in {city}")
```

---

## 3. Lists — Ordered collections

### What's a List?

A list is like a **numbered shopping list**.

```
Shopping List:
1. Milk
2. Eggs
3. Bread
```

In Python:
```python
fruits = ["apple", "banana", "cherry"]
```

### Important Points

- **Ordered** = Has position (0, 1, 2...) — NOT sorted alphabetically!
- **Mutable** = Can change (add, remove items)

### Accessing Items

```python
fruits = ["apple", "banana", "cherry"]

print(fruits[0])   # "apple"  (first item)
print(fruits[1])   # "banana" (second item)
print(fruits[-1])  # "cherry" (last item)
```

### Common List Operations

```python
fruits = ["apple", "banana"]

fruits.append("cherry")     # Add to end: ["apple", "banana", "cherry"]
fruits.insert(0, "date")   # Add at position 0: ["date", "apple", "banana", "cherry"]
fruits.remove("banana")   # Remove by value
del fruits[0]             # Remove by position
print(len(fruits))        # Get length: 3
```

### Loop Through List

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)

# Output:
# apple
# banana
# cherry
```

---

## 4. Dictionaries — Key-Value pairs

### What's a Dictionary?

A dictionary is like a **contact book**.

```
Contact Book:
Krishna → 9876543210
John → 1234567890
```

In Python:
```python
person = {
    "name": "Krishna",
    "city": "Kadapa",
    "phone": "9876543210"
}
```

### Accessing Values

```python
person = {"name": "Krishna", "city": "Kadapa"}

print(person["name"])     # "Krishna"
print(person["city"])      # "Kadapa"
```

### Adding/Changing Values

```python
person = {"name": "Krishna"}
person["city"] = "Kadapa"     # Add new key
person["name"] = "K.V."       # Change existing key
```

### Dictionary with List Inside

```python
person = {
    "name": "Krishna",
    "skills": ["Python", "GCP", "AI"]
}

print(person["skills"])       # ["Python", "GCP", "AI"]
print(person["skills"][0])    # "Python"
```

### Loop Through Dictionary

```python
person = {"name": "Krishna", "city": "Kadapa"}

for key in person:
    print(f"{key}: {person[key]}")

# Output:
# name: Krishna
# city: Kadapa
```

---

## 5. Tuples — Protected lists

### What's a Tuple?

A tuple is like a list but **locked**. You **cannot change** it after creating.

```python
# Tuple - cannot change
coordinates = (10, 20, 30)

# List - can change
fruits = ["apple", "banana"]
```

### Why Use Tuples?

- **Protection** — Data won't accidentally change
- **Faster** — Tuples are faster than lists
- **Hashable** — Can use as dictionary keys

```python
# This works
fruits = ["apple", "banana"]
fruits.append("cherry")   # ✅ OK

# This FAILS
coordinates = (10, 20, 30)
coordinates.append(40)    # ❌ ERROR! Cannot change tuple
```

---

## 6. Mutable vs Immutable

### Simple Definition

| Term | Meaning | Can change after creation? |
|------|---------|---------------------------|
| **Mutable** | Can change | ✅ Yes |
| **Immutable** | Cannot change | ❌ No |

### Real-World Analogy

- **Mutable** = A **whiteboard** — erase and write new things
- **Immutable** = A **printed paper** — need a new paper to change

### Python Types

| Type | Mutable? |
|------|----------|
| List | ✅ Yes |
| Dictionary | ✅ Yes |
| Tuple | ❌ No |
| String | ❌ No |
| Number (int, float) | ❌ No |

### Important Warning!

```python
a = [1, 2, 3]
b = a              # b points to SAME list as a!
b.append(4)        # Change b

print(a)           # [1, 2, 3, 4] — a also changed!
print(b)           # [1, 2, 3, 4]
```

**Why?** Because `b = a` doesn't copy — it makes both variables point to the **same list**.

---

## 7. If/Else — Making decisions

### Basic If/Else

```python
age = 18

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

### Multiple Conditions

```python
score = 85

if score >= 90:
    print("A Grade")
elif score >= 80:
    print("B Grade")
elif score >= 70:
    print("C Grade")
else:
    print("Need improvement")
```

### Comparison Operators

| Symbol | Meaning |
|--------|---------|
| `==` | Equal to |
| `!=` | Not equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater or equal |
| `<=` | Less or equal |

---

## 8. For Loop — Repeating items

### What is a For Loop?

A for loop repeats code for **each item** in a collection.

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)

# Output:
# apple
# banana
# cherry
```

### Using range()

`range(start, stop, step)` generates numbers.

```python
# 1 to 5
for i in range(1, 6):
    print(i)

# 0 to 4 (default starts at 0)
for i in range(5):
    print(i)

# Even numbers: 0, 2, 4, 6, 8
for i in range(0, 10, 2):
    print(i)
```

---

## 9. While Loop — Repeating until false

### What is a While Loop?

A while loop repeats **until a condition becomes false**.

```python
count = 5

while count > 0:
    print(count)
    count = count - 1

print("Done!")
# Output: 5, 4, 3, 2, 1, Done!
```

### Warning!

Make sure the condition eventually becomes `False`, or it will run **forever**!

```python
# BAD - infinite loop!
# while True:
#     print("Forever!")
```

---

## 10. Functions — Reusable code blocks

### What is a Function?

A function is like a **machine**:
- You put something in (input)
- It does something
- It gives something back (output)

### Creating a Function

```python
def greet(name):
    return f"Hello, {name}!"

message = greet("Krishna")
print(message)  # Hello, Krishna!
```

### Function with Default Value

```python
def greet(name="Friend"):
    return f"Hello, {name}!"

print(greet())          # Hello, Friend!
print(greet("Krishna")) # Hello, Krishna!
```

### Function with Multiple Inputs

```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # 8
```

### *args and **kwargs

```python
# *args - multiple arguments
def sum_all(*numbers):
    total = 0
    for n in numbers:
        total = total + n
    return total

print(sum_all(1, 2, 3, 4))  # 10

# **kwargs - multiple keyword arguments
def print_info(**details):
    for key, value in details.items():
        print(f"{key}: {value}")

print_info(name="Krishna", city="Kadapa")
# name: Krishna
# city: Kadapa
```

### Today's Task — chunk_text Function

```python
def chunk_text(text, size=512):
    chunks = []
    for i in range(0, len(text), size):
        chunks.append(text[i:i+size])
    return chunks

# Test
sample = "A" * 1500
result = chunk_text(sample, size=512)
print(f"Chunks: {len(result)}")  # 3
```

---

## 11. Common Errors & Fixes

### ❌ IndentationError

**Problem:** Wrong spacing at the beginning of lines.

```python
# WRONG
    fruits = ["apple"]    # Extra space!

# CORRECT
fruits = ["apple"]        # No leading space
```

**Fix:** Remove spaces before the line. Use 4 spaces for indentation inside loops/functions.

---

### ❌ NameError

**Problem:** Using a variable before creating it.

```python
# WRONG
print(name)
name = "Krishna"

# CORRECT
name = "Krishna"
print(name)
```

---

### ❌ IndexError

**Problem:** Trying to access position that doesn't exist.

```python
fruits = ["apple", "banana"]

print(fruits[5])  # ❌ Only 0 and 1 exist!
```

---

### ❌ TypeError

**Problem:** Mixing incompatible types.

```python
# WRONG
age = 25
print("Age: " + age)  # Cannot add string + integer

# CORRECT
age = 25
print("Age: " + str(age))
# OR
print(f"Age: {age}")
```

---

## 12. Interview Questions

### Q1: What's the difference between a list and a dictionary?

**Simple Answer:**
- **List** = Ordered by position (0, 1, 2). Access by index.
- **Dictionary** = Key-value pairs. Access by key.

**Analogy:**
- List = Numbered shopping list (1. milk, 2. eggs)
- Dictionary = Contact book (Krishna → 9876543210)

---

### Q2: What is the difference between mutable and immutable?

**Simple Answer:**
- Mutable = Can change after creation (List, Dict)
- Immutable = Cannot change after creation (Tuple, String, Number)

---

### Q3: What is a function and why use it?

**Simple Answer:**
A function is reusable code. Instead of writing the same code again, wrap it in a function and call it when needed.

---

### Q4: What is an f-string?

**Simple Answer:**
A way to put variables inside text using `f"text {variable}"`.

---

## 📝 Progress Tracker

| Day | Topic | Status |
|-----|-------|--------|
| 1 | Python + Gemini API | ✅ |
| 2 | Variables, Data Types | ✅ |
| 3 | Lists, Dicts, Loops | ✅ |
| 4 | Functions | ⏳ |

---

## 13. Future Projects — Scrapling (Day 29+)

### What is Scrapling?

A Python web scraping framework that's "Built by Web Scrapers for Web Scrapers".

**Key Features:**
- Spider Framework (like Scrapy but modern)
- Bypasses Cloudflare, anti-bot detection
- Adaptive parsing (learns from website changes)
- Proxy rotation
- Session management

### When to Use

| Use Case | Tool to Use |
|----------|-------------|
| Job trends, salary research | ✅ Brave Search (already setup) |
| Extract data from specific sites | ✅ Scrapling |
| Twitter/X data | ✅ Twitter API v2 (already setup) |
| LinkedIn profiles | Apify (easier) |

### Project Ideas (for GitHub Portfolio)

1. **Job Board Scraper** — Scrape LinkedIn/Indeed for GCP AI jobs
2. **Trend Analyzer** — Track AI news from multiple sources
3. **Content Aggregator** — Collect articles on specific topics

---

## 🔧 Tools Setup Summary

### Already Configured (100% FREE)

| Tool | Purpose | Status | Cost |
|------|---------|--------|------|
| **Brave Search** | Web research, job trends | ✅ Ready | Free tier |
| **Tweet Analyzer** | Analyze tweets via Brave | ✅ Ready | Free tier |
| **Gemini API** | AI/ML responses | ✅ Ready | Free tier |

### How to Use in OpenClaw

**Search the web (in chat):**
```
You: Search for "GCP AI Engineer salary India 2025"
→ I run: python3 scripts/brave_search.py "GCP AI Engineer salary India 2025"
```

**Analyze a tweet (in chat):**
```
You: [paste any tweet link]
→ I run: tweet_fetcher_free.py with the URL
```

---

## 🔧 OpenClaw Skills Created

| Skill | File | Purpose |
|-------|------|---------|
| `web_search` | scripts/brave_search.py | Web search |
| `tweet_analysis` | scripts/tweet_fetcher_free.py | Tweet analysis |

---

## 📱 Plugins - What's Worth Getting?

### Currently Not Needed
- **Twitter/X plugins** - We have free Brave Search alternative ✅
- **Paid APIs** - Free tier covers 90% of needs ✅

### Optional Future Add-ons (Only If Needed)
| Plugin | Use Case | When |
|--------|----------|------|
| **gog (Google Workspace)** | Sync to Google Drive | Need cloud backup |
| **GitHub integration** | Auto-commit to repos | If you want automation |
| **Telegram premium** | Advanced bot features | If bot grows |

---

## 🔴🔵 Raycast + Claude Code + OpenClaw — Ultimate Integration Plan

### The Power Trio

| Tool | What It Does | Best For |
|------|-------------|----------|
| **Raycast** | Quick actions, app launcher, snippets | Speed, productivity |
| **Claude Code** | AI coding assistant (this!) | Code, analysis, learning |
| **OpenClaw** | AI mentor, Telegram bot, daily tasks | Job prep, motivation |

---

### 🎯 How Each Tool Fits Your 56-Day Prep

#### 1. Raycast (Your Desktop Command Center)

**What it does:**
- App launcher (Cmd+Space)
- Quick calculations, clipboard history
- Window management
- Custom commands/scripts
- Snippets

**Best For:**
- Launching apps quickly
- Copy/paste snippets
- Window management
- Running scripts

**Key Extensions to Install:**
| Extension | Use |
|-----------|-----|
| App Search | Launch any app fast |
| Clipboard History | Access past copies |
| Window Management | Move/resize windows |
| Snippets | Code templates |
| GitHub | Quick repo access |
| Google | Search quickly |

---

#### 2. Claude Code (This AI - Your Coding Partner)

**What it does:**
- Code writing, debugging, explaining
- File exploration
- Git operations
- Terminal commands
- Web research

**Best For:**
- Writing code
- Debugging errors
- Explaining concepts
- Running commands

**How to Use:**
```bash
# Quick question
claude "explain what a list is in Python"

# Code review
claude --review path/to/file.py

# Run a task
claude "create a Python script that does X"
```

---

#### 3. OpenClaw (Your 24/7 AI Mentor)

**What it does:**
- Daily mission management
- Telegram bot
- Job prep guidance
- Hero story practice
- Motivation

**Best For:**
- Structured learning
- Interview prep
- Daily accountability
- Telegram access

**How to Use:**
```
Telegram: /start
Or: openclaw run morning-drill
```

---

### 🔗 Integration Workflow

#### Morning (7:00 AM)
```
1. Raycast → Check calendar/notes
2. OpenClaw → Get daily mission (Telegram)
3. Claude Code → Start coding
```

#### During the Day
```
1. Need quick info → Raycast (search, calc)
2. Coding help → Claude Code
3. Job research → OpenClaw (Brave Search)
4. Questions → OpenClaw (Telegram)
```

#### Evening
```
1. Commit code → Claude Code or Raycast/GitHub
2. Review progress → OpenClaw
3. Tomorrow's prep → Raycast (snippets ready)
```

---

### 📋 Daily Usage Map

| Time | Task | Tool |
|------|------|------|
| 7:00 AM | Get mission | OpenClaw (Telegram) |
| 7:30 AM | SQL practice | Claude Code |
| 8:00 AM | Python coding | Claude Code |
| 10:00 AM | Quick search | Raycast |
| 11:00 AM | Git commit | Raycast/GitHub |
| 12:00 PM | Research jobs | OpenClaw (Brave) |
| 2:00 PM | Debug issues | Claude Code |
| 5:00 PM | Review day | OpenClaw |
| Evening | Practice stories | OpenClaw |

---

### 🚀 Quick Commands

#### Raycast
```
Cmd+Space → Open Raycast
type app name → Launch app
type ">" → Run command
```

#### Claude Code (Terminal)
```bash
claude "help me understand X"
claude --print "explain this code"
```

#### OpenClaw (Telegram)
```
/start - Start
/status - Progress check
/revise - Revision mode
```

---

### 💡 Pro Tips

1. **Raycast Snippets** → Store common code templates
2. **Claude Code** → Use for explaining concepts (like we did today!)
3. **OpenClaw** → Your accountability partner
4. **All Three** → Cover speed (Raycast) + AI (Claude) + Structure (OpenClaw)

---

### ✅ What to Do Right Now

1. **Raycast:** Open Cmd+Space, explore extensions
2. **Claude Code:** You're using it now!
3. **OpenClaw:** Message on Telegram when you need help

---

*Last Updated: February 25, 2026*
*Keep building, Krishna! 🕉️*
