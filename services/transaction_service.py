from modules.transaction_repository import (
    get_active_transaction,
    update_return_transaction,
    get_all_transactions,
    get_transactions_by_member,
    get_transactions_by_book,
    get_overdue_transactions,
    get_currently_issued_books,
    get_fine_reports
)
from modules.book_repository import issue_book

def issue_book_to_member(book_id, member_id, db_name="library.db"):

    return issue_book(book_id, member_id, db_name)

def return_book_from_member(book_id, member_id, db_name="library.db"):

    from modules.book_repository import return_book

    return return_book(book_id, member_id, db_name)

def get_transactions():

    return get_all_transactions()

def get_member_transactions(member_id):

    return get_transactions_by_member(member_id)

def get_book_transactions(book_id):

    return get_transactions_by_book(book_id)

def get_active_transaction_for_member(book_id, member_id):

    return get_active_transaction(book_id, member_id)

def get_overdue_books():

    return get_overdue_transactions()

def get_currently_issued():

    return get_currently_issued_books()

def get_fine_report():

    return get_fine_reports()