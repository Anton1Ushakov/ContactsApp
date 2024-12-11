import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class AddContactWindow:
    def __init__(self, parent, contact_service, update_callback):
        self.contact_service = contact_service
        self.update_callback = update_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Add Contact")
        self.window.geometry("400x300")

        tk.Label(self.window, text="Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.name_entry = tk.Entry(self.window)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.window, text="Surname:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.surname_entry = tk.Entry(self.window)
        self.surname_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.window, text="Email:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.email_entry = tk.Entry(self.window)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.window, text="Phone:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.phone_entry = tk.Entry(self.window)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.window, text="Date of Birth (DD/MM/YYYY):").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.dob_entry = tk.Entry(self.window)
        self.dob_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Button(self.window, text="Save", command=self.save_contact).grid(row=5, column=0, columnspan=2, pady=10)

    def validate_date(self, date_str):
        try:
            # Check if the date is in DD/MM/YYYY format
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def save_contact(self):
        dob = self.dob_entry.get()
        if not self.validate_date(dob):
            messagebox.showerror("Invalid Date", "Please enter the date of birth in DD/MM/YYYY format.")
            return

        contact_data = {
            "name": self.name_entry.get(),
            "surname": self.surname_entry.get(),
            "email": self.email_entry.get(),
            "phoneNumber": self.phone_entry.get(),
            "dateOfBirth": dob,
        }

        try:
            self.contact_service.add_contact(contact_data)
            self.update_callback()
            self.window.destroy()
            messagebox.showinfo("Success", "Contact added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
