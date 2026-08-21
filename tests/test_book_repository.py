from modules.book_repository import (
    add_book,
    get_all_books,
    get_book_by_id,
    update_book,
    soft_delete_book
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