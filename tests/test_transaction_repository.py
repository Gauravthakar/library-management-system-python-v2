from modules.transaction_repository import (
    get_transactions_by_member, 
    get_transactions_by_book,
    add_transaction,
    get_active_transaction,
    update_return_transaction,
    get_all_transactions,
    get_overdue_transactions
    )

from database.database import create_tables, get_connection
import pytest
import os
import sqlite3

@pytest.fixture
def test_database():

    if os.path.exists("database/library_test.db"):
        os.remove("database/library_test.db")
        
    create_tables("library_test.db")

    connection = get_connection("library_test.db")
    cursor = connection.cursor()

    cursor.execute(
    """
    INSERT INTO books (
        book_id,
        title,
        author,
        category,
        quantity,
        available_quantity,
        created_at,
        is_active
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        "B001",
        "Python Basics",
        "Test Author",
        "Programming",
        1,
        1,
        "2026-08-14",
        1
    )
)

    cursor.execute(
    """
    INSERT INTO members (
        member_id,
        name,
        phone,
        email,
        address,
        join_date,
        is_active
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        "M001",
        "Test Member",
        "9999999999",
        "Test@example.com",
        "Test Address",
        "2026-08-14",
        1
    )
)

    cursor.execute(
    """
    INSERT INTO transactions (
        book_id,
        member_id,
        issue_date,
        due_date,
        return_date,
        fine,
        status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        "B001",
        "M001",
        "2026-08-05",
        "2026-08-12",
        None,
        0,
        "Issued"
    )
)

    connection.commit()

    yield connection

    connection.close()

    


def test_get_transactions_by_member(test_database):

    transactions = get_transactions_by_member("M001", "library_test.db")

    assert len(transactions) == 1
    assert transactions[0][1] == "B001"

def test_get_transactions_by_member_not_found():

    transactions = get_transactions_by_member("M999")

    assert transactions == []

def test_get_transactions_by_book():

    transactions = get_transactions_by_book("B001")

    assert len(transactions) == 1
    assert transactions[0][1] == "B001"

def test_get_transactions_by_book_not_found():

    transactions = get_transactions_by_book("B999")

    assert transactions == []


def test_add_transaction(test_database):

    result = add_transaction(
        test_database,
        "B001",
        "M001",
        "2026-08-14",
        "2026-08-21"
    )

    assert result is True

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE book_id = ? AND member_id = ?
        """,

        ("B001", "M001")
    )

    transaction_count = cursor.fetchone()[0]

    assert transaction_count == 2


def test_add_transaction_invalid_book(test_database):

    result = add_transaction(
        test_database,
        "B999",
        "M001",
        "2026-08-14",
        "2026-08-21"
    )

    assert result is False

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE book_id = ?
        """,

        ("B999",)
    )

    transaction_count = cursor.fetchone()[0]

    assert transaction_count == 0


def test_add_transaction_invalid_member(test_database):

    result = add_transaction(
        test_database,
        "B001",
        "M999",
        "2026-08-14",
        "2026-08-21"
    )

    assert result is False

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE member_id = ?
        """,

        ("M999",)
    )

    transaction_count = cursor.fetchone()[0]

    assert transaction_count == 0


def test_add_transaction_default_values(test_database):

    result = add_transaction(
        test_database,
        "B001",
        "M001",
        "2026-08-14",
        "2026-08-21"
    )

    assert result is True

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT return_date, fine, status
        FROM transactions
        ORDER BY transaction_id DESC
        LIMIT 1
        """
    )

    transaction = cursor.fetchone()

    assert transaction[0] is None
    assert transaction[1] == 0
    assert transaction[2] == "Issued"


def test_add_transaction_missing_issue_date(test_database):

    result = add_transaction(
        test_database,
        "B001",
        "M001",
        None,
        "2026-08-21"
    )

    assert result is False

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        """
    )

    transaction_count = cursor.fetchone()[0]

    assert transaction_count == 1


