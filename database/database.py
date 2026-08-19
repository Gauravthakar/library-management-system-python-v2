import os
import sqlite3

BASE_DIR = os.path.dirname(__file__)

DB_PATH = os.path.join(BASE_DIR, "library.db")

def get_connection(db_name="library.db"):
    connection = sqlite3.connect("database/" + db_name)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables(db_name="library.db"):
    connection = get_connection(db_name)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books(
            book_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity >= 0),
            available_quantity INTEGER NOT NULL CHECK(available_quantity >= 0),
            created_at TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            CHECK(available_quantity <= quantity)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members(
            member_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL CHECK(length(phone) == 10),
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            join_date TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id TEXT NOT NULL,
            member_id TEXT NOT NULL,
            issue_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            fine REAL DEFAULT 0 CHECK(fine >= 0),
            status TEXT NOT NULL,
            FOREIGN KEY(book_id)
            REFERENCES books(book_id),
            FOREIGN KEY(member_id)
            REFERENCES members(member_id),
            CHECK(status IN ('Issued', 'Returned'))
        )
    """)

    connection.commit()
    connection.close()
