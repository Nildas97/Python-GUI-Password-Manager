from tkinter import Tk, ttk, Label, Button, Entry, Frame, END, Toplevel
from db_ops import DBOperations

class root_window:
    def __init__(self, root, db):
        self.db = db
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("870x700+40+40")

        head_title = Label(self.root, text="Password Manager", width=80, fg="white", bg="blueviolet", font=("Roboto", 20), padx=20, pady=20)
        head_title.grid(columnspan=10, padx=200, pady=20) 

        self.crud_frame = Frame(self.root,highlightbackground="black", highlightthickness=2, padx=10, pady=30)
        self.crud_frame.grid()
        self.create_entry_labels()
        self.create_entry_boxes()
        self.create_crud_buttons()
        # self.search_entry = Entry(self.crud_frame, width=30, font=('Ariel', 12))
        # self.search_entry.grid(row=self.row_no, column=self.col_no)
        # self.col_no+=1
        # Button(self.crud_frame, text="Search", bg="greenyellow", font=("Ariel", 12), width=20).grid(
        #     row=self.row_no, column=self.col_no, padx=5, pady=5)
        self.create_records_tree()


    def create_entry_labels(self):
        self.col_no, self.row_no = 0, 0
        labels_info = ('ID', 'Website', 'Username', 'Password')
        for label_info in labels_info:
            Label(self.crud_frame, text=label_info, bg="gray20", fg="white", 
            font=("Ariel", 12), padx=5, pady=2).grid(row=self.row_no, column=self.col_no, padx=5, pady=2)
            self.col_no+=1
    
    def create_crud_buttons(self):
        self.row_no+=1
        self.col_no = 0
        buttons_info = (("Save", "mediumspringgreen", self.save_record), ("Update", "mediumslateblue", self.update_record), ("Delete", "lightcoral", self.delete_record), ("Copy Password", "goldenrod1", self.copy_password), ('Show All Records', 'deeppink1', self.show_record))
        for button_info in buttons_info:
            if button_info[0]=='Show All Records':
                self.row_no+=1
                self.col_no=1

            Button(self.crud_frame, text=button_info[0], bg=button_info[1], fg="white", 
            font=("Ariel", 12), padx=5, pady=2, width=30, command=button_info[2]).grid(row=self.row_no, column=self.col_no, padx=5, pady=10)
            self.col_no+=1
    
    def create_entry_boxes(self):
        self.row_no+=1
        self.entry_boxes = []
        self.col_no = 0
        for i in range(4):
            show= ""
            if i == 3:
                show = "*"
            entry_box = Entry(self.crud_frame, width=30, background="lightskyblue", font=("Ariel", 30), show=show)
            entry_box.grid(row=self.row_no, column=self.col_no, padx=10, pady=10)
            self.col_no+=1
            self.entry_boxes.append(entry_box)
    
    # CRUD functions

    # create record
    def save_record(self):
        website = self.entry_boxes[1].get().strip()
        username = self.entry_boxes[2].get().strip()
        password = self.entry_boxes[3].get().strip()

        # Validation check
        if not website or not username or not password:
            self.showmessage("Error", "All fields are required.")
            return

        data = {'website': website, 'username': username, 'password': password}
        self.db.create_record(data)
        self.show_record()  

    # update record
    def update_record(self):
        ID = self.entry_boxes[0].get().strip()
        website = self.entry_boxes[1].get().strip()
        username = self.entry_boxes[2].get().strip()
        password = self.entry_boxes[3].get().strip()

        # Validation check
        if not ID or not website or not username or not password:
            self.showmessage("Error", "All fields are required.")
            return

        data = {'ID': ID, 'website': website, 'username': username, 'password': password}
        self.db.update_record(data)
        self.show_record()

    # delete record
    def delete_record(self):
        ID = self.entry_boxes[0].get()
        self.db.delete_record(ID)
        self.show_record()

    # read record
    def show_record(self):
        # Clear existing records in the tree
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        # Fetch records from the database
        record_list = self.db.show_record()
        
        # Insert only website and username into the treeview
        for record in record_list:
            self.records_tree.insert('', END, values=(record[0], record[3], record[4]))

    def create_records_tree(self):
        columns = ('ID', 'website', 'username', 'password')
        self.records_tree = ttk.Treeview(self.root, columns=columns, show='headings')
        
        # Set the headings for each column
        self.records_tree.heading('ID', text="ID")
        self.records_tree.heading('website', text="Website")
        self.records_tree.heading('username', text="Username")
        self.records_tree.heading('password', text="Password")

        # Only show ID, website, and username in the table
        self.records_tree['displaycolumns'] = ('ID', 'website', 'username')

        def item_selected(event):
            for selected_item in self.records_tree.selection():
                item = self.records_tree.item(selected_item)
                record = item['values']
                
                # Only update the entry boxes for ID, website, username, and password
                for entry_box, item_value in zip(self.entry_boxes, record):
                    entry_box.delete(0, END)
                    entry_box.insert(0, item_value)

        self.records_tree.bind('<<TreeviewSelect>>', item_selected)

        # Place the Treeview on the grid
        self.records_tree.grid()


    def copy_password(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.entry_boxes[3].get())
        message = "Password Copied"
        title = "Copy"
        if self.entry_boxes[3].get()=="":
            message = "Box is empty"
            title = "Error"
        self.showmessage(title, message)

    def showmessage(self, title_box:str=None, message:str=None):
        TIME_TO_WAIT = 900 # in miliseconds
        root = Toplevel(self.root)
        background = "green"
        if title_box == "Error":
            background = "red"
        root.geometry('200x30+600+200')
        root.title(title_box)
        Label(root, text=message, background=background, font=("Ariel", 15), fg="white").pack(padx=4, pady=2)

        try:
            root.after(TIME_TO_WAIT, root.destroy)
        except Exception as e:
            print("Error occured", e)
            










if __name__ == "__main__":
    db_class = DBOperations()
    db_class.create_table()
    
    root = Tk()
    root_class = root_window(root, db_class)
    root.resizable(True, True)
    root.mainloop()