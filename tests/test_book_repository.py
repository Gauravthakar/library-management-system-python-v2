from modules.book_repository import (
    add_book,
    get_all_books,
    get_book_by_id,
    update_book,
    soft_delete_book,
    return_book,
    issue_book,
    calculate_fine
)

from database.database import create_tables, get_connection

import pytest
import os
import sqlite3
from datetime import datetime

@pytest.fixture
def test_database():

    if os.path.exists("database/library_test.db"):
        os.remove("database/library_test.db")

    create_tables("library_test.db")

    connection = get_connection("library_test.db")

    yield connection

    connection.close()


def test_add_book(test_database):

    result = add_book(
        "B001",
        "Python Basics",
        "Test Author",
        "Programming",
        5,
        "library_test.db"
    )

    assert result is True

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT *
        FROM books
        WHERE book_id = ?
        """,
        ("B001",)
    )

    book = cursor.fetchone()

    assert book is not None
    assert book[0] == "B001"
    assert book[1] == "Python Basics"
    assert book[2] == "Test Author"
    assert book[3] == "Programming"
    assert book[4] == 5
    assert book[5] == 5
    assert book[7] == 1


def test_add_book_duplicate_id(test_database):

    first_result = add_book(
        "B001",
        "Python Basics",
        "Test Author",
        "Programming",
        5,
        "library_test.db"
    )

    assert first_result is True

    second_result = add_book(
        "B001",
        "Django Basics",
        "Another Author",
        "Programming",
        10,
        "library_test.db"
    )

    assert second_result is False

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM books
        WHERE book_id = ?
        """,
        ("B001",)
    )

    book_count = cursor.fetchone()[0]

    assert book_count == 1

    cursor.execute(
        """
        SELECT title, quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B001",)
    )

    book = cursor.fetchone()

    assert book[0] == "Python Basics"
    assert book[1] == 5


def test_add_book_zero_quantity(test_database):

    result = add_book(
        "B002",
        "Django Basics",
        "Test Author",
        "Programming",
        0,
        "library_test.db"
    )

    assert result is True

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT quantity, available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B002",)
    )

    book = cursor.fetchone()

    assert book is not None
    assert book[0] == 0
    assert book[1] == 0


def test_add_book_negative_quantity(test_database):

    result = add_book(
        "B003",
        "Flask Basics",
        "Test Author",
        "Programming",
        -1,
        "library_test.db"
    )

    assert result is False

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM books
        WHERE book_id = ?
        """,
        ("B003",)
    )

    book_count = cursor.fetchone()[0]

    assert book_count == 0


def test_add_book_missing_title(test_database):

    result = add_book(
        "B004",
        None,
        "Test Author",
        "Programming",
        5,
        "library_test.db"
    )

    assert result is False

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM books
        WHERE book_id = ?
        """,
        ("B004",)
    )

    book_count = cursor.fetchone()[0]

    assert book_count == 0


def test_add_book_missing_author(test_database):

    result = add_book(
        "B005",
        "Java Basics",
        None,
        "Programming",
        5,
        "library_test.db"
    )

    assert result is False

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM books
        WHERE book_id = ?
        """,
        ("B005",)
    )

    book_count = cursor.fetchone()[0]

    assert book_count == 0


