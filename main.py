from database.database import create_tables, get_connection
from modules.book_repository import add_book

success = add_book(
    "B001",
    "Python Programming",
    "Gaurav",
    "Programming",
    10
)

print(success)

# create_tables()
# print("Library Management System Started...")



