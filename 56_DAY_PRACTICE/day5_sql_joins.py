# Day 5: SQL JOINs + Classes Intro

# ===============================
# SQL JOINs - Practice
# ===============================

# Creating sample tables for JOIN practice
# Run these in BigQuery or any SQL database

"""
-- Sample Data for JOINs

-- Table: employees
CREATE TABLE employees (
    id INT,
    name STRING,
    dept_id INT,
    salary INT
);

INSERT INTO employees VALUES
(1, 'Krishna', 10, 75000),
(2, 'Raj', 20, 80000),
(3, 'Priya', 10, 85000),
(4, 'Amit', NULL, 70000);

-- Table: departments
CREATE TABLE departments (
    id INT,
    dept_name STRING,
    location STRING
);

INSERT INTO departments VALUES
(10, 'Engineering', 'Hyderabad'),
(20, 'Data Science', 'Bangalore'),
(30, 'Marketing', 'Mumbai');

-- ============================================
-- INNER JOIN: Only matching records
-- ============================================
SELECT e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;

-- Result: Krishna -> Engineering, Raj -> Data Science, Priya -> Engineering

-- ============================================
-- LEFT JOIN: All employees + dept info
-- ============================================
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id;

-- Result: All 4 employees (Amit shows NULL dept - no matching dept)

-- ============================================
-- RIGHT JOIN: All departments + employee info
-- ============================================
SELECT e.name, d.dept_name
FROM employees e
RIGHT JOIN departments d ON e.dept_id = d.id;

-- Result: All 3 departments (Marketing shows NULL - no employee)

-- ============================================
-- FULL OUTER JOIN: Everything
-- ============================================
SELECT e.name, d.dept_name
FROM employees e
FULL OUTER JOIN departments d ON e.dept_id = d.id;

-- Result: All rows from both tables

-- ============================================
-- Multiple JOINs: 3 tables
-- ============================================
-- Table: orders (id, customer_id, product_id, amount)
-- Table: customers (id, name)
-- Table: products (id, product_name)

SELECT c.name, p.product_name, o.amount
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN products p ON o.product_id = p.id;
"""

# ===============================
# Python Classes - Preview
# ===============================

# Class: Employee
class Employee:
    def __init__(self, name, dept, salary):
        self.name = name
        self.dept = dept
        self.salary = salary

    def get_details(self):
        return f"{self.name} works in {self.dept} with salary {self.salary}"

    def bonus(self, percentage):
        return self.salary * (percentage / 100)

# Create object
emp = Employee("Krishna", "Engineering", 75000)
print(emp.get_details())
print(f"Bonus: {emp.bonus(10)}")

# Class inheritance
class Manager(Employee):
    def __init__(self, name, dept, salary, team_size):
        super().__init__(name, dept, salary)
        self.team_size = team_size

    def get_details(self):
        return f"{self.name} manages {self.team_size} people"

mgr = Manager("Raj", "Data Science", 80000, 5)
print(mgr.get_details())

print("\n✅ Day 5 Complete: JOINs + Classes intro done!")
