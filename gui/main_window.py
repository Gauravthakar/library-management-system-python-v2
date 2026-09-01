import tkinter as tk
from services.book_service import create_book

def open_add_book():

    add_window = tk.Toplevel()

    add_window.title("Add Book")
    add_window.geometry("500x600")

    title_lable = tk.Label(
        add_window,
        text="Add New Book",
        font=("Arial", 20, "bold")
    )

    title_lable.pack(pady=20)

    book_id_lable = tk.Label(add_window, text="Book ID")
    book_id_lable.pack()

    book_id_entry = tk.Entry(add_window)
    book_id_entry.pack(pady=5)

    title_label = tk.Label(add_window, text="Title")
    title_label.pack()

    title_entry = tk.Entry(add_window)
    title_entry.pack(pady=5)


    author_label = tk.Label(add_window, text="Author")
    author_label.pack()

    author_entry = tk.Entry(add_window)
    author_entry.pack(pady=5)


    category_label = tk.Label(add_window, text="Category")
    category_label.pack()

    category_entry = tk.Entry(add_window)
    category_entry.pack(pady=5)


    quantity_label = tk.Label(add_window, text="Quantity")
    quantity_label.pack()

    quantity_entry = tk.Entry(add_window)
    quantity_entry.pack(pady=5)

    def save_book():

        book_id = book_id_entry.get()
        title = title_entry.get()
        author = author_entry.get()
        category = category_entry.get()
        quantity = int(quantity_entry.get())

        result = create_book(
            book_id,
            title,
            author,
            category,
            quantity
        )

        if result:
            print("Book added successfully.")
            add_window.destroy()
        else:
            print("Failed to add book.")

    save_button = tk.Button(
        add_window,
        text="Add Book",
        width=25,
        height=2,
        command=save_book
    )

    save_button.pack(pady=20)

def open_book_management():

    book_window = tk.Toplevel()

    book_window.title("Book Management")
    book_window.geometry("700x500")

    title_lable = tk.Label(
        book_window,
        text="Book Management",
        font=("Arial", 20, "bold")
    )

    title_lable.pack(pady=30)

    add_button = tk.Button(
        book_window,
        text="Add Book",
        width=25,
        height=2,
        command=open_add_book
    )

    add_button.pack(pady=5)

    view_button = tk.Button(
        book_window,
        text="View Books",
        width=25,
        height=2
    )

    view_button.pack(pady=5)


    search_button = tk.Button(
        book_window,
        text="Search Book",
        width=25,
        height=2
    )

    search_button.pack(pady=5)


    update_button = tk.Button(
        book_window,
        text="Update Book",
        width=25,
        height=2
    )

    update_button.pack(pady=5)


    delete_button = tk.Button(
        book_window,
        text="Delete Book",
        width=25,
        height=2
    )

    delete_button.pack(pady=5)


    close_button = tk.Button(
        book_window,
        text="Close",
        width=25,
        height=2,
        command=book_window.destroy
    )

    close_button.pack(pady=5)

def start_application():

    root = tk.Tk()

    root.title("Library Management System")
    root.geometry("900x600")

    title_label = tk.Label(
        root,
        text="Library Management System",
        font=("Arial", 24, "bold")
    )

    title_label.pack(pady=40)

    book_button = tk.Button(
        root,
        text="Book Management",
        width=25,
        height=2,
        command=open_book_management
    )

    book_button.pack(pady=10)

    member_button = tk.Button(
        root,
        text="Member Management",
        width=25,
        height=2
    )

    member_button.pack(pady=10)

    transaction_button = tk.Button(
        root,
        text="Transaction Management",
        width=25,
        height=2
    )

    transaction_button.pack(pady=10)

    exit_button = tk.Button(
        root,
        text="Exit",
        width=25,
        height=2,
        command=root.destroy
    )

    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_application()