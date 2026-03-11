# Day 9: GCP Console + IAM Basics - Exercises

# ==============================
# Exercise 1: IAM Role Matching
# ==============================

def match_role_to_permission():
    """
    Match the correct role to each scenario.

    Scenario A: Read-only access to view billing
    Scenario B: Can deploy Cloud Functions but not modify IAM
    Scenario C: Full control including adding team members

    Returns: Dictionary with answers
    """
    answers = {
        "A": None,  # Your answer: Viewer, Editor, or Owner?
        "B": None,
        "C": None
    }

    # YOUR CODE HERE: Fill in the answers
    # Example: answers["A"] = "Viewer"

    return answers


# ==============================
# Exercise 2: Project Hierarchy
# ==============================

def build_project_hierarchy(org_name, folders, projects):
    """
    Build a simple project hierarchy.

    Args:
        org_name: Organization domain (e.g., "acme.com")
        folders: List of folder names
        projects: List of project names

    Returns: Dictionary showing hierarchy
    """
    hierarchy = {
        "organization": org_name,
        "folders": [],
        "projects": []
    }

    # YOUR CODE HERE: Build the hierarchy
    # Each folder should contain projects

    return hierarchy


# ==============================
# Exercise 3: Custom Role Design
# ==============================

def design_custom_role(role_name, permissions_list):
    """
    Design a custom role with specific permissions.

    Args:
        role_name: Name of your custom role
        permissions_list: List of permission strings

    Returns: Custom role definition
    """
    custom_role = {
        "role_name": role_name,
        "title": None,
        "description": None,
        "stage": "GA",  # ALPHA, BETA, or GA
        "included_permissions": []
    }

    # YOUR CODE HERE:
    # 1. Create a title (e.g., "Custom BigQuery Viewer")
    # 2. Write a description
    # 3. Add permissions

    return custom_role


# ==============================
# Exercise 4: ARRAY_AGG Challenge
# ==============================

def write_array_agg_query():
    """
    Write a BigQuery query that:
    - Groups employees by department
    - Creates an array of employee names per department

    Return the SQL query as a string.
    """
    query = ""

    # YOUR CODE HERE
    # Hint: Use ARRAY_AGG with GROUP BY
    # Table: employees (name STRING, department STRING, salary INT64)

    return query


# ==============================
# Exercise 5: STRUCT Challenge
# ==============================

def write_struct_query():
    """
    Write a BigQuery query that:
    - Creates a STRUCT with: name, department, salary
    - From the employees table

    Return the SQL query as a string.
    """
    query = ""

    # YOUR CODE HERE
    # Hint: Use STRUCT() to create nested data
    # Table: employees (name STRING, department STRING, salary INT64)

    return query


# ==============================
# Test Your Answers
# ==============================

if __name__ == "__main__":
    print("=== Day 9 Exercises ===\n")

    # Test Exercise 1
    print("1. IAM Role Matching:")
    answers = match_role_to_permission()
    print(f"   Answers: {answers}\n")

    # Test Exercise 2
    print("2. Project Hierarchy:")
    hierarchy = build_project_hierarchy("acme.com", ["engineering", "sales"], ["proj1", "proj2"])
    print(f"   {hierarchy}\n")

    # Test Exercise 3
    print("3. Custom Role Design:")
    role = design_custom_role("data_analyst", ["bigquery.jobs.create", "bigquery.tables.get"])
    print(f"   {roleData}\n")

    # Test Exercise 4
    print("4. ARRAY_AGG Query:")
    query = write_array_agg_query()
    print(f"   {query}\n")

    # Test Exercise 5
    print("5. STRUCT Query:")
    query = write_struct_query()
    print(f"   {query}\n")
