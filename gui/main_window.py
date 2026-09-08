import tkinter as tk
from tkinter import ttk
from services.book_service import(
    create_book, 
    get_books, 
    get_book, 
    update_book, 
    delete_book
)
from services.member_service import(
    create_member,
    get_members,
    get_member
)

# ========= Books Section ==========
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

def open_view_books():

    view_window = tk.Toplevel()

    view_window.title("View Books")
    view_window.geometry("800x500")

    title_lable = tk.Label(
        view_window,
        text="All Books",
        font=("Arial", 20, "bold")
    )

    title_lable.pack(pady=20)

    books = get_books()

    tree = ttk.Treeview(
        view_window,
        columns=("id", "title", "author", "category", "quantity", "available"),
        show="headings"
    )

    tree.heading("id", text="Book ID")
    tree.heading("title", text="Title")
    tree.heading("author", text="Author")
    tree.heading("category", text="Category")
    tree.heading("quantity", text="Quantity")
    tree.heading("available", text="Available")

    tree.column("id", width=100)
    tree.column("title", width=180)
    tree.column("author", width=180)
    tree.column("category", width=150)
    tree.column("quantity", width=100)
    tree.column("available", width=100)

    for book in books:
        tree.insert(
            "",
            tk.END,
            values=(
                book[0],
                book[1],
                book[2],
                book[3],
                book[4],
                book[5],
            )
        )

    tree.pack(fill="both", expand=True, padx=20, pady=10)

def open_search_book():

    search_window = tk.Toplevel()

    search_window.title("Search Book")
    search_window.geometry("600x500")

    title_label = tk.Label(
        search_window,
        text="Search Book",
        font=("Arial", 20, "bold")
    )

    title_label.pack(pady=20)

    book_id_label = tk.Label(
        search_window,
        text="Book ID"
    )

    book_id_label.pack(pady=5)

    book_id_entry = tk.Entry(
        search_window,
        width=30
    )

    book_id_entry.pack(pady=5)

    def search_book():

        book_id = book_id_entry.get()

        book = get_book(book_id)

        if book:

            book_id_value.config(text=book[0])
            title_value.config(text=book[1])
            author_value.config(text=book[2])
            category_value.config(text=book[3])
            quantity_value.config(text=book[4])
            available_value.config(text=book[5])

        else:

            book_id_value.config(text="Book not found")
            title_value.config(text="")
            author_value.config(text="")
            category_value.config(text="")
            quantity_value.config(text="")
            available_value.config(text="")

    details_frame = tk.LabelFrame(
        search_window,
        text="Book Details",
        font=("Arial", 12, "bold"),
        padx=20,
        pady=15
    )

    details_frame.pack(
        padx=30,
        pady=20,
        fill="x"
    )

    tk.Label(details_frame, text="Book ID").grid(row=0, column=0, sticky="w", pady=5)
    tk.Label(details_frame, text="Title").grid(row=1, column=0, sticky="w", pady=5)
    tk.Label(details_frame, text="Author").grid(row=2, column=0, sticky="w", pady=5)
    tk.Label(details_frame, text="Category").grid(row=3, column=0, sticky="w", pady=5)
    tk.Label(details_frame, text="Quantity").grid(row=4, column=0, sticky="w", pady=5)
    tk.Label(details_frame, text="Available").grid(row=5, column=0, sticky="w", pady=5)

    book_id_value = tk.Label(details_frame, text="")
    book_id_value.grid(row=0, column=1, sticky="w", pady=5)

    title_value = tk.Label(details_frame, text="")
    title_value.grid(row=1, column=1, sticky="w", pady=5)

    author_value = tk.Label(details_frame, text="")
    author_value.grid(row=2, column=1, sticky="w", pady=5)

    category_value = tk.Label(details_frame, text="")
    category_value.grid(row=3, column=1, sticky="w", pady=5)

    quantity_value = tk.Label(details_frame, text="")
    quantity_value.grid(row=4, column=1, sticky="w", pady=5)

    available_value = tk.Label(details_frame, text="")
    available_value.grid(row=5, column=1, sticky="w", pady=5)

    search_button = tk.Button(
        search_window,
        text="Search Book",
        width=20,
        height=2,
        command=search_book
    )

    search_button.pack(pady=20)

