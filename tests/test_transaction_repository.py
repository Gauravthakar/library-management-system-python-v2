from modules.transaction_repository import (
    get_transactions_by_member, 
    get_transactions_by_book
    )

from database.database import create_tables

create_tables("library_test.db")


def test_get_transactions_by_member():

    transactions = get_transactions_by_member("M001")

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