from modules.book_repository import(
    add_book,
    get_all_books,
    get_book_by_id,
    update_book,
    soft_delete_book
)

def create_book(book_id, title, author, category, quantity, db_name="library.db"):

    if quantity <= 0:
        return False

    return add_book(
        book_id,
        title,
        author,
        category,
        quantity,
        db_name
    )

def get_books(db_name="library.db"):

    return get_all_books(db_name)

def get_book(book_id, db_name="library.db"):

    return get_book_by_id(book_id, db_name)

def edit_book(book_id, title, author, category, quantity, db_name="library.db"):

    if quantity <= 0:
        return False

    return update_book(
        book_id,
        title,
        author,
        category,
        quantity,
        db_name
    )

def delete_book(book_id, db_name="library.db"):

    return soft_delete_book(book_id, db_name)