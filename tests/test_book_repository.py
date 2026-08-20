from modules.book_repository import (
    add_book
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