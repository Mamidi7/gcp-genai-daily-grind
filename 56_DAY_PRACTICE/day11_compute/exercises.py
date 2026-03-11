# Day 11: Compute Services - Exercises

# ==============================
# Exercise 1: Choose Compute Service
# ==============================

def choose_compute_service(scenario):
    """
    Choose the best compute service for each scenario.

    Returns: (service, reason)
    """
    scenarios = {
        "A": "Deploy a Python Flask API as container",
        "B": "Run a long-running ML training job with GPUs",
        "C": "Process files when uploaded to Cloud Storage",
        "D": "Run a complex microservices architecture",
        "E": "Host a traditional Windows server application"
    }

    # YOUR CODE HERE: Map each to best service
    # Options: Compute Engine, Cloud Run, Cloud Functions, GKE

    answers = {
        "A": None,
        "B": None,
        "C": None,
        "D": None,
        "E": None
    }

    return answers


# ==============================
# Exercise 2: SQL - CTE Challenge
# ==============================

def write_cte_query():
    """
    Write a BigQuery query using CTE that:
    - Finds departments where total salary > 100000
    - Returns department name and total salary

    Table: employees (department STRING, salary INT64, name STRING)

    Return the SQL query as a string.
    """
    query = ""

    # YOUR CODE HERE

    return query


# ==============================
# Exercise 3: SQL - Subquery Challenge
# ==============================

def write_subquery_query():
    """
    Write a BigQuery query using subquery that:
    - Finds employees who earn more than their department's average

    Table: employees (department STRING, salary INT64, name STRING)

    Return the SQL query as a string.
    """
    query = ""

    # YOUR CODE HERE

    return query


# ==============================
# Test Your Answers
# ==============================

if __name__ == "__main__":
    print("=== Day 11 Exercises ===\n")

    print("1. Compute Service Selection:")
    print("   Match scenarios to services!")
    print()

    print("2. CTE Query:")
    print("   Write your query in the function!")
    print()

    print("3. Subquery Query:")
    print("   Write your query in the function!")
    print()