def test_add_transaction_missing_due_date(test_database):

    result = add_transaction(
        test_database,
        "B001",
        "M001",
        "2026-08-14",
        None
    )

    assert result is False

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        """
    )

    transaction_count = cursor.fetchone()[0]

    assert transaction_count == 1


def test_get_active_transaction(test_database):

    transaction = get_active_transaction(
        "B001",
        "M001",
        "library_test.db"
    )

    assert transaction is not None
    assert transaction[1] == "B001"
    assert transaction[2] == "M001"
    assert transaction[7] == "Issued"


def test_get_active_transaction_not_found(test_database):

    transaction = get_active_transaction(
        "B001",
        "M999",
        "library_test.db"
    )

    assert transaction is None


def test_get_active_transaction_returned(test_database):

    transaction = get_active_transaction(
        "B001",
        "M001",
        "library_test.db"
    )

    transaction_id = transaction[0]

    update_return_transaction(
        test_database,
        transaction_id,
        "2026-08-14",
        10
    )

    active_transaction = get_active_transaction(
        "B001",
        "M001",
        "library_test.db"
    )

    assert active_transaction is None


def test_update_return_transaction(test_database):

    result = update_return_transaction(
        test_database,
        1,
        "2026-08-14",
        10
    )

    assert result is True

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT
            return_date,
            fine,
            status
        FROM transactions
        WHERE transaction_id = ?
        """,

        (1,)
    )

    transaction = cursor.fetchone()

    assert transaction[0] == "2026-08-14"
    assert transaction[1] == 10
    assert transaction[2] == "Returned"


def test_update_return_transaction_not_found(test_database):

    result = update_return_transaction(
        test_database,
        999,
        "2026-08-14",
        10
    )

    assert result is False

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        """
    )

    transaction_count = cursor.fetchone()[0]

    assert transaction_count == 1


def test_update_return_transaction_negative_fine(test_database):

    result = update_return_transaction(
        test_database,
        1,
        "2026-08-14",
        -10
    )

    assert result is False

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT return_date, fine, status
        FROM transactions
        WHERE transaction_id = ?
        """,
        (1,)
    )

    transaction = cursor.fetchone()

    assert transaction[0] is None
    assert transaction[1] == 0
    assert transaction[2] == "Issued"


def test_database_rejects_negative_fine(test_database):

    cursor = test_database.cursor()

    with pytest.raises(sqlite3.IntegrityError):

        cursor.execute(
            """
            UPDATE transactions
            SET fine = ?
            WHERE transaction_id = ?
            """,
            (-10, 1)
        )


def test_get_all_transactions(test_database):

    transactions = get_all_transactions("library_test.db")

    assert len(transactions) == 1
    assert transactions[0][1] == "B001"
    assert transactions[0][2] == "M001"
    assert transactions[0][7] == "Issued"


def test_get_all_transactions_empty(test_database):

    cursor = test_database.cursor()

    cursor.execute(
        """
        DELETE FROM transactions
        """
    )

    test_database.commit()

    transactions = get_all_transactions("library_test.db")

    assert transactions == []


def test_get_all_transactions_order(test_database):

    cursor = test_database.cursor()

    cursor.execute(
        """
        INSERT INTO transactions (
            book_id,
            member_id,
            issue_date,
            due_date,
            return_date,
            fine,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "B001",
            "M001",
            "2026-08-15",
            "2026-08-22",
            None,
            0,
            "Issued"
        )
    )

    test_database.commit()

    transactions = get_all_transactions("library_test.db")

    assert len(transactions) == 2
    assert transactions[0][3] == "2026-08-15"
    assert transactions[1][3] == "2026-08-05"


def test_get_transactions_by_member_filters_correctly(test_database):

    cursor = test_database.cursor()

    cursor.execute(
        """
        INSERT INTO members (
            member_id,
            name,
            phone,
            email,
            address,
            join_date,
            is_active
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "M002",
            "Second Member",
            "8888888888",
            "second@example.com",
            "Second Address",
            "2026-08-15",
            1
        )
    )

    cursor.execute(
        """
        INSERT INTO transactions (
            book_id,
            member_id,
            issue_date,
            due_date,
            return_date,
            fine,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "B001",
            "M002",
            "2026-08-15",
            "2026-08-22",
            None,
            0,
            "Issued"
        )
    )

    test_database.commit()

    transactions = get_transactions_by_member(
        "M001",
        "library_test.db"
    )

    assert len(transactions) == 1
    assert transactions[0][2] == "M001"


def test_get_transactions_by_member_order(test_database):

    cursor = test_database.cursor()

    cursor.execute(
        """
        INSERT INTO transactions (
            book_id,
            member_id,
            issue_date,
            due_date,
            return_date,
            fine,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "B001",
            "M001",
            "2026-08-16",
            "2026-08-23",
            None,
            0,
            "Issued"
        )
    )

    test_database.commit()

    transactions = get_transactions_by_member(
        "M001",
        "library_test.db"
    )

    assert len(transactions) == 2
    assert transactions[0][3] == "2026-08-16"
    assert transactions[1][3] == "2026-08-05"