def open_update_book():

    update_window = tk.Toplevel()

    update_window.title("Update Book")
    update_window.geometry("500x600")

    # Book ID
    book_id_label = tk.Label(
        update_window,
        text="Book ID"
    )
    book_id_label.pack(pady=5)

    book_id_entry = tk.Entry(
        update_window,
        width=30
    )
    book_id_entry.pack(pady=5)

    # Title
    book_title_label = tk.Label(
        update_window,
        text="Title"
    )
    book_title_label.pack(pady=5)

    book_title_entry = tk.Entry(
        update_window,
        width=30
    )
    book_title_entry.pack(pady=5)

    # Author
    author_label = tk.Label(
        update_window,
        text="Author"
    )
    author_label.pack(pady=5)

    author_entry = tk.Entry(
        update_window,
        width=30
    )
    author_entry.pack(pady=5)

    # Category
    category_label = tk.Label(
        update_window,
        text="Category"
    )
    category_label.pack(pady=5)

    category_entry = tk.Entry(
        update_window,
        width=30
    )
    category_entry.pack(pady=5)

    # Quantity
    quantity_label = tk.Label(
        update_window,
        text="Quantity"
    )
    quantity_label.pack(pady=5)

    quantity_entry = tk.Entry(
        update_window,
        width=30
    )
    quantity_entry.pack(pady=5)

    # Search function
    def search_book():

        book_id = book_id_entry.get()

        book = get_book(book_id)

        if book:

            book_title_entry.delete(0, tk.END)
            book_title_entry.insert(0, book[1])

            author_entry.delete(0, tk.END)
            author_entry.insert(0, book[2])

            category_entry.delete(0, tk.END)
            category_entry.insert(0, book[3])

            quantity_entry.delete(0, tk.END)
            quantity_entry.insert(0, book[4])

        else:

            print("Book not found.")

    # Search button
    search_button = tk.Button(
        update_window,
        text="Search Book",
        width=20,
        command=search_book
    )

    search_button.pack(pady=10)

    # Save Updates
    def save_updated_book():

        book_id = book_id_entry.get()
        title = book_title_entry.get()
        author = author_entry.get()
        category = category_entry.get()
        quantity = int(quantity_entry.get())

        result = update_book(
            book_id,
            title,
            author,
            category,
            quantity
        )

        if result:

            print("Book updated successfully.")

            update_window.destroy()

        else:

            print("Failed to update book.")

    # Update button
    update_button = tk.Button(
        update_window,
        text="Update Book",
        width=25,
        height=2,
        command=save_updated_book
    )

    update_button.pack(pady=25)

