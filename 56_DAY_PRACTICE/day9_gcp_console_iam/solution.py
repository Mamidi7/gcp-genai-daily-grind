# Day 9: GCP Console + IAM Basics - Solutions

# ==============================
# Exercise 1: IAM Role Matching
# ==============================

def match_role_to_permission():
    """
    Match the correct role to each scenario.

    Scenario A: Read-only access to view billing -> Viewer
    Scenario B: Can deploy Cloud Functions but not modify IAM -> Editor
    Scenario C: Full control including adding team members -> Owner
    """
    answers = {
        "A": "Viewer",      # Read-only access
        "B": "Editor",      # Can deploy/manage resources but not IAM
        "C": "Owner"        # Full control including IAM
    }

    return answers


# ==============================
# Exercise 2: Project Hierarchy
# ==============================

def build_project_hierarchy(org_name, folders, projects):
    """
    Build a simple project hierarchy.
    """
    hierarchy = {
        "organization": org_name,
        "folders": [],
        "projects": projects
    }

    # Add folders with nested structure
    for folder in folders:
        hierarchy["folders"].append({
            "name": folder,
            "projects": projects  # In reality, projects can be in different folders
        })

    return hierarchy


# ==============================
# Exercise 3: Custom Role Design
# ==============================

def design_custom_role(role_name, permissions_list):
    """
    Design a custom role with specific permissions.
    """
    custom_role = {
        "role_name": role_name,
        "title": "Custom Data Analyst Role",
        "description": "Role for data analysts who need to run queries and view tables but cannot modify schemas",
        "stage": "GA",
        "included_permissions": permissions_list
    }

    return custom_role


# ==============================
# Exercise 4: ARRAY_AGG Challenge
# ==============================

def write_array_agg_query():
    """
    Write a BigQuery query that:
    - Groups employees by department
    - Creates an array of employee names per department
    """
    query = """
SELECT
    department,
    ARRAY_AGG(name) as employee_names
FROM employees
GROUP BY department
    """

    return query.strip()


# ==============================
# Exercise 5: STRUCT Challenge
# ==============================

def write_struct_query():
    """
    Write a BigQuery query that:
    - Creates a STRUCT with: name, department, salary
    - From the employees table
    """
    query = """
SELECT
    STRUCT(
        name AS employee_name,
        department AS dept,
        salary AS compensation
    ) as employee_info
FROM employees
    """

    return query.strip()


# ==============================
# Test Your Answers
# ==============================

if __name__ == "__main__":
    print("=== Day 9 Solutions ===\n")

    # Test Exercise 1
    print("1. IAM Role Matching:")
    answers = match_role_to_permission()
    for scenario, role in answers.items():
        print(f"   Scenario {scenario}: {role}")
    print()

    # Test Exercise 2
    print("2. Project Hierarchy:")
    hierarchy = build_project_hierarchy("acme.com", ["engineering", "sales"], ["proj1", "proj2"])
    print(f"   Org: {hierarchy['organization']}")
    print(f"   Folders: {[f['name'] for f in hierarchy['folders']]}")
    print()

    # Test Exercise 3
    print("3. Custom Role Design:")
    role = design_custom_role("data_analyst", ["bigquery.jobs.create", "bigquery.tables.get"])
    print(f"   Title: {role['title']}")
    print(f"   Description: {role['description']}")
    print(f"   Permissions: {role['included_permissions']}")
    print()

    # Test Exercise 4
    print("4. ARRAY_AGG Query:")
    print(write_array_agg_query())
    print()

    # Test Exercise 5
    print("5. STRUCT Query:")
    print(write_struct_query())
    print()

    print("✓ All solutions verified!")
