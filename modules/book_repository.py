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


def get_book_by_id(book_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT *
            FROM books
            WHERE book_id = ?
            AND is_active = 1
            """,
            (book_id,)
        )

        book = cursor.fetchone()
        return book

    finally:
        connection.close()


def update_book(book_id, title, author, category, quantity):

    book = get_book_by_id(book_id)
    if book is None:
        return False

    new_quantity = quantity
    #Tuple index of Book Table.
    old_quantity = book[4]
    old_available_quantity = book[5]

    issued_books = old_quantity - old_available_quantity

    if new_quantity < issued_books:
        return False

    difference = new_quantity - old_quantity

    new_available_quantity = old_available_quantity + difference

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE books
            SET
                title = ?,
                author = ?,
                category = ?,
                quantity = ?,
                available_quantity = ?
            WHERE book_id = ?
            """,

            (
                title,
                author,
                category,
                new_quantity,
                new_available_quantity,
                book_id
            )
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()