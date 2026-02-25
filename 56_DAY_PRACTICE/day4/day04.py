# Day 4: Functions, Sets, Comprehensions

# Functions
def greet(name):
    return f"Hey {name}, let's crush it!"

def sum_all(*numbers):
    return sum(numbers)

def introduce(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

# Sets
skills_python = {"python", "sql", "bigquery", "vertex"}
skills_gcp = {"gcp", "bigquery", "vertex", "cloud run"}

both = skills_python & skills_gcp
only_python = skills_python - skills_gcp
all_skills = skills_python | skills_gcp

# Comprehensions
projects = [
    {"name": "Data Pipeline", "days": 5},
    {"name": "ML Model", "days": 12},
    {"name": "API Deploy", "days": 3},
    {"name": "Dashboard", "days": 7}
]

long_projects = [p["name"] for p in projects if p["days"] > 5]
short_projects = [p["name"] for p in projects if p["days"] <= 5]

print("Both:", both)
print("Only Python:", only_python)
print("All Skills:", all_skills)
print("Long Projects:", long_projects)
print("Short Projects:", short_projects)
