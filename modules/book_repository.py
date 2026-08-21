from database.database import get_connection
from modules.member_repository import *
from modules.transaction_repository import *
from datetime import datetime, timedelta
import sqlite3

def add_book(book_id, title, author, category, quantity, db_name="library.db"):

    available_quantity = quantity
    created_at = datetime.now().strftime("%Y-%m-%d")
    is_active = 1

    connection = get_connection(db_name)
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


def get_all_books(db_name="library.db"):

    connection = get_connection(db_name)
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


def get_book_by_id(book_id, db_name="library.db"):

    connection = get_connection(db_name)
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


def update_book(book_id, title, author, category, quantity, db_name="library.db"):

    book = get_book_by_id(book_id, db_name)
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

    connection = get_connection(db_name)
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


def soft_delete_book(book_id, db_name="library.db"):

    book = get_book_by_id(book_id, db_name)
    if book is None:
        return False

    connection = get_connection(db_name)
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE books
            SET is_active = 0
            WHERE book_id = ?
            """,
            
            (book_id,)
        )

        connection.commit()
        return True

    finally:
        connection.close()


def update_available_quantity(connection, book_id, available_quantity):

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE books
        SET available_quantity = ?
        WHERE book_id = ?
        """,
    
        (
            available_quantity,
            book_id
        )
    )
    
    return True


def issue_book(book_id, member_id, db_name="library.db"):

    book = get_book_by_id(book_id, db_name)
    if book is None:
        return False

    member = get_member_by_id(member_id, db_name)
    if member is None:
        return False

    available_quantity = book[5]
    if available_quantity == 0:
        return False

    new_available_quantity = available_quantity - 1

    issue_date = datetime.now()
    due_date = issue_date + timedelta(days=7)

    issue_date = issue_date.strftime('%Y-%m-%d')
    due_date = due_date.strftime('%Y-%m-%d')

    connection = get_connection(db_name)

    try:

        update_available_quantity(connection, book_id, new_available_quantity)

        add_transaction(connection, book_id, member_id, issue_date, due_date)

        connection.commit()

    except Exception:

        connection.rollback()
        return False

    finally:

        connection.close()

    return True


def return_book(book_id, member_id, db_name="library.db"):

    transaction = get_active_transaction(book_id, member_id, db_name)
    if transaction is None:
        return False

    book = get_book_by_id(book_id, db_name)
    if book is None:
        return False

    available_quantity = book[5]

    return_date = datetime.now()
    due_date = datetime.strptime(transaction[4], '%Y-%m-%d')
    fine = calculate_fine(due_date, return_date)

    new_available_quantity = available_quantity + 1

    return_date = return_date.strftime('%Y-%m-%d')

    connection = get_connection(db_name)

    try:

        update_available_quantity(connection, book_id, new_available_quantity)
        update_return_transaction(connection, transaction[0], return_date, fine)
        connection.commit()

    except Exception:

        connection.rollback()
        return False

    finally:

        connection.close()

    return True



def calculate_fine(due_date, return_date):

    late_days = (return_date - due_date).days

    if late_days <= 0:
        return 0

    return late_days * 10