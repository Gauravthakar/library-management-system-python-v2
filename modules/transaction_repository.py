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

    finally:
        connection.close()