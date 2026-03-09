# 🐍 Python Cheat Sheet — 10th Std Level

> Explain like I'm a 10th std kid from Andhra! 😎

---

## 1. Variables — Box lekapothe?

**What is it?**
Variable ante baga simple - einemo **box** create chesi, value ni store cheyyataniki.

```
┌─────────────┐
│ BOX         │
│ ┌─────────┐ │
│ │ "Krishna"│ │
│ └─────────┘ │
│    name     │  ← Label (variable name)
└─────────────┘
```

**Code:**
```python
name = "Krishna"    # Box lo text
age = 25            # Box lo number
is_smart = True     # Box lo True/False
```

**4 Types:**
| Type | Telugu lo | Example |
|------|-----------|---------|
| `str` | Text | `"Krishna"` |
| `int` | Full Number | `25` |
| `float` | Decimal | `5.9` |
| `bool` | Yes/No | `True` |

---

## 2. f-strings — Text lo Variable Paste Cheste

**What is it?**
f-string ante fast format. Text lo `{}` use chesi variable paste cheyyachhu.

```python
name = "Krishna"
print(f"My name is {name}")
# Output: My name is Krishna
```

**Old way (don't use):**
```python
print("My name is " + name)  # Hard
print(f"My name is {name}")   # Easy ✅
```

---

## 3. Lists — Numbered List

**What is it?**
List ante ordered collection. Like shopping list - 1st item, 2nd item...

```
1. Milk
2. Eggs
3. Bread
```

**Code:**
```python
fruits = ["apple", "banana", "cherry"]
print(fruits[0])   # "apple" (1st)
print(fruits[-1])  # "cherry" (last)
```

**Common Operations:**
```python
fruits.append("date")     # Add to last
fruits.insert(0, "date") # Add to first position
fruits.remove("banana")  # Remove by name
len(fruits)              # Count items
```

---

## 4. Dictionary — Contact Book

**What is it?**
Dict ante key-value pairs. Like contact book:

```
Krishna → 9876543210
Raj → 1234567890
```

**Code:**
```python
person = {"name": "Krishna", "city": "Kadapa"}

print(person["name"])   # "Krishna"
person["age"] = 25       # Add new
```

---

## 5. Tuple — Locked List

**What is it?**
Tuple ante list kani **change cheyyale**. Locked!

```python
coords = (10, 20, 30)
coords[0] = 50  # ❌ ERROR! Can't change
```

---

## 6. Mutable vs Immutable

| Term | Meaning | Examples |
|------|---------|----------|
| Mutable | Change cheyyalam | List, Dict |
| Immutable | Change cheyyale | Tuple, String, Number |

```python
# Mutable - Change cheyyalam ✅
fruits = ["apple"]
fruits.append("banana")  # OK

# Immutable - Change cheyyale ❌
name = "Krishna"
name = "Raj"  # Actually creates new string
```

---

## 7. If/Else — Decision Making

**What is it?**
If condition true ante ee code, else ante alternative.

```python
age = 18

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

**Multiple:**
```python
score = 85

if score >= 90:
    print("A Grade")
elif score >= 80:
    print("B Grade")
else:
    print("C Grade")
```

---

## 8. For Loop — Repeat Cheyyataniki

**What is it?**
For loop ante - elanti item leni ante, sochinchi korachhu.

```python
fruits = ["apple", "banana"]

for fruit in fruits:
    print(fruit)

# Output:
# apple
# banana
```

**range() - Numbers:**
```python
for i in range(5):        # 0,1,2,3,4
for i in range(1, 6):    # 1,2,3,4,5
for i in range(0, 10, 2): # 0,2,4,6,8 (even)
```

---

## 9. While Loop — Until False

**What is it?**
While loop ante - condition false avvudu varaku repeat cheyyataniki.

```python
count = 5

while count > 0:
    print(count)
    count = count - 1

# Output: 5,4,3,2,1
```

---

## 10. Functions — Machine

**What is it?**
Function ante oka machine - input enter cheyy, output output ga vastundi.

```python
def greet(name):
    return f"Hello {name}!"

print(greet("Krishna"))  # Hello Krishna!
```

**Default Value:**
```python
def greet(name="Friend"):
    return f"Hello {name}!"

print(greet())         # Hello Friend!
print(greet("Krishna")) # Hello Krishna!
```

***args - Multiple Inputs:**
```python
def sum_all(*numbers):
    return sum(numbers)

print(sum_all(1, 2, 3, 4))  # 10
```

**kwargs - Key-Value:**
```python
def info(**data):
    for k, v in data.items():
        print(f"{k}: {v}")

info(name="Krishna", city="Kadapa")
# Output:
# name: Krishna
# city: Kadapa
```

---

## 11. Sets — Unique Items

**What is it?**
Set ante unique items - duplicates automatic ga remove aitai.

```python
skills = {"python", "sql", "python"}  # "python" once only!
print(skills)  # {'python', 'sql'}
```

**Operations:**
```python
set1 = {"python", "sql"}
set2 = {"sql", "gcp"}

set1 & set2   # Intersection: {'sql'} (common)
set1 | set2   # Union: {'python', 'sql', 'gcp'} (all)
set1 - set2   # Difference: {'python'} (only in set1)
```

---

## 12. Comprehensions — One-Liner List

**What is it?**
Comprehension ante - for loop ni one line lo write cheyyataniki.

**Template:**
```python
[new_item for item in list if condition]
```

**Examples:**
```python
# Squares
squares = [x**2 for x in range(1, 6)]
# [1, 4, 9, 16, 25]

# Even numbers only
nums = [1,2,3,4,5,6,7,8,9,10]
evens = [x for x in nums if x % 2 == 0]
# [2, 4, 6, 8, 10]

# Dictionary
squares = {x: x**2 for x in range(3)}
# {0: 0, 1: 1, 2: 4}

# Flatten matrix
matrix = [[1,2], [3,4]]
flat = [n for row in matrix for n in row]
# [1, 2, 3, 4]
```

---

## Quick Interview Answers

| Question | Answer |
|----------|--------|
| List vs Dict? | List = ordered by index, Dict = key-value |
| List vs Tuple? | List = can change, Tuple = locked |
| Mutable vs Immutable? | Mutable = can change (list, dict), Immutable = cannot (tuple, str) |
| List comprehension? | One-liner to create/filter lists |
| *args? | Multiple arguments as tuple |
| **kwargs? | Multiple key-value as dict |
| Set use case? | Remove duplicates, find common items |

---

*Last Updated: Feb 26, 2026*
