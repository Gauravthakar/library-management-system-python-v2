from database.database import create_tables, get_connection

create_tables()
print("Library Management System Started...")

# connection = get_connection()
# cursor = connection.cursor()

# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# tables = cursor.fetchall()

# print(tables)

# connection.close()