def test_get_transactions_by_book_filters_correctly(test_database):

    cursor = test_database.cursor()

    cursor.execute(
        """
        INSERT INTO books (
            book_id,
            title,
            author,
            category,
            quantity,
            available_quantity,
            created_at,
            is_active
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "B002",
            "Django Basics",
            "Test Author 2",
            "Programming",
            1,
            1,
            "2026-08-15",
            1
        )
    )

    cursor.execute(
        """
        INSERT INTO transactions (
            book_id,
            member_id,
            issue_date,
            due_date,
            return_date,
            fine,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "B002",
            "M001",
            "2026-08-15",
            "2026-08-22",
            None,
            0,
            "Issued"
        )
    )

    test_database.commit()

    transactions = get_transactions_by_book(
        "B001",
        "library_test.db"
    )

    assert len(transactions) == 1
    assert transactions[0][1] == "B001"


def test_get_transactions_by_book_order(test_database):

    cursor = test_database.cursor()

    cursor.execute(
        """
        INSERT INTO transactions (
            book_id,
            member_id,
            issue_date,
            due_date,
            return_date,
            fine,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "B001",
            "M001",
            "2026-08-16",
            "2026-08-23",
            None,
            0,
            "Issued"
        )
    )

    test_database.commit()

    transactions = get_transactions_by_book(
        "B001",
        "library_test.db"
    )

    assert len(transactions) == 2
    assert transactions[0][3] == "2026-08-16"
    assert transactions[1][3] == "2026-08-05"


def test_get_overdue_transactions(test_database):

    overdue_transactions = get_overdue_transactions("library_test.db")

    assert len(overdue_transactions) == 1
    assert overdue_transactions[0][0] == "B001"
    assert overdue_transactions[0][2] == "M001"
    assert overdue_transactions[0][6] == "Issued"


def test_get_overdue_transactions_excludes_returned(test_database):

    cursor = test_database.cursor()

    cursor.execute(
        """
        UPDATE transactions
        SET status = 'Returned',
            return_date = '2026-08-14'
        WHERE transaction_id = 1
        """
    )

    test_database.commit()

    overdue_transactions = get_overdue_transactions(
        "library_test.db"
    )

    assert overdue_transactions == []


def test_get_overdue_transactions_excludes_future_due_date(test_database):

    cursor = test_database.cursor()

    cursor.execute(
        """
        UPDATE transactions
        SET due_date = '2099-12-31'
        WHERE transaction_id = 1
        """
    )

    test_database.commit()

    overdue_transactions = get_overdue_transactions(
        "library_test.db"
    )

    assert overdue_transactions == []


def test_get_overdue_transactions_join_data(test_database):

    cursor = test_database.cursor()

    cursor.execute(
        """
        UPDATE transactions
        SET status = 'Issued',
            due_date = '2026-08-12'
        WHERE transaction_id = 1
        """
    )

    test_database.commit()

    overdue_transactions = get_overdue_transactions(
        "library_test.db"
    )

    assert len(overdue_transactions) == 1
    assert overdue_transactions[0][0] == "B001"
    assert overdue_transactions[0][1] == "Python Basics"
    assert overdue_transactions[0][2] == "M001"
    assert overdue_transactions[0][3] == "Test Member"


def test_get_overdue_transactions_order(test_database):

    cursor = test_database.cursor()

    cursor.execute(
        """
        INSERT INTO transactions (
            book_id,
            member_id,
            issue_date,
            due_date,
            return_date,
            fine,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "B001",
            "M001",
            "2026-08-10",
            "2026-08-10",
            None,
            0,
            "Issued"
        )
    )

    test_database.commit()

    overdue_transactions = get_overdue_transactions(
        "library_test.db"
    )

    assert len(overdue_transactions) == 2
    assert overdue_transactions[0][5] == "2026-08-10"
    assert overdue_transactions[1][5] == "2026-08-12"