import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry
import re


class AddContactWindow:
    def __init__(self, parent, contact_service, update_callback):
        self.contact_service = contact_service
        self.update_callback = update_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Add Contact")
        self.window.geometry("400x350")


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

        tk.Label(self.window, text="Date of Birth:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.dob_entry = DateEntry(self.window, width=17, background='darkblue', foreground='white', borderwidth=2,
                                   date_pattern='dd/mm/yyyy')
        self.dob_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.window, text="VK ID:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.vk_id_entry = tk.Entry(self.window)
        self.vk_id_entry.grid(row=5, column=1, padx=10, pady=5)

        today = datetime.today().date()
        self.dob_entry.config(maxdate=today)

        tk.Button(self.window, text="Save", command=self.save_contact).grid(row=6, column=0, columnspan=2, pady=10)

    def validate_email(self, email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def validate_phone(self, phone):
        pattern = r"^\+?\d{10,15}$"
        return re.match(pattern, phone) is not None

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def save_contact(self):
        errors = []

        if not self.name_entry.get():
            errors.append("Name is required.")
        if not self.surname_entry.get():
            errors.append("Surname is required.")

        email = self.email_entry.get()
        if not email:
            errors.append("Email is required.")
        elif not self.validate_email(email):
            errors.append("Invalid email format.")

        phone = self.phone_entry.get()
        if not phone:
            errors.append("Phone number is required.")
        elif not self.validate_phone(phone):
            errors.append("Invalid phone number format.")

        dob = self.dob_entry.get()
        if not dob:
            errors.append("Date of birth is required.")
        elif not self.validate_date(dob):
            errors.append("Please enter the date of birth in DD/MM/YYYY format.")

        if errors:
            messagebox.showerror("Validation Errors", "\n".join(errors))
            return

        contact_data = {
            "name": self.name_entry.get(),
            "surname": self.surname_entry.get(),
            "email": email,
            "phoneNumber": phone,
            "dateOfBirth": dob,
            "vk_id": self.vk_id_entry.get(),  # Поле VK ID теперь необязательно
        }

        try:
            self.contact_service.add_contact(contact_data)
            self.update_callback()
            self.window.destroy()
            messagebox.showinfo("Success", "Contact added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
