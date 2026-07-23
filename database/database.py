import os
import sqlite3

BASE_DIR = os.path.dirname(__file__)

DB_PATH = os.path.join(BASE_DIR, "library.db")

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    return connection


def create_tables():
    connection = get_connection()
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
    print("Books Table Created")

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
    print("Member Table Created")
    print(DB_PATH)

    connection.commit()
    connection.close()
