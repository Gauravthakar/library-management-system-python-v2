from database.database import get_connection
from datetime import datetime
import sqlite3

def add_member(member_id, name, phone, email, address):

    join_date = datetime.now().strftime("%Y-%m-%d")
    is_active = 1

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO members(
            member_id,
            name,
            phone,
            email,
            address,
            join_date,
            is_active
            )

            VALUES(?, ?, ?, ?, ?, ?, ?)
            """,

            (
                member_id,
                name,
                phone,
                email,
                address,
                join_date,
                is_active
            )
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def get_all_members():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT *
            FROM members
            WHERE is_active = 1
            ORDER BY name ASC
            """
        )

        members = cursor.fetchall()
        return members

    finally:
        connection.close()


def get_member_by_id(member_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT *
            FROM members
            WHERE member_id = ?
            AND is_active = 1
            """,

            (member_id,)
        )

        member = cursor.fetchone()
        return member

    finally:
        connection.close()


def update_member(member_id, name, phone, email, address):

    member = get_member_by_id(member_id)
    if member is None:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE members
            SET
                name = ?,
                phone = ?,
                email = ?,
                address = ?
            WHERE member_id = ?
            """,

            (
                name,
                phone,
                email,
                address,
                member_id
            )
        )

        connection.commit()
        return True

    finally:
        connection.close()


def soft_delete_member(member_id):

    member = get_member_by_id(member_id)
    if member is None:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE members
            SET is_active = 0
            WHERE member_id = ?
            """,

            (member_id,)
        )

        connection.commit()
        return True

    finally:
        connection.close()