import tkinter as tk
from tkinter import messagebox

class EditContactWindow:
    def __init__(self, parent, contact_service, update_callback, contact_index):
        self.contact_service = contact_service
        self.update_callback = update_callback
        self.contact_index = contact_index

        self.window = tk.Toplevel(parent)
        self.window.title("Edit Contact")
        self.window.geometry("400x400")

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
        self.dob_entry = tk.Entry(self.window)
        self.dob_entry.grid(row=4, column=1, padx=10, pady=5)
        self.dob_entry.insert(0, contact["dateOfBirth"])

        tk.Label(self.window, text="Age:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.age_label = tk.Label(self.window, text=f"{self.contact_service.calculate_age(contact['dateOfBirth'])} years")
        self.age_label.grid(row=5, column=1, sticky="w", padx=10, pady=5)

        self.save_button = tk.Button(self.window, text="Save", command=self.save_contact)
        self.save_button.grid(row=6, column=0, columnspan=2, pady=10)

    def save_contact(self):
        updated_contact = {
            "name": self.name_entry.get(),
            "surname": self.surname_entry.get(),
            "email": self.email_entry.get(),
            "phoneNumber": self.phone_entry.get(),
            "dateOfBirth": self.dob_entry.get()
        }
        self.contact_service.update_contact(self.contact_index, updated_contact)
        self.update_callback()
        self.window.destroy()
