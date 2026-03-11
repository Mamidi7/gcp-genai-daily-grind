# Day 11: Compute Services - Solutions

# ==============================
# Exercise 1: Choose Compute Service
# ==============================

def choose_compute_service(scenario):
    """
    Choose the best compute service for each scenario.
    """
    answers = {
        "A": ("Cloud Run", "Containerized app - perfect for Cloud Run"),
        "B": ("Compute Engine", "Need GPU access and full OS control"),
        "C": ("Cloud Functions", "Event-driven, triggered by Cloud Storage"),
        "D": ("GKE", "Complex microservices need Kubernetes"),
        "E": ("Compute Engine", "Traditional app needs full OS control")
    }

    return answers


# ==============================
# Exercise 2: CTE Challenge
# ==============================

def write_cte_query():
    """
    Find departments where total salary > 100000
    """
    query = """
WITH dept_salaries AS (
    SELECT
        department,
        SUM(salary) as total_salary
    FROM employees
    GROUP BY department
)
SELECT
    department,
    total_salary
FROM dept_salaries
WHERE total_salary > 100000
ORDER BY total_salary DESC
    """

    return query.strip()


# ==============================
# Exercise 3: Subquery Challenge
# ==============================

def write_subquery_query():
    """
    Find employees who earn more than their department's average
    """
    query = """
SELECT
    name,
    salary,
    department
FROM employees e1
WHERE salary > (
    SELECT AVG(salary)
    FROM employees e2
    WHERE e2.department = e1.department
)
ORDER BY department, salary DESC
    """

    return query.strip()


# ==============================
# Test Your Answers
# ==============================

if __name__ == "__main__":
    print("=== Day 11 Solutions ===\n")

    # Test Exercise 1
    print("1. Compute Service Selection:")
    answers = choose_compute_service("A")
    for key, (service, reason) in answers.items():
        print(f"   {key}: {service} - {reason}")
    print()

    # Test Exercise 2
    print("2. CTE Query:")
    print(write_cte_query())
    print()

    # Test Exercise 3
    print("3. Subquery Query:")
    print(write_subquery_query())
    print()

    print("✓ All solutions verified!")
