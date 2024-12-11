import tkinter as tk
from tkinter import messagebox
from business.contact_service import ContactService
from ui.add_contact_window import AddContactWindow
from ui.edit_contact_window import EditContactWindow

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Contacts App")
        self.contact_service = ContactService()

        # Configure the window layout
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # Create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Add contact", command=self.add_contact)
        self.file_menu.add_command(label="Edit contact", command=self.edit_contact)
        self.menu_bar.add_cascade(label="Edit", menu=self.file_menu)


        # About menu
        self.about_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.about_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)

        # Search bar
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(fill="x", padx=10, pady=5)
        self.search_label = tk.Label(self.search_frame, text="Search:")
        self.search_label.pack(side="left")
        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.search_entry.bind("<KeyRelease>", self.filter_contacts)

        # Contact list frame
        self.contact_frame = tk.Frame(self.root)
        self.contact_frame.pack(side="left", fill="y", padx=10, pady=5)

        # Contact list
        self.contact_list = tk.Listbox(self.contact_frame)
        self.contact_list.pack(fill="both", expand=True)
        self.contact_list.bind("<<ListboxSelect>>", self.display_contact_details)

        # Buttons below the contact list
        self.button_frame = tk.Frame(self.contact_frame)
        self.button_frame.pack(fill="x", pady=5)
        self.add_button = tk.Button(self.button_frame, text="Add", command=self.add_contact)
        self.add_button.pack(side="left", padx=5)
        self.edit_button = tk.Button(self.button_frame, text="Edit", command=self.edit_contact)
        self.edit_button.pack(side="left", padx=5)
        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_contact)
        self.delete_button.pack(side="left", padx=5)

        # Contact details frame
        self.details_frame = tk.Frame(self.root)
        self.details_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        self.name_label = tk.Label(self.details_frame, text="Name:")
        self.name_label.grid(row=0, column=0, sticky="w")
        self.name_value = tk.Label(self.details_frame, text="")
        self.name_value.grid(row=0, column=1, sticky="w")

        self.surname_label = tk.Label(self.details_frame, text="Surname:")
        self.surname_label.grid(row=1, column=0, sticky="w")
        self.surname_value = tk.Label(self.details_frame, text="")
        self.surname_value.grid(row=1, column=1, sticky="w")

        self.email_label = tk.Label(self.details_frame, text="Email:")
        self.email_label.grid(row=2, column=0, sticky="w")
        self.email_value = tk.Label(self.details_frame, text="")
        self.email_value.grid(row=2, column=1, sticky="w")

        self.phone_label = tk.Label(self.details_frame, text="Phone:")
        self.phone_label.grid(row=3, column=0, sticky="w")
        self.phone_value = tk.Label(self.details_frame, text="")
        self.phone_value.grid(row=3, column=1, sticky="w")

        self.dob_label = tk.Label(self.details_frame, text="Date of Birth:")
        self.dob_label.grid(row=4, column=0, sticky="w")
        self.dob_value = tk.Label(self.details_frame, text="")
        self.dob_value.grid(row=4, column=1, sticky="w")

        self.age_label = tk.Label(self.details_frame, text="Age:")
        self.age_label.grid(row=5, column=0, sticky="w")
        self.age_value = tk.Label(self.details_frame, text="")
        self.age_value.grid(row=5, column=1, sticky="w")

        self.update_contact_list()

    def update_contact_list(self, filtered_contacts=None):
        self.contact_list.delete(0, tk.END)
        contacts = filtered_contacts if filtered_contacts else self.contact_service.get_contacts()
        for contact in contacts:
            self.contact_list.insert(tk.END, f"{contact['name']} {contact['surname']}")

    def filter_contacts(self, event):
        query = self.search_entry.get()
        filtered_contacts = self.contact_service.filter_contacts(query)
        self.update_contact_list(filtered_contacts)

    def display_contact_details(self, event):
        if len(self.contact_list.curselection()) == 0:
            return
        index = self.contact_list.curselection()[0]
        contact = self.contact_service.get_contacts()[index]

        self.name_value.config(text=contact["name"])
        self.surname_value.config(text=contact["surname"])
        self.email_value.config(text=contact["email"])
        self.phone_value.config(text=contact["phoneNumber"])
        self.dob_value.config(text=contact["dateOfBirth"])
        self.age_value.config(text=f"{self.contact_service.calculate_age(contact['dateOfBirth'])} years")

    def add_contact(self):
        AddContactWindow(self.root, self.contact_service, self.update_contact_list)

    def edit_contact(self):
        if len(self.contact_list.curselection()) == 0:
            messagebox.showwarning("Warning", "Please select a contact to edit.")
            return
        index = self.contact_list.curselection()[0]
        EditContactWindow(self.root, self.contact_service, self.update_contact_list, index)

    def delete_contact(self):
        if len(self.contact_list.curselection()) == 0:
            messagebox.showwarning("Warning", "Please select a contact to delete.")
            return
        index = self.contact_list.curselection()[0]
        self.contact_service.delete_contact(index)
        self.update_contact_list()

    def show_about(self):
        messagebox.showinfo("About", "Contacts App Version 1.0\nDeveloped by [Your Name]")