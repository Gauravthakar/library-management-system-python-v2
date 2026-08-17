from modules.transaction_repository import (
    get_transactions_by_member, 
    get_transactions_by_book,
    add_transaction
    )

from database.database import create_tables, get_connection
import pytest
import os

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