def test_add_book_missing_category(test_database):

    result = add_book(
        "B006",
        "C# Basics",
        "Test Author",
        None,
        5,
        "library_test.db"
    )

    assert result is False

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM books
        WHERE book_id = ?
        """,
        ("B006",)
    )

    book_count = cursor.fetchone()[0]

    assert book_count == 0


def test_get_all_books(test_database):

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
            "B001",
            "Python Basics",
            "Test Author",
            "Programming",
            5,
            5,
            "2026-08-20",
            1
        )
    )

    test_database.commit()

    books = get_all_books(
        "library_test.db"
    )

    assert len(books) == 1
    assert books[0][0] == "B001"
    assert books[0][1] == "Python Basics"
    assert books[0][7] == 1


def test_get_all_books_excludes_inactive_books(test_database):

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
            "Test Author",
            "Programming",
            5,
            5,
            "2026-08-20",
            0
        )
    )

    test_database.commit()

    books = get_all_books(
        "library_test.db"
    )

    assert books == []


def test_get_all_books_order(test_database):

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
            "B001",
            "Python Basics",
            "Test Author",
            "Programming",
            5,
            5,
            "2026-08-20",
            1
        )
    )

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
            "Test Author",
            "Programming",
            5,
            5,
            "2026-08-20",
            1
        )
    )

    test_database.commit()

    books = get_all_books(
        "library_test.db"
    )

    assert len(books) == 2
    assert books[0][1] == "Django Basics"
    assert books[1][1] == "Python Basics"


def test_get_book_by_id(test_database):

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
            "B001",
            "Python Basics",
            "Test Author",
            "Programming",
            5,
            5,
            "2026-08-20",
            1
        )
    )

    test_database.commit()

    book = get_book_by_id(
        "B001",
        "library_test.db"
    )

    assert book is not None
    assert book[0] == "B001"
    assert book[1] == "Python Basics"
    assert book[2] == "Test Author"
    assert book[3] == "Programming"
    assert book[4] == 5
    assert book[5] == 5
    assert book[7] == 1


def test_get_book_by_id_not_found(test_database):

    book = get_book_by_id(
        "B999",
        "library_test.db"
    )

    assert book is None


def test_get_book_by_id_inactive_book(test_database):

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
            "Test Author",
            "Programming",
            5,
            5,
            "2026-08-20",
            0
        )
    )

    test_database.commit()

    book = get_book_by_id(
        "B002",
        "library_test.db"
    )

    assert book is None


def test_update_book(test_database):

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
            "B001",
            "Python Basics",
            "Old Author",
            "Programming",
            5,
            5,
            "2026-08-20",
            1
        )
    )

    test_database.commit()

    result = update_book(
        "B001",
        "Advanced Python",
        "New Author",
        "Advanced Programming",
        10,
        "library_test.db"
    )

    assert result is True

    cursor.execute(
        """
        SELECT
            title,
            author,
            category,
            quantity,
            available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B001",)
    )

    book = cursor.fetchone()

    assert book[0] == "Advanced Python"
    assert book[1] == "New Author"
    assert book[2] == "Advanced Programming"
    assert book[3] == 10
    assert book[4] == 10


def test_update_book_with_issued_books(test_database):

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
            "Python Advanced",
            "Test Author",
            "Programming",
            5,
            3,
            "2026-08-20",
            1
        )
    )

    test_database.commit()

    result = update_book(
        "B002",
        "Python Advanced Updated",
        "New Author",
        "Advanced Programming",
        6,
        "library_test.db"
    )

    assert result is True

    cursor.execute(
        """
        SELECT
            quantity,
            available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B002",)
    )

    book = cursor.fetchone()

    assert book[0] == 6
    assert book[1] == 4


def test_update_book_decrease_quantity(test_database):

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
            "B003",
            "Flask Basics",
            "Test Author",
            "Programming",
            5,
            3,
            "2026-08-20",
            1
        )
    )

    test_database.commit()

    result = update_book(
        "B003",
        "Flask Basics Updated",
        "New Author",
        "Web Development",
        4,
        "library_test.db"
    )

    assert result is True

    cursor.execute(
        """
        SELECT
            quantity,
            available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B003",)
    )

    book = cursor.fetchone()

    assert book[0] == 4
    assert book[1] == 2


def test_update_book_quantity_less_than_issued(test_database):

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
            "B004",
            "Java Basics",
            "Test Author",
            "Programming",
            5,
            3,
            "2026-08-20",
            1
        )
    )

    test_database.commit()

    result = update_book(
        "B004",
        "Java Updated",
        "New Author",
        "Programming",
        1,
        "library_test.db"
    )

    assert result is False

    cursor.execute(
        """
        SELECT
            title,
            quantity,
            available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B004",)
    )

    book = cursor.fetchone()

    assert book[0] == "Java Basics"
    assert book[1] == 5
    assert book[2] == 3


def test_update_book_not_found(test_database):

    result = update_book(
        "B999",
        "Unknown Book",
        "Unknown Author",
        "Programming",
        5,
        "library_test.db"
    )

    assert result is False

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM books
        """
    )

    book_count = cursor.fetchone()[0]

    assert book_count == 0


def test_update_inactive_book(test_database):

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
            "B005",
            "Deleted Book",
            "Old Author",
            "Programming",
            5,
            5,
            "2026-08-20",
            0
        )
    )

    test_database.commit()

    result = update_book(
        "B005",
        "Updated Book",
        "New Author",
        "Programming",
        10,
        "library_test.db"
    )

    assert result is False

    cursor.execute(
        """
        SELECT
            title,
            quantity,
            available_quantity,
            is_active
        FROM books
        WHERE book_id = ?
        """,
        ("B005",)
    )

    book = cursor.fetchone()

    assert book[0] == "Deleted Book"
    assert book[1] == 5
    assert book[2] == 5
    assert book[3] == 0


