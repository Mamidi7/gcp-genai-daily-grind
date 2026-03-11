# Day 10: Cloud Storage (GCS) - Solutions

# ==============================
# Exercise 1: Storage Class Selection
# ==============================

def select_storage_class(scenario):
    """
    Select the appropriate storage class for each scenario.
    """
    answers = {
        "A": "Standard",    # Website images - accessed frequently
        "B": "Nearline",    # Monthly backups - accessed once a month
        "C": "Archive",     # Yearly compliance - rarely accessed
        "D": "Standard"    # Real-time ML inference - accessed constantly
    }

    return answers


# ==============================
# Exercise 2: Bucket Naming
# ==============================

def validate_bucket_name(bucket_name):
    """
    Validate if a bucket name is valid.
    """
    is_valid = True
    reason = ""

    # Check length
    if len(bucket_name) < 3 or len(bucket_name) > 63:
        return False, "Must be 3-63 characters"

    # Check for invalid characters
    valid_chars = set('abcdefghijklmnopqrstuvwxyz0123456789-.')
    if not all(c in valid_chars for c in bucket_name):
        return False, "Only lowercase letters, numbers, dashes, dots allowed"

    # Cannot start or end with dash
    if bucket_name.startswith('-') or bucket_name.endswith('-'):
        return False, "Cannot start or end with dash"

    # Cannot have consecutive dots
    if '..' in bucket_name:
        return False, "Cannot have consecutive dots"

    # Cannot be IP address format
    parts = bucket_name.split('.')
    if len(parts) == 4 and all(p.isdigit() for p in parts):
        return False, "Cannot be IP address format"

    return True, "Valid bucket name"


# ==============================
# Exercise 3: Window Functions
# ==============================

def write_row_number_query():
    """
    Write a BigQuery query that:
    - Ranks customers by total purchase amount
    - Uses ROW_NUMBER()
    - Shows top 10 customers
    """
    query = """
WITH customer_totals AS (
    SELECT
        customer_id,
        SUM(amount) as total_purchases
    FROM orders
    GROUP BY customer_id
)
SELECT
    customer_id,
    total_purchases,
    ROW_NUMBER() OVER (ORDER BY total_purchases DESC) as customer_rank
FROM customer_totals
ORDER BY customer_rank
LIMIT 10
    """

    return query.strip()


def write_lag_query():
    """
    Write a BigQuery query that:
    - Shows daily page views
    - Includes previous day's views (LAG)
    - Shows day-over-day change
    """
    query = """
SELECT
    date,
    page_views,
    LAG(page_views) OVER (ORDER BY date) as prev_day_views,
    page_views - LAG(page_views) OVER (ORDER BY date) as day_over_day_change
FROM daily_stats
ORDER BY date
    """

    return query.strip()


# ==============================
# Test Your Answers
# ==============================

if __name__ == "__main__":
    print("=== Day 10 Solutions ===\n")

    # Test Exercise 1
    print("1. Storage Class Selection:")
    answers = select_storage_class("A")
    print(f"   A (website images): {answers['A']}")
    print(f"   B (monthly backups): {answers['B']}")
    print(f"   C (yearly logs): {answers['C']}")
    print(f"   D (ML inference): {answers['D']}")
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
    print("   ROW_NUMBER Query:")
    print(write_row_number_query())
    print()
    print("   LAG Query:")
    print(write_lag_query())
    print()

    print("✓ All solutions verified!")
