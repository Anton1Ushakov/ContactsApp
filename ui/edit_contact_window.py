import tkinter as tk
from tkinter import messagebox
import re
from datetime import datetime
from tkcalendar import DateEntry

class EditContactWindow:
    def __init__(self, parent, contact_service, update_callback, contact_index):
        self.contact_service = contact_service
        self.update_callback = update_callback
        self.contact_index = contact_index

        self.window = tk.Toplevel(parent)
        self.window.title("Edit Contact")
        self.window.geometry("400x450")  # Increased height for new field

        contact = self.contact_service.get_contacts()[contact_index]

        tk.Label(self.window, text="Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.name_entry = tk.Entry(self.window)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.name_entry.insert(0, contact["name"])

        tk.Label(self.window, text="Surname:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.surname_entry = tk.Entry(self.window)
        self.surname_entry.grid(row=1, column=1, padx=10, pady=5)
        self.surname_entry.insert(0, contact["surname"])

        tk.Label(self.window, text="Email:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.email_entry = tk.Entry(self.window)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)
        self.email_entry.insert(0, contact["email"])

        tk.Label(self.window, text="Phone:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.phone_entry = tk.Entry(self.window)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=5)
        self.phone_entry.insert(0, contact["phoneNumber"])

        tk.Label(self.window, text="Date of Birth:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.dob_entry = DateEntry(self.window, width=17, background='darkblue', foreground='white', borderwidth=2,
                                   date_pattern='dd/mm/yyyy')
        self.dob_entry.grid(row=4, column=1, padx=10, pady=5)

        today = datetime.today().date()
        self.dob_entry.config(maxdate=today)

        tk.Label(self.window, text="VK ID:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.vk_id_entry = tk.Entry(self.window)
        self.vk_id_entry.grid(row=5, column=1, padx=10, pady=5)
        self.vk_id_entry.insert(0, contact.get("vk_id", ""))

        self.save_button = tk.Button(self.window, text="Save", command=self.save_contact)
        self.save_button.grid(row=6, column=0, columnspan=2, pady=10)

    def save_contact(self):
        errors = []  # List to collect error messages

        # Collect updated contact data
        updated_contact = {
            "name": self.name_entry.get(),
            "surname": self.surname_entry.get(),
            "email": self.email_entry.get(),
            "phoneNumber": self.phone_entry.get(),
            "dateOfBirth": self.dob_entry.get(),
            "vk_id": self.vk_id_entry.get(),  # VK ID remains optional
        }

        # Check for empty fields
        if not updated_contact["name"]:
            errors.append("Name is required.")
        if not updated_contact["surname"]:
            errors.append("Surname is required.")
        if not updated_contact["email"]:
            errors.append("Email is required.")
        if not updated_contact["phoneNumber"]:
            errors.append("Phone number is required.")
        if not updated_contact["dateOfBirth"]:
            errors.append("Date of birth is required.")

        # Validate email
        if updated_contact["email"] and not self.is_valid_email(updated_contact["email"]):
            errors.append("Invalid email address. Please enter a valid email.")

        # Validate phone number
        if updated_contact["phoneNumber"] and not self.is_valid_phone(updated_contact["phoneNumber"]):
            errors.append("Invalid phone number. It must start with 7 and contain 11 digits.")

        # Validate date of birth
        if updated_contact["dateOfBirth"] and not self.is_valid_date(updated_contact["dateOfBirth"]):
            errors.append("Invalid date of birth. Please enter a valid date in DD/MM/YYYY format.")

        # If there are errors, show them in a single message box
        if errors:
            error_message = "\n".join(errors)
            messagebox.showerror("Validation Errors", error_message)
            return

        # Format date of birth
        updated_contact["dateOfBirth"] = self.format_date(updated_contact["dateOfBirth"])

        # Save the updated contact
        self.contact_service.update_contact(self.contact_index, updated_contact)
        self.update_callback()

        # Show a success message
        messagebox.showinfo("Success", "Contact saved successfully!")

        # Close the window
        self.window.destroy()

    def is_valid_email(self, email):
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_regex, email) is not None

    def is_valid_phone(self, phone):
        phone_regex = r"^7\d{10}$"  # Phone must start with 7 and contain exactly 11 digits
        return re.match(phone_regex, phone) is not None

    def is_valid_date(self, date_str):
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def format_date(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%d/%m/%Y")
        except ValueError:
            return date_str
