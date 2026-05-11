import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_PATH = "sample_data/business.db"


def create_database():
    # Create sample_data folder if it doesn't exist
    os.makedirs("sample_data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            email       TEXT,
            city        TEXT,
            joined_date TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category    TEXT,
            price       REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            product_id  INTEGER,
            quantity    INTEGER,
            order_date  TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id)  REFERENCES products(id)
        )
    """)

    customers = [
        ("Ali Hassan",     "ali@email.com",     "Karachi",   "2022-01-15"),
        ("Sara Khan",      "sara@email.com",    "Lahore",    "2022-03-20"),
        ("Ahmed Raza",     "ahmed@email.com",   "Islamabad", "2022-05-10"),
        ("Fatima Malik",   "fatima@email.com",  "Karachi",   "2022-07-22"),
        ("Usman Tariq",    "usman@email.com",   "Peshawar",  "2022-09-05"),
        ("Ayesha Noor",    "ayesha@email.com",  "Lahore",    "2023-01-18"),
        ("Bilal Ahmed",    "bilal@email.com",   "Karachi",   "2023-03-30"),
        ("Zara Hussain",   "zara@email.com",    "Islamabad", "2023-06-14"),
        ("Omar Sheikh",    "omar@email.com",    "Multan",    "2023-08-25"),
        ("Hina Baig",      "hina@email.com",    "Lahore",    "2023-11-11"),
    ]

    products = [
        ("Laptop",         "Electronics",  85000),
        ("Smartphone",     "Electronics",  45000),
        ("Headphones",     "Electronics",   8500),
        ("Office Chair",   "Furniture",    12000),
        ("Standing Desk",  "Furniture",    25000),
        ("Notebook",       "Stationery",     150),
        ("Pen Set",        "Stationery",     300),
        ("Backpack",       "Accessories",   3500),
        ("Water Bottle",   "Accessories",    800),
        ("Monitor",        "Electronics",  32000),
    ]

    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO customers (name, email, city, joined_date) VALUES (?,?,?,?)",
            customers
        )

    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO products (product_name, category, price) VALUES (?,?,?)",
            products
        )

    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] == 0:
        random.seed(42)
        start_date = datetime(2023, 1, 1)
        orders = []
        for _ in range(200):
            customer_id = random.randint(1, 10)
            product_id  = random.randint(1, 10)
            quantity    = random.randint(1, 5)
            order_date  = (start_date + timedelta(days=random.randint(0, 364))
                           ).strftime("%Y-%m-%d")
            orders.append((customer_id, product_id, quantity, order_date))

        cursor.executemany(
            "INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES (?,?,?,?)",
            orders
        )

    conn.commit()
    conn.close()
    print(f"Database created at {DB_PATH}")
    print("Tables: customers, products, orders")
    print("Sample data inserted successfully.")


def get_schema():
    """
    Returns the database schema as a string.
    This is sent to the LLM so it knows what tables and
    columns exist — without this the LLM would invent
    table names that do not exist.
    """
    schema = """
DATABASE SCHEMA (SQLite):

TABLE: customers
  - id          INTEGER  (primary key, auto increment)
  - name        TEXT     (customer full name)
  - email       TEXT     (customer email)
  - city        TEXT     (city name e.g. Karachi, Lahore, Islamabad)
  - joined_date TEXT     (format: YYYY-MM-DD)

TABLE: products
  - id           INTEGER  (primary key, auto increment)
  - product_name TEXT     (name of the product)
  - category     TEXT     (Electronics, Furniture, Stationery, Accessories)
  - price        REAL     (price in PKR)

TABLE: orders
  - id          INTEGER  (primary key, auto increment)
  - customer_id INTEGER  (foreign key → customers.id)
  - product_id  INTEGER  (foreign key → products.id)
  - quantity    INTEGER  (number of units ordered)
  - order_date  TEXT     (format: YYYY-MM-DD)

RELATIONSHIPS:
  orders.customer_id → customers.id
  orders.product_id  → products.id

IMPORTANT NOTES:
  - Revenue = products.price * orders.quantity
  - Use strftime('%Y-%m', order_date) for monthly grouping
  - Use strftime('%Y', order_date) for yearly grouping
  - All text comparisons are case-insensitive in SQLite
"""
    return schema


def execute_query(sql):
    """
    Executes a SQL query and returns:
    - columns: list of column names
    - rows: list of result rows
    - error: error message if query failed
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        return columns, rows, None

    except Exception as e:
        return None, None, str(e)


if __name__ == "__main__":
    create_database()