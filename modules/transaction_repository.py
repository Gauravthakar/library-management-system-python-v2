from database.database import get_connection
import sqlite3


def add_transaction(connection, book_id, member_id, issue_date, due_date):

    return_date = None
    fine = 0
    status = "Issued"

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO transactions(
            book_id,
            member_id,
            issue_date,
            due_date,
            return_date,
            fine,
            status
            )

            VALUES(?, ?, ?, ?, ?, ?, ?)
            """,

            (
                book_id,
                member_id,
                issue_date,
                due_date,
                return_date,
                fine,
                status
            )
        )

        return True

    except sqlite3.IntegrityError:
        return False


def get_active_transaction(book_id, member_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT *
            FROM transactions
            WHERE book_id = ?
            AND member_id = ?
            AND status = "Issued"
            """,
        
            (
                book_id,
                member_id
            )
        )
        
        transaction = cursor.fetchone()
        return transaction

    finally:
        connection.close()


def update_return_transaction(connection, transaction_id, return_date, fine):

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE transactions
        SET 
            return_date = ?,
            fine = ?,
            status = 'Returned'
        WHERE transaction_id = ?
        """,
    
        (
            return_date,
            fine,
            transaction_id
        )
    )
    
    return True 


def get_all_transactions():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT * FROM transactions
            ORDER BY issue_date DESC
            """
        )

        transactions = cursor.fetchall()
        return transactions

    finally:

        connection.close()


def get_transactions_by_member(member_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT *
            FROM transactions
            WHERE member_id = ?
            ORDER BY issue_date DESC
            """,

            (member_id,)
        )

        member_transactions = cursor.fetchall()
        return member_transactions

    finally:

        connection.close()


def get_transactions_by_book(book_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT *
            FROM transactions
            WHERE book_id = ?
            ORDER BY issue_date DESC
            """,

            (book_id,)
        )

        book_transactions = cursor.fetchall()
        return book_transactions

    finally:

        connection.close()


def get_overdue_transactions():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT *
            FROM transactions
            WHERE status = "Issued"
            AND due_date < CURRENT_DATE
            ORDER BY due_date ASC
            """
        )

        overdue_transactions = cursor.fetchall()
        return overdue_transactions

    finally:

        connection.close()