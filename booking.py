from tkinter import *
import tkinter.messagebox
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Booking Management")
        self.master.configure(bg='#f0f0f0')  # Set background color

        # Frames for better layout
        self.top_frame = Frame(master, bg='#4682B4', height=100)
        self.top_frame.pack(fill=BOTH)
        self.bottom_frame = Frame(master, bg='#ffffff', height=500)
        self.bottom_frame.pack(fill=BOTH, expand=True)

        # Heading label in the top frame
        self.heading = Label(self.top_frame, text="Booking Management System", bg='#4682B4', fg='white', 
                             font=('Arial', 30, 'bold'))
        self.heading.pack(pady=20)

        # Search Section
        self.search_label = Label(self.bottom_frame, text="Enter Customer's Name", bg='#ffffff', font=('Arial', 18))
        self.search_label.grid(row=0, column=0, padx=20, pady=20, sticky=W)

        self.search_entry = Entry(self.bottom_frame, width=30, font=('Arial', 14))
        self.search_entry.grid(row=0, column=1, padx=10, pady=20, sticky=W)

        self.search_button = Button(self.bottom_frame, text="Search", command=self.search_db, 
                                    bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'), width=12)
        self.search_button.grid(row=0, column=2, padx=10, pady=20)

        # Result frame (where the update form will be shown)
        self.result_frame = LabelFrame(self.bottom_frame, text="Update Customer Details", 
                                       font=('Arial', 16, 'bold'), bg='#f0f0f0', padx=20, pady=20)
        self.result_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky=W+E)

    def search_db(self):
        self.input = self.search_entry.get()

        sql = "SELECT * FROM appointments WHERE name LIKE ?"
        self.res = c.execute(sql, (self.input,))
        result = False  # to check if a result is found

        for self.row in self.res:
            result = True
            self.name1 = self.row[1]
            self.age = self.row[2]
            self.gender = self.row[3]
            self.location = self.row[4]
            self.time = self.row[6]
            self.phone = self.row[5]

        if result:
            # Call the update form creation method
            self.create_update_form()
        else:
            tkinter.messagebox.showerror("Error", "No customer found with that name")

    def create_update_form(self):
        # Clear the frame if it has any previous content
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        self.create_label_entry("Customer's Name", 0, self.name1)
        self.create_label_entry("Age", 1, self.age)
        self.create_label_entry("Gender", 2, self.gender)
        self.create_label_entry("Address", 3, self.location)
        self.create_label_entry("Book Date", 4, self.time)
        self.create_label_entry("Phone Number", 5, self.phone)

        self.update_button = Button(self.result_frame, text="Update", command=self.update_db, bg='#4CAF50', 
                                    fg='white', font=('Arial', 14, 'bold'), width=12)
        self.update_button.grid(row=6, column=1, pady=20)

        self.delete_button = Button(self.result_frame, text="Delete", command=self.delete_db, bg='#F44336', 
                                    fg='white', font=('Arial', 14, 'bold'), width=12)
        self.delete_button.grid(row=6, column=2, pady=20)

    # Method to create labels and entry widgets inside the result frame
    def create_label_entry(self, text, row, value):
        label = Label(self.result_frame, text=text, font=('Arial', 14), bg='#f0f0f0')
        label.grid(row=row, column=0, padx=10, pady=10, sticky=W)

        entry = Entry(self.result_frame, width=30, font=('Arial', 12))
        entry.grid(row=row, column=1, padx=10, pady=10)
        entry.insert(END, str(value))

        # Storing entries for later use
        if row == 0:
            self.ent1 = entry
        elif row == 1:
            self.ent2 = entry
        elif row == 2:
            self.ent3 = entry
        elif row == 3:
            self.ent4 = entry
        elif row == 4:
            self.ent5 = entry
        elif row == 5:
            self.ent6 = entry

    def update_db(self):
        # declaring the variables to update
        self.var1 = self.ent1.get()  # updated name
        self.var2 = self.ent2.get()  # updated age
        self.var3 = self.ent3.get()  # updated gender
        self.var4 = self.ent4.get()  # updated address
        self.var5 = self.ent5.get()  # updated phone
        self.var6 = self.ent6.get()  # updated date

        query = "UPDATE appointments SET name=?, age=?, gender=?, location=?, phone=?, scheduled_time=? WHERE name LIKE ?"
        c.execute(query, (self.var1, self.var2, self.var3, self.var4, self.var5, self.var6, self.search_entry.get(),))
        conn.commit()
        tkinter.messagebox.showinfo("Updated", "Successfully Updated.")

    def delete_db(self):
        sql2 = "DELETE FROM appointments WHERE name LIKE ?"
        c.execute(sql2, (self.search_entry.get(),))
        conn.commit()
        tkinter.messagebox.showinfo("Success", "Deleted Successfully")

# creating the object
root = Tk()
b = Application(root)
root.geometry("800x600+100+50")
root.resizable(False, False)
root.mainloop()