def open_delete_book():

    delete_window = tk.Toplevel()

    delete_window.title("Delete Book")
    delete_window.geometry("500x400")

    title_label = tk.Label(
        delete_window,
        text="Delete Book",
        font=("Arial", 20, "bold")
    )

    title_label.pack(pady=30)

    book_id_label = tk.Label(
        delete_window,
        text="Book ID"
    )

    book_id_label.pack(pady=10)

    book_id_entry = tk.Entry(
        delete_window,
        width=30
    )

    book_id_entry.pack(pady=10)

    def delete_selected_book():

        book_id = book_id_entry.get()

        result = delete_book(book_id)

        if result:

            print("Book deleted successfully.")

            delete_window.destroy()

        else:

            print("Failed to delete book.")

    delete_button = tk.Button(
        delete_window,
        text="Delete Book",
        width=25,
        height=2,
        command=delete_selected_book
    )

    delete_button.pack(pady=30)


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
        height=2,
        command=open_view_books
    )

    view_button.pack(pady=5)


    search_button = tk.Button(
        book_window,
        text="Search Book",
        width=25,
        height=2,
        command=open_search_book
    )

    search_button.pack(pady=5)


    update_button = tk.Button(
        book_window,
        text="Update Book",
        width=25,
        height=2,
        command=open_update_book
    )

    update_button.pack(pady=5)


    delete_button = tk.Button(
        book_window,
        text="Delete Book",
        width=25,
        height=2,
        command=open_delete_book
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


# =========== Members Section ===========

# Add Member
def open_add_member():

    add_window = tk.Toplevel()

    add_window.title("Add Member")
    add_window.geometry("500x650")

    title_label = tk.Label(
        add_window,
        text="Add New Member",
        font=("Arial", 20, "bold")
    )

    title_label.pack(pady=20)

    member_id_label = tk.Label(
        add_window,
        text="Member ID"
    )
    member_id_label.pack(pady=5)

    member_id_entry = tk.Entry(
        add_window,
        width=30
    )
    member_id_entry.pack(pady=5)

    name_label = tk.Label(
        add_window,
        text="Name"
    )
    name_label.pack(pady=5)

    name_entry = tk.Entry(
        add_window,
        width=30
    )
    name_entry.pack(pady=5)

    phone_label = tk.Label(
        add_window,
        text="Phone"
    )
    phone_label.pack(pady=5)

    phone_entry = tk.Entry(
        add_window,
        width=30
    )
    phone_entry.pack(pady=5)

    email_label = tk.Label(
        add_window,
        text="Email"
    )
    email_label.pack(pady=5)

    email_entry = tk.Entry(
        add_window,
        width=30
    )
    email_entry.pack(pady=5)

    address_label = tk.Label(
        add_window,
        text="Address"
    )
    address_label.pack(pady=5)

    address_entry = tk.Entry(
        add_window,
        width=30
    )
    address_entry.pack(pady=5)

    # Save Member
    def save_member():

        member_id = member_id_entry.get()
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()

        result = create_member(
            member_id,
            name,
            phone,
            email,
            address
        )

        if result:

            print("Member added successfully.")

            add_window.destroy()

        else:

            print("Failed to add member.")

    save_button = tk.Button(
        add_window,
        text="Add Member",
        width=25,
        height=2,
        command=save_member
    )

    save_button.pack(pady=25)

# View Members
def open_view_members():

    view_window = tk.Toplevel()

    view_window.title("View Members")
    view_window.geometry("1000x500")

    title_label = tk.Label(
        view_window,
        text="All Members",
        font=("Arial", 20, "bold")
    )

    title_label.pack(pady=20)

    members = get_members()

    tree = ttk.Treeview(
        view_window,
        columns=("id", "name", "phone", "email", "address", "join_date"),
        show="headings"
    )

    tree.heading("id", text="Member ID")
    tree.heading("name", text="Name")
    tree.heading("phone", text="Phone")
    tree.heading("email", text="Email")
    tree.heading("address", text="Address")
    tree.heading("join_date", text="Join Date")

    tree.column("id", width=100)
    tree.column("name", width=150)
    tree.column("phone", width=120)
    tree.column("email", width=200)
    tree.column("address", width=200)
    tree.column("join_date", width=120)

    for member in members:

        tree.insert(
            "",
            tk.END,
            values=(
                member[0],
                member[1],
                member[2],
                member[3],
                member[4],
                member[5]
            )
        )

    tree.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

# Search Member
def open_search_member():

    search_window = tk.Toplevel()

    search_window.title("Search Member")
    search_window.geometry("600x500")

    title_label = tk.Label(
        search_window,
        text="Search Member",
        font=("Arial", 20, "bold")
    )

    title_label.pack(pady=20)

    member_id_label = tk.Label(
        search_window,
        text="Member ID"
    )

    member_id_label.pack(pady=5)

    member_id_entry = tk.Entry(
        search_window,
        width=30
    )

    member_id_entry.pack(pady=5)

    def search_member():

        member_id = member_id_entry.get()

        member = get_member(member_id)

        if member:

            member_id_value.config(text=member[0])
            name_value.config(text=member[1])
            phone_value.config(text=member[2])
            email_value.config(text=member[3])
            address_value.config(text=member[4])
            join_date_value.config(text=member[5])

        else:

            member_id_value.config(text="Member not found")
            name_value.config(text="")
            phone_value.config(text="")
            email_value.config(text="")
            address_value.config(text="")
            join_date_value.config(text="")

    details_frame = tk.LabelFrame(
        search_window,
        text="Member Details",
        font=("Arial", 12, "bold"),
        padx=20,
        pady=15
    )

    details_frame.pack(
        padx=30,
        pady=20,
        fill="x"
    )

    tk.Label(details_frame, text="Member ID").grid(row=0, column=0, sticky="w", pady=5)
    tk.Label(details_frame, text="Name").grid(row=1, column=0, sticky="w", pady=5)
    tk.Label(details_frame, text="Phone").grid(row=2, column=0, sticky="w", pady=5)
    tk.Label(details_frame, text="Email").grid(row=3, column=0, sticky="w", pady=5)
    tk.Label(details_frame, text="Address").grid(row=4, column=0, sticky="w", pady=5)
    tk.Label(details_frame, text="Join Date").grid(row=5, column=0, sticky="w", pady=5)


    member_id_value = tk.Label(details_frame, text="")
    member_id_value.grid(row=0, column=1, sticky="w", pady=5)

    name_value = tk.Label(details_frame, text="")
    name_value.grid(row=1, column=1, sticky="w", pady=5)

    phone_value = tk.Label(details_frame, text="")
    phone_value.grid(row=2, column=1, sticky="w", pady=5)

    email_value = tk.Label(details_frame, text="")
    email_value.grid(row=3, column=1, sticky="w", pady=5)

    address_value = tk.Label(details_frame, text="")
    address_value.grid(row=4, column=1, sticky="w", pady=5)

    join_date_value = tk.Label(details_frame, text="")
    join_date_value.grid(row=5, column=1, sticky="w", pady=5)

    search_button = tk.Button(
        search_window,
        text="Search Member",
        width=20,
        command=search_member
    )

    search_button.pack(pady=20)

def open_member_management():

    member_window = tk.Toplevel()

    member_window.title("Member Management")
    member_window.geometry("700x500")

    title_label = tk.Label(
        member_window,
        text="Member Management",
        font=("Arial", 20, "bold")
    )

    title_label.pack(pady=30)

    add_button = tk.Button(
        member_window,
        text="Add Member",
        width=25,
        height=2,
        command=open_add_member
    )

    add_button.pack(pady=10)

    view_button = tk.Button(
        member_window,
        text="View Members",
        width=25,
        height=2,
        command=open_view_members
    )

    view_button.pack(pady=10)

    search_button = tk.Button(
        member_window,
        text="Search Member",
        width=25,
        height=2,
        command=open_search_member
    )

    search_button.pack(pady=10)

    update_button = tk.Button(
        member_window,
        text="Update Member",
        width=25,
        height=2
    )

    update_button.pack(pady=10)

    delete_button = tk.Button(
        member_window,
        text="Delete Member",
        width=25,
        height=2
    )

    delete_button.pack(pady=10)

    close_button = tk.Button(
        member_window,
        text="Close",
        width=25,
        height=2,
        command=member_window.destroy
    )

    close_button.pack(pady=10)

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
        height=2,
        command=open_member_management
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