from database.database import get_connection
from datetime import datetime
import sqlite3

def add_book(book_id, title, author, category, quantity):

    available_quantity = quantity
    created_at = datetime.now().strftime("%Y-%m-%d")
    is_active = 1

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO books(
            book_id,
            title, 
            author, 
            category, 
            quantity, 
            available_quantity, 
            created_at, 
            is_active
            )
                    
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                            
            """,

            (
                book_id,
                title, 
                author, 
                category, 
                quantity, 
                available_quantity,    
                created_at, 
                is_active
            )
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def get_all_books():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT *
            FROM books
            WHERE is_active = 1
            ORDER BY title ASC
            
            """
        )

        books = cursor.fetchall()
        return books

    finally:
        connection.close()