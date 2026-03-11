# Day 10: Cloud Storage (GCS) - Exercises

# ==============================
# Exercise 1: Storage Class Selection
# ==============================

def select_storage_class(scenario):
    """
    Select the appropriate storage class for each scenario.

    Args:
        scenario: Description of data access pattern

    Returns: Recommended storage class
    """
    # Scenarios to match:
    scenarios = {
        "A": "Frequently accessed website images",
        "B": "Monthly backup files",
        "C": "Yearly compliance audit logs",
        "D": "Real-time ML model inference"
    }

    # YOUR CODE HERE: Map each scenario to correct storage class
    # Options: Standard, Nearline, Coldline, Archive

    answers = {
        "A": None,
        "B": None,
        "C": None,
        "D": None
    }

    return answers


# ==============================
# Exercise 2: Bucket Naming
# ==============================

def validate_bucket_name(bucket_name):
    """
    Validate if a bucket name is valid.

    Returns: (is_valid, reason)
    """
    # YOUR CODE HERE:
    # Rules:
    # - 3-63 characters
    # - lowercase letters, numbers, dashes only
    # - cannot start or end with dash
    # - cannot have consecutive dots

    is_valid = True
    reason = ""

    return is_valid, reason


# ==============================
# Exercise 3: Window Functions
# ==============================

def write_row_number_query():
    """
    Write a BigQuery query that:
    - Ranks customers by total purchase amount
    - Uses ROW_NUMBER()
    - Shows top 10 customers

    Return the SQL query as a string.
    """
    query = ""

    # YOUR CODE HERE
    # Tables: orders (customer_id, amount)
    # Hint: First sum by customer, then apply ROW_NUMBER

    return query


def write_lag_query():
    """
    Write a BigQuery query that:
    - Shows daily page views
    - Includes previous day's views (LAG)
    - Shows day-over-day change

    Return the SQL query as a string.
    """
    query = ""

    # YOUR CODE HERE
    # Table: daily_stats (date, page_views)

    return query


# ==============================
# Test Your Answers
# ==============================

if __name__ == "__main__":
    print("=== Day 10 Exercises ===\n")

    # Test Exercise 1
    print("1. Storage Class Selection:")
    answers = select_storage_class("A")
    print(f"   Try it! Map: {answers}")
    print()

    # Test Exercise 2
    print("2. Bucket Naming:")
    test_names = ["my-bucket", "MyBucket", "bucket-name-", "bucket..name"]
    for name in test_names:
        valid, reason = validate_bucket_name(name)
        print(f"   {name}: {'✓ Valid' if valid else '✗ Invalid'} - {reason}")
    print()

    # Test Exercise 3
    print("3. Window Functions:")
    print("   Write your queries in the functions above!")
    print()
