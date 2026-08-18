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


def get_active_transaction(book_id, member_id, db_name="library.db"):

    connection = get_connection(db_name)
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

    connection.commit()
    
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


def get_transactions_by_member(member_id, db_name="library.db"):

    connection = get_connection(db_name)
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


def get_transactions_by_book(book_id, db_name="library.db"):

    connection = get_connection(db_name)
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
            SELECT 
                books.book_id,
                books.title,
                members.member_id,
                members.name,
                transactions.issue_date,
                transactions.due_date,
                transactions.status
            FROM transactions
            INNER JOIN books
                ON transactions.book_id = books.book_id
            INNER JOIN members
                ON transactions.member_id = members.member_id
            WHERE transactions.status = "Issued"
            AND transactions.due_date < CURRENT_DATE
            ORDER BY transactions.due_date ASC
            """
        )

        overdue_transactions = cursor.fetchall()
        return overdue_transactions

    finally:

        connection.close()


def get_currently_issued_books():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                books.book_id,
                books.title,
                members.member_id,
                members.name,
                transactions.issue_date,
                transactions.due_date,
                transactions.status
            FROM transactions
            INNER JOIN books
                ON transactions.book_id = books.book_id
            INNER JOIN members
                ON transactions.member_id = members.member_id
            WHERE transactions.status = "Issued"
            ORDER BY transactions.due_date ASC
            """
        )

        currently_issued = cursor.fetchall()
        return currently_issued

    finally:

        connection.close()


def get_fine_reports():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                books.book_id,
                books.title,
                members.member_id,
                members.name,
                transactions.issue_date,
                transactions.due_date,
                transactions.return_date,
                transactions.fine
            FROM transactions
            INNER JOIN books
                ON transactions.book_id = books.book_id
            INNER JOIN members
                ON transactions.member_id = members.member_id
            WHERE transactions.status = "Returned"
            AND transactions.fine > 0
            ORDER BY transactions.fine DESC
            """
        )

        fine_reports = cursor.fetchall()
        return fine_reports


    finally:

        connection.close()