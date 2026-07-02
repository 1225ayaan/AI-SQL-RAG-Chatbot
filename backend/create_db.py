import sqlite3

conn = sqlite3.connect("data/employees.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    department TEXT,
    salary INTEGER,
    city TEXT
)
""")

employees = [
    (1, "Ayaan", 23, "Cloud", 50000, "Pune"),
    (2, "Rahul", 28, "HR", 45000, "Mumbai"),
    (3, "Sneha", 25, "IT", 60000, "Pune"),
    (4, "Rohan", 30, "Finance", 70000, "Delhi"),
    (5, "Priya", 27, "Marketing", 55000, "Bangalore"),
    (6, "Amit", 29, "IT", 65000, "Pune"),
    (7, "Neha", 26, "HR", 48000, "Mumbai"),
    (8, "Arjun", 31, "Cloud", 80000, "Hyderabad"),
    (9, "Pooja", 24, "Finance", 52000, "Pune"),
    (10, "Vikas", 32, "IT", 90000, "Chennai")
]

cursor.execute("DELETE FROM employees")

cursor.executemany(
    "INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?)",
    employees
)

conn.commit()
conn.close()

print("Database Created Successfully!")