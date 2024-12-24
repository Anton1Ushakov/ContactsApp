import tkinter as tk
from tkinter import messagebox
from datetime import datetime

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
        self.file_menu.add_command(label="Delete", command=self.delete_contact)
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

        # Add VK link to the contact details frame
        self.vk_label = tk.Label(self.details_frame, text="VK ID:")
        self.vk_label.grid(row=6, column=0, sticky="w")
        self.vk_value = tk.Label(self.details_frame, text="", fg="blue", cursor="hand2")
        self.vk_value.grid(row=6, column=1, sticky="w")
        self.vk_value.bind("<Button-1>", self.open_vk_link)

        self.age_label = tk.Label(self.details_frame, text="Age:")
        self.age_label.grid(row=5, column=0, sticky="w")
        self.age_value = tk.Label(self.details_frame, text="")
        self.age_value.grid(row=5, column=1, sticky="w")

        self.update_contact_list()

    def update_contact_list(self, filtered_contacts=None, selected_index=None):
        self.contact_list.delete(0, tk.END)
        contacts = filtered_contacts if filtered_contacts else self.contact_service.get_contacts()
        for contact in contacts:
            self.contact_list.insert(tk.END, f"{contact['name']} {contact['surname']}")

        # If a specific contact is selected, highlight it and show its details
        if selected_index is not None:
            self.contact_list.selection_clear(0, tk.END)
            self.contact_list.select_set(selected_index)
            self.display_contact_details(None)

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

        # Convert date of birth to DD/MM/YYYY format
        dob = contact["dateOfBirth"]
        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d")
            formatted_dob = dob_date.strftime("%d/%m/%Y")
        except ValueError:
            formatted_dob = dob

        self.dob_value.config(text=formatted_dob)
        self.age_value.config(text=f"{self.contact_service.calculate_age(contact['dateOfBirth'])} years")
        self.vk_value.config(text=contact.get("vkLink", ""), fg="blue" if contact.get("vkLink") else "black")

    def open_vk_link(self, event):
        vk_url = self.vk_value.cget("text")
        if vk_url:
            import webbrowser
            webbrowser.open(vk_url)

    def add_contact(self):
        AddContactWindow(self.root, self.contact_service, self.update_contact_list)

    def edit_contact(self):
        if len(self.contact_list.curselection()) == 0:
            messagebox.showwarning("Warning", "Please select a contact to edit.")
            return
        index = self.contact_list.curselection()[0]

        # Pass the selected index to update the contact details after editing
        EditContactWindow(self.root, self.contact_service, lambda: self.update_contact_list(selected_index=index), index)

    def delete_contact(self):
        if len(self.contact_list.curselection()) == 0:
            messagebox.showwarning("Warning", "Please select a contact to delete.")
            return

        # Confirmation dialog
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this contact?")
        if not confirm:
            return

        index = self.contact_list.curselection()[0]
        self.contact_service.delete_contact(index)
        self.update_contact_list()

        # If the list is not empty, select the first contact and display its details
        if self.contact_list.size() > 0:
            self.contact_list.selection_clear(0, tk.END)
            self.contact_list.select_set(0)
            self.display_contact_details(None)

    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About ContactsApp")
        about_window.geometry("400x300")
        about_window.resizable(False, False)

        # Create a frame for left alignment
        content_frame = tk.Frame(about_window)
        content_frame.pack(fill="both", padx=20, pady=10, anchor="w", expand=True)

        # Title
        title_label = tk.Label(content_frame, text="ContactsApp", font=("Arial", 24, "bold"), anchor="w",
                               justify="left")
        title_label.pack(anchor="w")

        # Version
        version_label = tk.Label(content_frame, text="v. 1.0.0", font=("Arial", 14), anchor="w", justify="left")
        version_label.pack(anchor="w", pady=5)

        # Author
        author_label = tk.Label(content_frame, text="Author: Anton Ushakov", font=("Arial", 12), anchor="w",
                                justify="left")
        author_label.pack(anchor="w", pady=2)

        # Feedback email
        email_label = tk.Label(content_frame, text="Email for feedback: ushakov-rea@mail.ru", font=("Arial", 12),
                               anchor="w", justify="left")
        email_label.pack(anchor="w", pady=2)

        # GitHub link
        github_label = tk.Label(content_frame, text="GitHub: github.com/antonushakov", font=("Arial", 12), fg="blue",
                                cursor="hand2", anchor="w", justify="left")
        github_label.pack(anchor="w", pady=2)
        github_label.bind("<Button-1>", lambda e: self.open_url("https://github.com/Anton1Ushakov"))

        # Footer placeholder at the bottom
        footer_frame = tk.Frame(content_frame)
        footer_frame.pack(side="bottom", fill="x", pady=10)

        footer_label = tk.Label(footer_frame, text="© 2024 Anton Ushakov", font=("Arial", 10, "italic"), anchor="w",
                                justify="left")
        footer_label.pack(anchor="w")

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)



