from services.book_service import *
from services.member_service import *
from services.transaction_service import *

# =========== Book Section ==========
def add_book_menu():

    print("\n===== Add Book =====")

    book_id = input("Enter Book ID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    category = input("Enter Category: ")
    quantity = int(input("Enter Quantity: "))

    result = create_book(
        book_id,
        title,
        author,
        category,
        quantity
    )

    if result:
        print("Book added successfully.")
    else:
        print("Failed to add book.")


def view_books():

    books = get_books()

    if not books:
        print("\nNo books found.")
        return

    print("\n===== Books =====")

    for book in books:
        print(
            f"ID: {book[0]} | "
            f"Title: {book[1]} | "
            f"Author: {book[2]} | "
            f"Category: {book[3]} | "
            f"Quantity: {book[4]} | "
            f"Available: {book[5]}"
        )


def search_book_menu():

    book_id = input("Enter Book ID: ")

    book = get_book(book_id)

    if book is None:
        print("Book not found.")
        return

    print("\n===== Book Details =====")
    print(f"Book ID: {book[0]}")
    print(f"Title: {book[1]}")
    print(f"Author: {book[2]}")
    print(f"Category: {book[3]}")
    print(f"Quantity: {book[4]}")
    print(f"Available Quantity: {book[5]}")


def update_book_menu():

    print("\n===== Update Book =====")

    book_id = input("Enter Book ID: ")

    book = get_book(book_id)

    if book is None:
        print("Book not found.")
        return

    print(f"Current Title: {book[1]}")
    print(f"Current Author: {book[2]}")
    print(f"Current Category: {book[3]}")
    print(f"Current Quantity: {book[4]}")

    title = input("Enter New Title: ")
    author = input("Enter New Author: ")
    category = input("Enter New Category: ")
    quantity = int(input("Enter New Quantity: "))

    result = edit_book(
        book_id,
        title,
        author,
        category,
        quantity
    )

    if result:
        print("Book updated successfully.")
    else:
        print("Failed to update book.")


def delete_book_menu():

    print("\n===== Delete Book =====")

    book_id = input("Enter Book ID: ")

    book = get_book(book_id)

    if book is None:
        print("Book not found.")
        return

    print(f"Book: {book[1]}")

    confirm = input("Are you sure you want to delete this book? (y/n): ")

    if confirm.lower() != "y":
        print("Delete cancelled.")
        return

    result = delete_book(book_id)

    if result:
        print("Book deleted successfully.")
    else:
        print("Failed to delete book.")


def book_menu():

    while True:

        print("\n===== Book Management =====")
        print("1. Add Book")
        print("2. View Books")
        print("3. Search Book")
        print("4. Update Book")
        print("5. Delete Book")
        print("6. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book_menu()

        elif choice == "2":
            view_books()

        elif choice == "3":
            search_book_menu()

        elif choice == "4":
            update_book_menu()

        elif choice == "5":
            delete_book_menu()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")


# ========= Member Section ===========

def add_member_menu():

    print("\n===== Add Member =====")

    member_id = input("Enter Member ID: ")
    name = input("Enter Name: ")
    phone = input("Enter Phone: ")
    email = input("Enter Email: ")
    address = input("Enter Address: ")

    result = create_member(
        member_id,
        name,
        phone,
        email,
        address
    )

    if result:
        print("Member added successfully.")
    else:
        print("Failed to add member.")


def view_members():

    members = get_members()

    if not members:
        print("\nNo members found.")
        return

    print("\n===== Members =====")

    for member in members:
        print(
            f"ID: {member[0]} | "
            f"Name: {member[1]} | "
            f"Phone: {member[2]} | "
            f"Email: {member[3]}"
        )


def search_member_menu():

    print("\n===== Search Member =====")

    member_id = input("Enter Member ID: ")

    member = get_member(member_id)

    if member is None:
        print("Member not found.")
        return

    print("\n===== Member Details =====")
    print(f"Member ID: {member[0]}")
    print(f"Name: {member[1]}")
    print(f"Phone: {member[2]}")
    print(f"Email: {member[3]}")
    print(f"Address: {member[4]}")
    print(f"Join Date: {member[5]}")


def update_member_menu():

    print("\n===== Update Member =====")

    member_id = input("Enter Member ID: ")

    member = get_member(member_id)

    if member is None:
        print("Member not found.")
        return

    print(f"Current Name: {member[1]}")
    print(f"Current Phone: {member[2]}")
    print(f"Current Email: {member[3]}")
    print(f"Current Address: {member[4]}")

    name = input("Enter New Name: ")
    phone = input("Enter New Phone: ")
    email = input("Enter New Email: ")
    address = input("Enter New Address: ")

    result = edit_member(
        member_id,
        name,
        phone,
        email,
        address
    )

    if result:
        print("Member updated successfully.")
    else:
        print("Failed to update member.")


def delete_member_menu():

    print("\n===== Delete Member =====")

    member_id = input("Enter Member ID: ")

    member = get_member(member_id)

    if member is None:
        print("Member not found.")
        return

    print(f"Member: {member[1]}")

    confirm = input("Are you sure you want to delete this member? (y/n): ")

    if confirm.lower() != "y":
        print("Delete cancelled.")
        return

    result = delete_member(member_id)

    if result:
        print("Member deleted successfully.")
    else:
        print("Failed to delete member.")


def member_menu():

    while True:

        print("\n===== Member Management =====")
        print("1. Add Member")
        print("2. View Members")
        print("3. Search Member")
        print("4. Update Member")
        print("5. Delete Member")
        print("6. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_member_menu()

        elif choice == "2":
            view_members()

        elif choice == "3":
            search_member_menu()

        elif choice == "4":
            update_member_menu()

        elif choice == "5":
            delete_member_menu()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")

# ========= Transaction Section ===========

def issue_book_menu():

    print("\n===== Issue Book =====")

    book_id = input("Enter Book ID: ")
    member_id = input("Enter Member ID: ")

    result = issue_book_to_member(book_id, member_id)

    if result:
        print("Book issued successfully.")
    else:
        print("Failed to issue book.")


def return_book_menu():

    print("\n===== Return Book =====")

    book_id = input("Enter Book ID: ")
    member_id = input("Enter Member ID: ")

    result = return_book_from_member(
        book_id,
        member_id
    )

    if result:
        print("Book returned successfully.")
    else:
        print("Failed to return book.")


def view_transactions():

    transactions = get_transactions()

    if not transactions:
        print("\nNo transactions found.")
        return

    print("\n===== All Transactions =====")

    for transaction in transactions:
        print(
            f"ID: {transaction[0]} | "
            f"Book ID: {transaction[1]} | "
            f"Member ID: {transaction[2]} | "
            f"Issue Date: {transaction[3]} | "
            f"Due Date: {transaction[4]} | "
            f"Return Date: {transaction[5]} | "
            f"Fine: {transaction[6]} | "
            f"Status: {transaction[7]}"
        )


def member_transaction_history():

    print("\n===== Member Transaction History =====")

    member_id = input("Enter Member ID: ")

    transactions = get_member_transactions(member_id)

    if not transactions:
        print("No transactions found for this member.")
        return

    for transaction in transactions:
        print(
            f"ID: {transaction[0]} | "
            f"Book ID: {transaction[1]} | "
            f"Member ID: {transaction[2]} | "
            f"Issue Date: {transaction[3]} | "
            f"Due Date: {transaction[4]} | "
            f"Return Date: {transaction[5]} | "
            f"Fine: {transaction[6]} | "
            f"Status: {transaction[7]}"
        )


def book_transaction_history():

    print("\n===== Book Transaction History =====")

    book_id = input("Enter Book ID: ")

    transactions = get_book_transactions(book_id)

    if not transactions:
        print("No transactions found for this book.")
        return

    for transaction in transactions:
        print(
            f"ID: {transaction[0]} | "
            f"Book ID: {transaction[1]} | "
            f"Member ID: {transaction[2]} | "
            f"Issue Date: {transaction[3]} | "
            f"Due Date: {transaction[4]} | "
            f"Return Date: {transaction[5]} | "
            f"Fine: {transaction[6]} | "
            f"Status: {transaction[7]}"
        )


def overdue_books_menu():

    print("\n===== Overdue Books =====")

    transactions = get_overdue_books()

    if not transactions:
        print("No overdue books found.")
        return

    for transaction in transactions:
        print(
            f"ID: {transaction[0]} | "
            f"Book ID: {transaction[1]} | "
            f"Member ID: {transaction[2]} | "
            f"Issue Date: {transaction[3]} | "
            f"Due Date: {transaction[4]} | "
            f"Return Date: {transaction[5]} | "
            f"Fine: {transaction[6]} | "
            f"Status: {transaction[7]}"
        )


def currently_issued_books_menu():

    print("\n===== Currently Issued Books =====")

    transactions = get_currently_issued()

    if not transactions:
        print("No books are currently issued.")
        return

    for transaction in transactions:
        print(
            f"ID: {transaction[0]} | "
            f"Book ID: {transaction[1]} | "
            f"Member ID: {transaction[2]} | "
            f"Issue Date: {transaction[3]} | "
            f"Due Date: {transaction[4]} | "
            f"Status: {transaction[7]}"
        )


def fine_reports_menu():

    print("\n===== Fine Reports =====")

    reports = get_fine_report()

    if not reports:
        print("No fine records found.")
        return

    for report in reports:
        print(
            f"Transaction ID: {report[0]} | "
            f"Book ID: {report[1]} | "
            f"Member ID: {report[2]} | "
            f"Fine: ₹{report[3]}"
        )

def transaction_menu():

    while True:

        print("\n===== Transaction Management =====")
        print("1. Issue Book")
        print("2. Return Book")
        print("3. View All Transactions")
        print("4. Member Transaction History")
        print("5. Book Transaction History")
        print("6. Overdue Books")
        print("7. Currently Issued Books")
        print("8. Fine Reports")
        print("9. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            issue_book_menu()

        elif choice == "2":
            return_book_menu()

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            member_transaction_history()

        elif choice == "5":
            book_transaction_history()

        elif choice == "6":
            overdue_books_menu()

        elif choice == "7":
            currently_issued_books_menu()

        elif choice == "8":
            fine_reports_menu()

        elif choice == "9":
            break

        else:
            print("Invalid choice. Please try again.")


def main_menu():

    print("\n===== Library Management System =====")
    print("1. Book Management")
    print("2. Member Management")
    print("3. Transaction Management")
    print("4. Exit")

def main():

    while True:
        main_menu()

        choice = input("Enter Your Choice : ")

        if choice == "1":
            book_menu()

        elif choice == "2":
            member_menu()

        elif choice == "3":
            transaction_menu()

        elif choice == "4":
            print("GoodBye!")
            break

        else:
            print("Invalid Choice.")

if __name__ == "__main__":
    main()