def test_update_book_quantity_equal_to_issued(test_database):

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
            "B006",
            "SQL Basics",
            "Test Author",
            "Database",
            5,
            3,
            "2026-08-20",
            1
        )
    )

    test_database.commit()

    result = update_book(
        "B006",
        "SQL Basics Updated",
        "New Author",
        "Database",
        2,
        "library_test.db"
    )

    assert result is True

    cursor.execute(
        """
        SELECT
            quantity,
            available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B006",)
    )

    book = cursor.fetchone()

    assert book[0] == 2
    assert book[1] == 0


def test_soft_delete_book(test_database):

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
            "B007",
            "Django Basics",
            "Test Author",
            "Programming",
            5,
            5,
            "2026-08-20",
            1
        )
    )

    test_database.commit()

    result = soft_delete_book(
        "B007",
        "library_test.db"
    )

    assert result is True

    cursor.execute(
        """
        SELECT is_active
        FROM books
        WHERE book_id = ?
        """,
        ("B007",)
    )

    book = cursor.fetchone()

    assert book[0] == 0


def test_soft_delete_book_not_found(test_database):

    result = soft_delete_book(
        "B999",
        "library_test.db"
    )

    assert result is False

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM books
        """
    )

    book_count = cursor.fetchone()[0]

    assert book_count == 0


def test_soft_delete_already_inactive_book(test_database):

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
            "B008",
            "Deleted Book",
            "Test Author",
            "Programming",
            5,
            5,
            "2026-08-20",
            0
        )
    )

    test_database.commit()

    result = soft_delete_book(
        "B008",
        "library_test.db"
    )

    assert result is False

    cursor.execute(
        """
        SELECT is_active
        FROM books
        WHERE book_id = ?
        """,
        ("B008",)
    )

    book = cursor.fetchone()

    assert book[0] == 0


def test_soft_delete_book_with_issued_copies(test_database):

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
            "B009",
            "Python Advanced",
            "Test Author",
            "Programming",
            5,
            3,
            "2026-08-20",
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
            "test@example.com",
            "Test Address",
            "2026-08-20",
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
            "B009",
            "M001",
            "2026-08-20",
            "2026-08-27",
            None,
            0,
            "Issued"
        )
    )

    test_database.commit()

    result = soft_delete_book(
        "B009",
        "library_test.db"
    )

    assert result is True

    cursor.execute(
        """
        SELECT
            is_active,
            quantity,
            available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B009",)
    )

    book = cursor.fetchone()

    assert book[0] == 0
    assert book[1] == 5
    assert book[2] == 3

    cursor.execute(
        """
        SELECT
            status,
            return_date
        FROM transactions
        WHERE book_id = ?
        """,
        ("B009",)
    )

    transaction = cursor.fetchone()

    assert transaction[0] == "Issued"
    assert transaction[1] is None


def test_return_book_after_soft_delete(test_database):

    cursor = test_database.cursor()

    # Add member
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
            "test@example.com",
            "Test Address",
            "2026-08-20",
            1
        )
    )

    # Add book with one issued copy
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
            "B010",
            "Python Advanced",
            "Test Author",
            "Programming",
            5,
            4,
            "2026-08-20",
            1
        )
    )

    # Add active transaction
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
            "B010",
            "M001",
            "2026-08-20",
            "2026-08-27",
            None,
            0,
            "Issued"
        )
    )

    test_database.commit()

    # Soft delete the book
    result = soft_delete_book(
        "B010",
        "library_test.db"
    )

    assert result is True

    # Return the issued book
    result = return_book(
        "B010",
        "M001",
        "library_test.db"
    )

    assert result is True

    # Check book availability
    cursor.execute(
        """
        SELECT available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B010",)
    )

    book = cursor.fetchone()

    assert book[0] == 5

    # Check transaction
    cursor.execute(
        """
        SELECT status, return_date
        FROM transactions
        WHERE book_id = ? AND member_id = ?
        """,
        ("B010", "M001")
    )

    transaction = cursor.fetchone()

    assert transaction[0] == "Returned"
    assert transaction[1] is not None


