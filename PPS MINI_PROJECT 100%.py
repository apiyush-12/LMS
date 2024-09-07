import tkinter as tk  # to create gui
from tkinter import ttk  #to add image
from tkinter import messagebox 
from datetime import datetime
from tkcalendar import Calendar
import json
class AdminLogin:

    def __init__(self, root):
        self.root = root
        self.root.title("Admin Login")
        self.root.geometry("1920x1080")
        image_path = image_path = r'C:\Users\PIYUSH KUMAR\Downloads\mini_project\srmadminlogo.png' 
        self.photo = tk.PhotoImage(file=image_path).subsample(2)

        
        self.image_label = tk.Label(self.root, image=self.photo)
        self.image_label.pack(pady=10)

        self.title_label = tk.Label(self.root, text="Library Management System", font=("times new roman", 38, "bold italic"))
        self.title_label.pack(pady=10)

      
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(pady=10)

        self.username_label = tk.Label(entry_frame, text="Username:", font=("Arial", 12))
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = tk.Entry(entry_frame, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(entry_frame, text="Password:", font=("Arial", 12))
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = tk.Entry(entry_frame, show="*", font=("Arial", 12))
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.password_entry.bind("<Return>",lambda event: self.login_button.invoke())
        self.show_password_var = tk.BooleanVar()
        self.show_password_checkbox = tk.Checkbutton(self.root, text="Show Password", variable=self.show_password_var, command=self.toggle_password)
        self.show_password_checkbox.pack(pady=5)

        
        self.login_button = tk.Button(self.root, text="Login", command=self.check_login, font=("Arial", 12), bg="#1C86EE",fg="#ffffff")
        self.login_button.pack(pady=20)
        self.root.bind('<Return>',lambda event=None: self.admin_login())
        self.srm_label = tk.Label(self.root, text="~SRMIST", font=("Arial", 12, "italic"), fg="red")
        self.srm_label.pack()

    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry["show"] = ""
        else:
            self.password_entry["show"] = "*"


    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "pk6990" and password == "pksah":
            self.root.destroy() 
        elif username == "tr2472" and password == "tushar":
            self.root.destroy()  
        else:
            messagebox.showerror("Login Failed", "        Moye......moye.....moyeeemoye....re..!!!       ")

class Library:
    def __init__(self, books_data):   
        self.books_data = books_data
        self.available_books = {book_id: {'name': book_details['name'], 'quantity': 1} for book_id, book_details in books_data.items()}
        self.borrowed_books = {}


    def save_to_file(self, file_path):
        data = {
            "available_books": self.available_books,
            "borrowed_books": self.borrowed_books
        }
        with open(file_path, 'w') as file:
            json.dump(data, file)



    def load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.available_books = data["available_books"]
                self.borrowed_books = data["borrowed_books"]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error occurred: {e}")
            self.available_books = {}
            self.borrowed_books = {}


    def display_available_books(self):
        return [f"{book_id}: {book_details['name']}" for book_id, book_details in self.books_data.items()]
    

    def lend_book(self, requested_book_id, first_name, last_name, reg_number, batch, issue_date):
        requested_book_id = int(requested_book_id)
        if requested_book_id in self.available_books:
            book_name = self.available_books[requested_book_id]['name']

            if requested_book_id in self.borrowed_books:
                borrower_name = f"{self.borrowed_books[requested_book_id]['first_name']} {self.borrowed_books[requested_book_id]['last_name']}"
                messagebox.showerror("Book Already Borrowed", f"Sorry, the requested book is already borrowed by {borrower_name}.")
            else:
                self.borrowed_books[requested_book_id] = {
                    'name': book_name,
                    'first_name': first_name,
                    'last_name': last_name,
                    'reg_number': reg_number,
                    'batch': batch,
                    'issue_date': issue_date
                }
                del self.available_books[requested_book_id]

                messagebox.showinfo("Success", f"Book '{book_name}' with ID {requested_book_id} has been borrowed by {first_name} {last_name}.")
        else:
            messagebox.showerror("Book Unavailable", "Sorry, the requested book is not available in the library.")

    def validate_date_format(self, date_text):
        try:
            datetime.strptime(date_text, '%d/%m/%Y')
            return True
        except ValueError:
            return False
    def return_book(self, returned_book_id, return_date):
       returned_book_id = int(returned_book_id) 
       if returned_book_id in self.borrowed_books:
        book_name = self.borrowed_books[returned_book_id]['name']
        self.available_books[returned_book_id] = {'name': book_name}
        return_date = datetime.now().strftime('%d/%m/%Y')
        self.borrowed_books[returned_book_id]['return_date'] = return_date
        del self.borrowed_books[returned_book_id]
        messagebox.showinfo("Success", f"Book '{book_name}' with ID {returned_book_id} has been returned on {return_date}.")
       else:
        messagebox.showerror("Book Not Borrowed", "This book was not borrowed from the library. Please check the ID again.")
    def add_book(self, book_id, book_name):
        if book_id not in self.books_data:
            self.books_data[book_id] = {'name': book_name}
            self.available_books[book_id]={"name":book_name, 'quantity':1}
            messagebox.showinfo("Book Added", f"Book '{book_name}' with ID {book_id} has been added to the library.")
        else:
            messagebox.showinfo("Book Added", f"Book '{book_name}' with ID {book_id} is already in the library.")
    def delete_book(self, book_id):
        if book_id in self.books_data:
            book_name = self.books_data[book_id]['name']
            del self.books_data[book_id]
            if book_id in self.borrowed_books:
                del self.borrowed_books[book_id]
            messagebox.showinfo("Book Deleted", f"Book '{book_name}' with ID {book_id} has been deleted from the library.")
        else:
            messagebox.showinfo("Book Not Found", f"Book with ID {book_id} is not in the library.")
    def search_books(self, query):
        results = []
        for book_id, book_details in self.books_data.items():
            book_name = book_details['name'].lower()
            if query.lower() in book_name or query == str(book_id):
                results.append(f"{book_id}: {book_details['name']}")
        return results
    def display_borrowing_history(self, first_name, last_name):
        issued_books = []
        for book_id, details in self.borrowed_books.items():
            if details['first_name'] == first_name and details['last_name'] == last_name:
                issued_books.append(f"Book ID: {book_id}, Book Name: {details['name']}, Issue Date: {details['issue_date']}")
        if issued_books:
            return issued_books
        else:
            return [f"No borrowing history found for {first_name} {last_name}."]  
    def show_history(self, first_name, last_name, issue_date):
        issued_books = []
        if self.validate_date_format(issue_date):
            for book_id, details in self.borrowed_books.items():
                if details['first_name'] == first_name and details['last_name'] == last_name and details['issue_date'] == issue_date:
                    issued_books.append(details['name'])
            if issued_books:
                issued_books_str = "\n".join(issued_books)
                messagebox.showinfo("Issued Books", f"Books issued by {first_name} {last_name} on {issue_date}:\n{issued_books_str}")
            else:
                messagebox.showinfo("No History", f"No books were issued by {first_name} {last_name} on {issue_date}.")
        else:
            messagebox.showerror("Invalid Date Format", "Please use the format DD/MM/YYYY for the issue date.")
    def display_last_3_histories(self):
        histories = []
        count = 1
        for book_id, details in reversed(self.borrowed_books.items()):
            if count > 3:
                break
            issue_date = details['issue_date']
            return_date = details.get('return_date', 'Not Returned')
            history = (count, f"{details['first_name']} {details['last_name']}", book_id, details['name'], issue_date, return_date)
            histories.append(history)
            count += 1
        return histories
class LibraryGUI:
    def __init__(self, root, library):
        self.root = root
        self.library = library
        self.title_frame = None
        self.initialize_ui()
        self.set_theme_light_green()
    def set_theme_light_green(self):
        style = ttk.Style()
        style.theme_use('clam')  
        style.configure('.', background='#C3E6CB')
    def validate_integer_input(self, input_data):
        try:
            return int(input_data)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer.")
            return None
    def initialize_ui(self):
        self.root.geometry("1920x1080")

        path_to_image1 = r'C:\Users\PIYUSH KUMAR\Downloads\mini_project\srm-logo.png'
        path_to_image2 = r'C:\Users\PIYUSH KUMAR\Downloads\mini_project\srm-logo.png'


        image1 = tk.PhotoImage(file=path_to_image1).subsample(3)
        image2 = tk.PhotoImage(file=path_to_image2).subsample(3)

        
        label1 = tk.Label(self.root, image=image1, bg='#E6E6FA')
        label1.image = image1
        label1.place(x=0, y=0, anchor='nw')

        # Title label


        label2 = tk.Label(self.root, image=image2, bg='#E6E6FA')
        label2.image = image2
        label2.place(x=self.root.winfo_screenwidth(), y=0, anchor='ne')

        self.root.title("        Library Management System         ")
        self.root.configure(bg='#E6E6FA')
        self.root.option_add('*TCombobox*Listbox*Background', 'white')
        self.title_frame = tk.Frame(self.root, bd=2, relief=tk.SOLID, padx=20, pady=20)
        self.title_frame.pack()
        title_label = tk.Label(self.title_frame, text="             Welcome To The Library             ", font=("times new roman", 38, "bold italic"),
                               bg='#FF6103', fg='#F0F8FF')
        title_label.pack(side=tk.LEFT, padx=5)
        self.project_label = tk.Label(self.root, text="                        Project by ~Piyush kumar,RA2311029010030 & Tushar Raj,RA2311029010015                         ",
                                      font=("Arial", 14), bg='#000000', fg='#f0f0f0')
        self.project_label.pack()
        self.main_frame = tk.Frame(self.root, bg='#E6E6FA')
        self.main_frame.pack(pady=20)
        self.borrow_frame = tk.LabelFrame(self.main_frame, text="Borrow and Return Books", font=("Arial", 20, "bold"),
                                         bg='#F0FFFF',highlightthickness=1, highlightbackground="black")
        self.borrow_frame.grid(row=0, column=0, padx=20, pady=10, sticky='nsew')
        self.add_delete_frame = tk.LabelFrame(self.main_frame, text="Add and Delete Books", font=("Arial", 20, "bold"),
                                             bg='#F0FFFF')
        self.add_delete_frame.grid(row=0, column=1, padx=20, pady=10, sticky='nsew')
        self.available_books_frame = tk.LabelFrame(self.main_frame, text="Available Books", font=("Arial", 20, "bold"),
                                                  bg='#F0FFFF', highlightthickness=1 ,highlightbackground="black")
        self.available_books_frame.grid(row=0, column=2, padx=20, pady=10, sticky='nsew',rowspan=2)
        self.clock_frame = tk.Frame(self.root, bg='#E6E6FA')
        self.clock_frame.pack(side="top" ,anchor="ne")
        self.clock_label = tk.Label(self.clock_frame, font=("Arial", 16), bg='#E6E6FA')
        self.clock_label.pack()
        self.update_clock()
        self.create_borrow_widgets()
        self.create_return_widgets()
        self.create_add_delete_widgets()
        self.create_available_books_widget()
        show_history_button = tk.Button(self.main_frame, text="Show History", command=self.show_last_3_histories,
                                       bg='#436EEE', fg='white', font=("Arial", 12))
        show_history_button.grid(row=1, column=2, padx=20, pady=10)
    def update_clock(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%d/%m/%Y")
        self.clock_label.config(text=f"Date: {current_date} \nTime: {current_time}")
        self.root.after(1000, self.update_clock)
    def create_return_widgets(self):
             return_frame = tk.LabelFrame(self.main_frame, text="Return Book", font=("Arial", 22, "bold"), bg='#E0FFFF')
             return_frame.grid(row=1, column=0, padx=20, pady=10, sticky='nsew')

             return_label = tk.Label(return_frame, text="Enter Book ID:", font=("Arial", 12), bg='#ffffff')
             return_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

             self.return_entry = tk.Entry(return_frame, width=30)
             self.return_entry.grid(row=0, column=1, padx=5, pady=5)

             return_button = tk.Button(return_frame, text="Return Book", command=self.return_book,
                              bg='#f44336', fg='white', font=("Arial", 12))
             return_button.grid(row=1, column=0, columnspan=2, pady=10)
    def return_book(self):
            book_id = self.return_entry.get()
            return_date = datetime.now().strftime('%d/%m/%Y') 
            self.library.return_book(book_id,return_date)
            self.create_add_delete_widgets()
            self.update_available_books()
    def return_book_gui(self, book_id):
            if not book_id.isdigit():
                 messagebox.showerror("Invalid Input", "Book ID must be a number.")
                 return
            return_date = datetime.now().strftime('%d/%m/%Y') 
            book_id = int(book_id)
            self.library.return_book(book_id,return_date)
            self.update_available_books()
    def create_borrow_widgets(self):
        labels = ["1. Book ID:", "2. Book Name:", "3. First Name:", "4. Last Name:", "5. Registration Number:", "6. Program:"]
        entries = []

        def on_enter(event):
            current_entry = self.root.focus_get()
            current_index = entries.index(current_entry)
            if current_index < len(entries) - 1:
                entries[current_index + 1].focus()

        for i in range(len(labels)):
            label = tk.Label(self.borrow_frame, text=labels[i], font=("Arial", 12), bg='#f0f0f0')
            label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            entry = tk.Entry(self.borrow_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.bind("<Return>", on_enter)  
            entries.append(entry)

        issue_date_label = tk.Label(self.borrow_frame, text="7. Issue Date:", font=("Arial", 12), bg='#f0f0f0')
        issue_date_label.grid(row=len(labels), column=0, padx=5, pady=5, sticky=tk.W)
        self.issue_date_entry = tk.Entry(self.borrow_frame, width=30)
        self.issue_date_entry.grid(row=len(labels), column=1, padx=5, pady=5)
        self.issue_date_entry.bind("<Return>", on_enter) 

        pick_date_button = tk.Button(self.borrow_frame, text="Pick Date", command=self.popup_calendar, bg='#FFA500', fg='white', font=("Arial", 12))
        pick_date_button.grid(row=len(labels), column=2, padx=5, pady=5)

        borrow_button = tk.Button(self.borrow_frame, text="Borrow Book", command=lambda: self.borrow_book(entries),
                                 bg='#4caf50', fg='white', font=("Arial", 12))
        borrow_button.grid(row=len(labels) + 1, column=0, columnspan=3, pady=20)
    def popup_calendar(self):
        def get_date():
            self.issue_date_entry.delete(0, 'end')
            self.issue_date_entry.insert(0, cal.get_date())
            top.destroy()
        top = tk.Toplevel(self.root)
        cal = Calendar(top, selectmode="day", date_pattern="dd/MM/yyyy")
        cal.pack(padx=20, pady=20)
        button = tk.Button(top, text="Select", command=get_date)
        button.pack(pady=10)
    def pick_issue_date(self):
        def set_date():
            self.issue_date_entry.delete(0, 'end')
            self.issue_date_entry.insert(0, cal.get_date())
            top.destroy()
        top = tk.Toplevel(self.root)
        top.geometry("250x250")
        cal = Calendar(top, selectmode="day", date_pattern="dd/MM/yyyy")
        cal.pack(padx=20, pady=20)
        set_date_button = tk.Button(top, text="Set Date", command=set_date, bg='#4caf50', fg='white', font=("Arial", 12))
        set_date_button.pack(pady=10)
    def borrow_book(self, entries):
        book_id, book_name, first_name, last_name, reg_number, batch = [e.get() for e in entries]
        issue_date = self.issue_date_entry.get()
        if not book_id.isdigit():
            messagebox.showerror("Invalid Input", "Book ID must be a number.")
            return
        book_id = int(book_id)
        self.library.lend_book(book_id, first_name, last_name, reg_number, batch, issue_date)
        self.update_available_books()
    def create_add_delete_widgets(self):
        labels = ["Book ID:", "Book Name:", "New Book Name:", "New Book ID:"]
        entries = []
        add_delete_frame = tk.LabelFrame(self.main_frame, text="Add and Delete Books", font=("Arial", 20, "bold"),
                                             bg='#F0FFFF')
        add_delete_frame.grid(row=0, column=1, padx=20, pady=10, sticky='nsew')
        for i in range(len(labels)):
            label = tk.Label(add_delete_frame, text=labels[i], font=("Arial", 12), bg='#ffffff')
            label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            entry = tk.Entry(add_delete_frame, width=20)  
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry)
        add_button = tk.Button(add_delete_frame, text="Add Book", command=lambda: self.add_book_gui(entries),
                               bg='#2196f3', fg='white', font=("Arial", 12))
        add_button.grid(row=len(labels), column=0, columnspan=2, pady=10)
        update_button = tk.Button(add_delete_frame, text="Update Book", command=lambda: self.update_book_gui(entries),
                                  bg='#FFA500', fg='white', font=("Arial", 12))
        update_button.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)
        delete_button = tk.Button(add_delete_frame, text="Delete Book", command=lambda: self.delete_book_gui(entries),
                                  bg='#f44336', fg='white', font=("Arial", 12))
        delete_button.grid(row=len(labels) + 2, column=0, columnspan=2, pady=10)
    def update_book_gui(self, entries):
        book_id, book_name, new_book_name, new_book_id = [e.get() for e in entries]
        if not book_id.isdigit() or not new_book_id.isdigit():
            messagebox.showerror("Invalid Input", "Book ID and New Book ID must be a number.")
            return
        book_id = int(book_id)
        new_book_id = int(new_book_id)
        self.library.delete_book(book_id)
        self.library.add_book(new_book_id, new_book_name)
        self.update_available_books()
    def delete_book_gui(self, entries):
        book_id = entries[0].get()
        if not book_id.isdigit():
            messagebox.showerror("Invalid Input", "Book ID must be a number.")
            return
        book_id = int(book_id)
        confirmation = messagebox.askquestion("Confirmation", f"Are you sure you want to delete the book with ID {book_id}?")
        if confirmation == 'yes':
            self.library.delete_book(book_id)
            self.update_available_books()
    def add_book_gui(self, entries):
        book_id, book_name = [e.get() for e in entries[:2]]
        if not book_id.isdigit():
            messagebox.showerror("Invalid Input", "Book ID must be a number.")
            return
        book_id = int(book_id)
        self.library.add_book(book_id, book_name)
        self.update_available_books()
    def create_available_books_widget(self):
        self.available_books_tree = ttk.Treeview(self.available_books_frame, columns=('Book ID', 'Book Name', 'Quantity'), show='headings')
        self.available_books_tree.heading('Book ID', text='Book ID')
        self.available_books_tree.heading('Book Name', text='Book Name')
        self.available_books_tree.column('Book ID', width=100, anchor='center')
        self.available_books_tree.column('Book Name', width=200, anchor='center')
        self.available_books_tree.pack(padx=10, pady=10)

        search_frame = tk.Frame(self.available_books_frame, bg='#C3E6CB') 
        search_frame.pack(pady=10)

        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5) 

        search_button = tk.Button(search_frame, text="Search", command=self.search_book, bg='#FFA500', fg='white', font=("Arial", 10))
        search_button.pack(side=tk.LEFT, padx=5)  

        self.update_available_books()
    def search_book(self):
        query = self.search_entry.get()
        results = self.library.search_books(query)
        self.update_available_books(results)
    def show_borrowing_history(self, entries):
        first_name, last_name = [e.get() for e in entries]
        history = self.library.display_borrowing_history(first_name, last_name)
        messagebox.showinfo("Borrowing History", "\n".join(history))
    def update_available_books(self, books=None):
        self.clear_treeview()
        if not books:
            books = self.library.display_available_books()
        for book in books:
            book_info = book.split(':')
            if len(book_info) >= 2:
                book_id, book_name = book_info[0], ':'.join(book_info[1:])
                if int(book_id) not in self.library.borrowed_books:  # Check if the book is not borrowed
                    self.available_books_tree.insert("", "end", values=(book_id, book_name))
    def clear_treeview(self):
        for record in self.available_books_tree.get_children():
            self.available_books_tree.delete(record)
    def show_last_3_histories(self):
        histories = self.library.display_last_3_histories()
        history_window = tk.Tk()
        history_window.title("Last 3 Borrowing Histories")
        tree = ttk.Treeview(history_window, columns=(1, 2, 3, 4, 5, 6), show="headings")
        tree.pack()
        tree.heading(1, text="S.NO")
        tree.heading(2, text="NAME")
        tree.heading(3, text="BOOK ID")
        tree.heading(4, text="BOOK NAME")
        tree.heading(5, text="ISSUE DATE")
        tree.heading(6, text="RETURN DATE")
        for history in histories:
            tree.insert("", "end", values=history, tag='centered')
        for col in range(1, 7):
            tree.column(col, anchor='center')
if __name__ == '__main__':
    root = tk.Tk()
    admin_login = AdminLogin(root)
    root.mainloop()
    if admin_login:      
        book_dict = {
            101: {'name': 'BOOK1'},
            102: {'name': 'BOOK2'},
            103: {'name': 'BOOK3'},
            104: {'name': 'BOOK4'},
            105: {'name': 'BOOK5'},
        }
        my_library = Library(book_dict)
        library_gui = LibraryGUI(tk.Tk(), my_library)
        library_gui.root.mainloop()