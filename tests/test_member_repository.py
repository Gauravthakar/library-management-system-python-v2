from modules.member_repository import (
    add_member,
    get_all_members,
    get_member_by_id,
    update_member,
    soft_delete_member
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


def test_add_member(test_database):

    result = add_member(
        "M001",
        "Test Member",
        "9999999999",
        "test@example.com",
        "Test Address",
        "library_test.db"
    )

    assert result is True

    cursor = test_database.cursor()

    cursor.execute(
        """
        SELECT *
        FROM members
        WHERE member_id = ?
        """,
        ("M001",)
    )

    member = cursor.fetchone()

    assert member is not None
    assert member[0] == "M001"
    assert member[1] == "Test Member"
    assert member[2] == "9999999999"
    assert member[3] == "test@example.com"
    assert member[4] == "Test Address"
    assert member[6] == 1


def test_add_member_duplicate_id(test_database):

    result = add_member(
        "M001",
        "First Member",
        "9999999999",
        "first@example.com",
        "First Address",
        "library_test.db"
    )

    assert result is True

    result = add_member(
        "M001",
        "Second Member",
        "8888888888",
        "second@example.com",
        "Second Address",
        "library_test.db"
    )

    assert result is False


def test_get_all_members(test_database):

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
            "Gaurav",
            "9999999999",
            "gaurav@example.com",
            "Address 1",
            "2026-08-25",
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
            "M002",
            "Rahul",
            "8888888888",
            "rahul@example.com",
            "Address 2",
            "2026-08-25",
            1
        )
    )

    test_database.commit()

    members = get_all_members("library_test.db")

    assert len(members) == 2


def test_get_all_members_excludes_inactive(test_database):

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
            "Inactive Member",
            "8888888888",
            "inactive@example.com",
            "Inactive Address",
            "2026-08-25",
            0
        )
    )

    test_database.commit()

    members = get_all_members("library_test.db")

    assert members == []


def test_get_member_by_id(test_database):

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
            "2026-08-25",
            1
        )
    )

    test_database.commit()

    member = get_member_by_id(
        "M001",
        "library_test.db"
    )

    assert member is not None
    assert member[0] == "M001"
    assert member[1] == "Test Member"
    assert member[2] == "9999999999"
    assert member[3] == "test@example.com"
    assert member[4] == "Test Address"
    assert member[6] == 1


def test_get_member_by_id_not_found(test_database):

    member = get_member_by_id(
        "M999",
        "library_test.db"
    )

    assert member is None


def test_get_member_by_id_inactive(test_database):

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
            "Inactive Member",
            "8888888888",
            "inactive@example.com",
            "Inactive Address",
            "2026-08-25",
            0
        )
    )

    test_database.commit()

    member = get_member_by_id(
        "M002",
        "library_test.db"
    )

    assert member is None


def test_update_member(test_database):

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
            "Old Name",
            "9999999999",
            "old@example.com",
            "Old Address",
            "2026-08-25",
            1
        )
    )

    test_database.commit()

    result = update_member(
        "M001",
        "New Name",
        "8888888888",
        "new@example.com",
        "New Address",
        "library_test.db"
    )

    assert result is True

    cursor.execute(
        """
        SELECT name, phone, email, address
        FROM members
        WHERE member_id = ?
        """,
        ("M001",)
    )

    member = cursor.fetchone()

    assert member[0] == "New Name"
    assert member[1] == "8888888888"
    assert member[2] == "new@example.com"
    assert member[3] == "New Address"


def test_update_member_not_found(test_database):

    result = update_member(
        "M999",
        "New Name",
        "8888888888",
        "new@example.com",
        "New Address",
        "library_test.db"
    )

    assert result is False


def test_soft_delete_member(test_database):

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
            "Delete Member",
            "8888888888",
            "delete@example.com",
            "Delete Address",
            "2026-08-25",
            1
        )
    )

    test_database.commit()

    result = soft_delete_member(
        "M002",
        "library_test.db"
    )

    assert result is True

    cursor.execute(
        """
        SELECT is_active
        FROM members
        WHERE member_id = ?
        """,
        ("M002",)
    )

    member = cursor.fetchone()

    assert member[0] == 0


def test_soft_delete_member_not_found(test_database):

    result = soft_delete_member(
        "M999",
        "library_test.db"
    )

    assert result is False