def test_issue_book_soft_deleted_book(test_database):

    cursor = test_database.cursor()

    # Add another book
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
            "B011",
            "Django Advanced",
            "Test Author",
            "Programming",
            5,
            5,
            "2026-08-20",
            1
        )
    )

    test_database.commit()

    # Soft delete the book
    result = soft_delete_book(
        "B011",
        "library_test.db"
    )

    assert result is True

    # Try to issue the deleted book
    result = issue_book(
        "B011",
        "M001"
    )

    assert result is False

    # Verify no transaction was created
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE book_id = ?
        """,
        ("B011",)
    )

    transaction_count = cursor.fetchone()[0]

    assert transaction_count == 0


def test_issue_book_no_available_quantity(test_database):

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
            "B012",
            "Python Advanced",
            "Test Author",
            "Programming",
            5,
            0,
            "2026-08-20",
            1
        )
    )

    test_database.commit()

    result = issue_book(
        "B012",
        "M001"
    )

    assert result is False

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE book_id = ?
        """,
        ("B012",)
    )

    transaction_count = cursor.fetchone()[0]

    assert transaction_count == 0

    cursor.execute(
        """
        SELECT available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B012",)
    )

    book = cursor.fetchone()

    assert book[0] == 0


def test_issue_book_rollback_on_transaction_failure(test_database, monkeypatch):

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
            "B013",
            "Flask Advanced",
            "Test Author",
            "Programming",
            5,
            5,
            "2026-08-20",
            1
        )
    )

    test_database.commit()

    def fake_add_transaction(*args, **kwargs):
        raise sqlite3.IntegrityError("Simulated transaction failure")

    monkeypatch.setattr(
        "modules.book_repository.add_transaction",
        fake_add_transaction
    )

    result = issue_book(
        "B013",
        "M001"
    )

    assert result is False

    cursor.execute(
        """
        SELECT available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B013",)
    )

    book = cursor.fetchone()

    assert book[0] == 5

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE book_id = ?
        """,
        ("B013",)
    )

    transaction_count = cursor.fetchone()[0]

    assert transaction_count == 0


def test_issue_book_updates_book_and_transaction(test_database):

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
            "M001",
            "Test Member",
            "9999999999",
            "test@example.com",
            "Test Address",
            "2026-08-22",
            1
        )
    )

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
            "B014",
            "FastAPI Basics",
            "Test Author",
            "Programming",
            5,
            5,
            "2026-08-22",
            1
        )
    )

    test_database.commit()

    result = issue_book(
        "B014",
        "M001",
        "library_test.db"
    )

    assert result is True

    # Check book quantity
    cursor.execute(
        """
        SELECT quantity, available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B014",)
    )

    book = cursor.fetchone()

    assert book[0] == 5
    assert book[1] == 4

    # Check transaction
    cursor.execute(
        """
        SELECT
            book_id,
            member_id,
            issue_date,
            due_date,
            return_date,
            fine,
            status
        FROM transactions
        WHERE book_id = ?
        ORDER BY transaction_id DESC
        LIMIT 1
        """,
        ("B014",)
    )

    transaction = cursor.fetchone()

    assert transaction is not None
    assert transaction[0] == "B014"
    assert transaction[1] == "M001"
    assert transaction[2] == datetime.now().strftime("%Y-%m-%d")
    assert transaction[4] is None
    assert transaction[5] == 0
    assert transaction[6] == "Issued"


def test_return_book_updates_book_and_transaction(test_database):

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
            "M001",
            "Test Member",
            "9999999999",
            "test@example.com",
            "Test Address",
            "2026-08-22",
                1
        )
    )

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
            "B015",
            "Django Basics",
            "Test Author",
            "Programming",
            5,
            4,
            "2026-08-24",
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
            "B015",
            "M001",
            "2026-08-20",
            "2099-08-27",
            None,
            0,
            "Issued"
        )
    )

    test_database.commit()

    result = return_book(
        "B015",
        "M001",
        "library_test.db"
    )

    assert result is True

    # Check book quantity
    cursor.execute(
        """
        SELECT quantity, available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B015",)
    )

    book = cursor.fetchone()

    assert book[0] == 5
    assert book[1] == 5

    # Check transaction
    cursor.execute(
        """
        SELECT
            return_date,
            fine,
            status
        FROM transactions
        WHERE book_id = ?
        ORDER BY transaction_id DESC
        LIMIT 1
        """,
        ("B015",)
    )

    transaction = cursor.fetchone()

    assert transaction is not None
    assert transaction[0] == datetime.now().strftime("%Y-%m-%d")
    assert transaction[1] == 0
    assert transaction[2] == "Returned"


def test_return_book_calculates_fine(test_database):

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
            "Fine Test Member",
            "8888888888",
            "fine@example.com",
            "Fine Test Address",
            "2026-08-24",
            1
        )
    )

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
            "B016",
            "Python Advanced",
            "Test Author",
            "Programming",
            5,
            4,
            "2026-08-24",
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
            "B016",
            "M002",
            "2026-08-15",
            "2026-08-20",
            None,
            0,
            "Issued"
        )
    )

    test_database.commit()

    result = return_book(
        "B016",
        "M002",
        "library_test.db"
    )

    assert result is True

    cursor.execute(
        """
        SELECT fine, status
        FROM transactions
        WHERE book_id = ?
        ORDER BY transaction_id DESC
        LIMIT 1
        """,
        ("B016",)
    )

    transaction = cursor.fetchone()

    assert transaction is not None
    assert transaction[0] >= 0
    assert transaction[1] == "Returned"


def test_return_book_already_returned_transaction(test_database):

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
            "M003",
            "Returned Test Member",
            "7777777777",
            "returned@example.com",
            "Returned Test Address",
            "2026-08-24",
            1
        )
    )

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
            "B017",
            "Flask Basics",
            "Test Author",
            "Programming",
            5,
            5,
            "2026-08-24",
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
            "B017",
            "M003",
            "2026-08-15",
            "2026-08-20",
            "2026-08-21",
            10,
            "Returned"
        )
    )

    test_database.commit()

    result = return_book(
        "B017",
        "M003",
        "library_test.db"
    )

    assert result is False

    cursor.execute(
        """
        SELECT available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B017",)
    )

    book = cursor.fetchone()

    assert book[0] == 5

    cursor.execute(
        """
        SELECT return_date, fine, status
        FROM transactions
        WHERE book_id = ?
        """,
        ("B017",)
    )

    transaction = cursor.fetchone()

    assert transaction[0] == "2026-08-21"
    assert transaction[1] == 10
    assert transaction[2] == "Returned"


def test_issue_book_when_no_available_copies(test_database):

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
            "M004",
            "No Copy Test Member",
            "6666666666",
            "nocopy@example.com",
            "No Copy Test Address",
            "2026-08-24",
            1
        )
    )

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
            "B018",
            "Python Zero Copies",
            "Test Author",
            "Programming",
            5,
            0,
            "2026-08-24",
            1
        )
    )

    test_database.commit()

    result = issue_book(
        "B018",
        "M004",
        "library_test.db"
    )

    assert result is False

    cursor.execute(
        """
        SELECT available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B018",)
    )

    book = cursor.fetchone()

    assert book[0] == 0

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE book_id = ?
        """,
        ("B018",)
    )

    transaction_count = cursor.fetchone()[0]

    assert transaction_count == 0


def test_issue_book_invalid_member(test_database):

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
            "B019",
            "Python Advanced",
            "Test Author",
            "Programming",
            5,
            5,
            "2026-08-24",
            1
        )
    )

    test_database.commit()

    result = issue_book(
        "B019",
        "M999",
        "library_test.db"
    )

    assert result is False

    cursor.execute(
        """
        SELECT available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B019",)
    )

    book = cursor.fetchone()

    assert book[0] == 5

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE book_id = ?
        """,
        ("B019",)
    )

    transaction_count = cursor.fetchone()[0]

    assert transaction_count == 0


def test_return_book_without_active_transaction(test_database):

    cursor = test_database.cursor()

    # Add member
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
            "M005",
            "No Transaction Member",
            "5555555555",
            "notransaction@example.com",
            "Test Address",
            "2026-08-24",
            1
        )
    )

    # Add book
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
            "B020",
            "Python Testing",
            "Test Author",
            "Programming",
            5,
            5,
            "2026-08-24",
            1
        )
    )

    test_database.commit()

    # Try to return without an active transaction
    result = return_book(
        "B020",
        "M005",
        "library_test.db"
    )

    assert result is False

    # Book quantity should remain unchanged
    cursor.execute(
        """
        SELECT available_quantity
        FROM books
        WHERE book_id = ?
        """,
        ("B020",)
    )

    book = cursor.fetchone()

    assert book[0] == 5

    # No transaction should exist
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE book_id = ? AND member_id = ?
        """,
        ("B020", "M005")
    )

    transaction_count = cursor.fetchone()[0]

    assert transaction_count == 0


def test_calculate_fine_for_late_return():

    due_date = datetime.strptime(
        "2026-08-20",
        "%Y-%m-%d"
    )

    return_date = datetime.strptime(
        "2026-08-23",
        "%Y-%m-%d"
    )

    fine = calculate_fine(
        due_date,
        return_date
    )

    assert fine == 30