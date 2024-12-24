import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import messagebox
from datetime import datetime
import os
import json

# Имя файла для хранения контактов
CONTACTS_FILE = "contacts.json"

# Функция загрузки контактов из JSON-файла
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            loaded_contacts = json.load(f)
            for contact in loaded_contacts:
                if "surname" not in contact:
                    contact["surname"] = ""  # Добавить пустую фамилию
            return loaded_contacts
    return []

# Функция сохранения контактов в JSON-файл
def save_contacts():
    with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=4)

# Инициализация списка контактов из файла
contacts = load_contacts()

class AppWindow:
    def __init__(self, parent):
        # Create the main window
        self.parent = parent
        self.window = tk.Toplevel()
        self.window.geometry("670x500")
        self.window.title("Contacts App")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Create a menu bar
        self.menu_bar = tk.Menu(self.window)
        self.window.config(menu=self.menu_bar)

        # Add "New" menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.exit_program)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Add "New" menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Add contact", command=self.open_new_contact_window)
        self.file_menu.add_command(label="Edit contact", command=self.edit_contact)
        self.menu_bar.add_cascade(label="Edit", menu=self.file_menu)

        # Add "About" menu
        self.about_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.about_menu.add_command(label="About App", command=self.show_about_window)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)

        # Configure grid layout
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=3)
        self.window.rowconfigure(0, weight=0)  # Строка поиска
        self.window.rowconfigure(1, weight=1)  # Список контактов
        self.window.rowconfigure(2, weight=0)  # Кнопки

        # Create a frame for search bar
        self.search_frame = tk.Frame(self.window)
        self.search_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.search_label = tk.Label(self.search_frame, text="Search", font=("Arial", 13))
        self.search_label.pack(side="top", anchor="w")

        tk.Label(self.search_frame, font=("Arial", 13)).pack(side="left", padx=(0, 0))
        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.filter_contacts)  # Фильтровать при вводе текста

        # Create the list box (contact list)
        self.contact_list = tk.Listbox(self.window)
        self.contact_list.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.contact_list.bind("<<ListboxSelect>>", self.list_clicked)

        self.update_list()

        # Create a frame for buttons
        self.button_frame = tk.Frame(self.window)
        self.button_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        # Add buttons
        self.add_button = tk.Button(self.button_frame, text="Add", command=self.open_new_contact_window)
        self.add_button.pack(side="left", padx=5)

        self.edit_button = tk.Button(self.button_frame, text="Edit", command=self.edit_contact)
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_contact)
        self.delete_button.pack(side="left", padx=5)

        # Create a frame for contact details
        self.details_frame = tk.Frame(self.window)
        self.details_frame.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)

        # Add widgets to the details frame
        self.name_label = tk.Label(self.details_frame, text="Name", font=("Arial", 13))
        self.name_label.grid(row=0, column=0, sticky="w", pady=2, padx=(0, 100))
        self.name_text = tk.Entry(self.details_frame)
        self.name_text.grid(row=1, column=0, sticky="ew", pady=2, padx=(0, 100))

        self.surname_label = tk.Label(self.details_frame, text="Surname", font=("Arial", 13))
        self.surname_label.grid(row=2, column=0, sticky="w", pady=2, padx=(0, 100))
        self.surname_text = tk.Entry(self.details_frame)
        self.surname_text.grid(row=3, column=0, sticky="ew", pady=2, padx=(0, 100))

        self.email_label = tk.Label(self.details_frame, text="Email", font=("Arial", 13))
        self.email_label.grid(row=4, column=0, sticky="w", pady=2, padx=(0, 100))
        self.email_text = tk.Entry(self.details_frame)
        self.email_text.grid(row=5, column=0, sticky="ew", pady=2, padx=(0, 100))

        self.phone_label = tk.Label(self.details_frame, text="Phone", font=("Arial", 13))
        self.phone_label.grid(row=6, column=0, sticky="w", pady=2, padx=(0, 100))
        self.phone_text = tk.Entry(self.details_frame)
        self.phone_text.grid(row=7, column=0, sticky="ew", pady=2, padx=(0, 100))

        self.dob_label = tk.Label(self.details_frame, text="Date of birth", font=("Arial", 13))
        self.dob_label.grid(row=8, column=0, sticky="w", pady=2, padx=(0, 100))
        self.dob_text = tk.Entry(self.details_frame)
        self.dob_text.grid(row=9, column=0, sticky="ew", pady=2, padx=(0, 100))

        self.age_label = tk.Label(self.details_frame, text="Age", font=("Arial", 13))
        self.age_label.grid(row=10, column=0, sticky="w", pady=2, padx=(0, 100))
        self.age_info = tk.Label(self.details_frame, text="", font=("Arial", 13))
        self.age_info.grid(row=11, column=0, sticky="w", pady=2, padx=(0, 100))

        if contacts:
            self.contact_list.select_set(0)
            self.list_clicked(None)


    def update_list(self, filtered_contacts=None):
        self.contact_list.delete(0, tk.END)
        to_display = filtered_contacts if filtered_contacts is not None else contacts
        for contact in to_display:
            display_name = f"{contact['name']} {contact['surname']}"  # Имя + Фамилия
            self.contact_list.insert(tk.END, display_name)

    def exit_program(self):
        # Close the application
        self.window.quit()

    def filter_contacts(self, event):
        query = self.search_entry.get().lower()
        filtered_contacts = [
            contact for contact in contacts
            if query in contact["name"].lower() or query in contact["surname"].lower()
        ]
        self.update_list(filtered_contacts)


    def list_clicked(self, e):
        if len(self.contact_list.curselection()) == 0:
            return
        self.selected = int(self.contact_list.curselection()[0])
        contact = contacts[self.selected]

        self.name_text.delete(0, tk.END)
        self.name_text.insert(0, contact["name"])

        self.surname_text.delete(0, tk.END)
        self.surname_text.insert(0, contact["surname"])

        self.email_text.delete(0, tk.END)
        self.email_text.insert(0, contact["email"])

        self.phone_text.delete(0, tk.END)
        self.phone_text.insert(0, contact["phoneNumber"])

        self.dob_text.delete(0, tk.END)
        self.dob_text.insert(0, datetime.strptime(contact["dateOfBirth"], "%Y-%m-%d").strftime("%d/%m/%Y"))

        today = datetime.now()
        birthday = datetime.strptime(contact["dateOfBirth"], "%Y-%m-%d")
        age = today.year - birthday.year
        if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
            age -= 1
        self.age_info["text"] = f"{age} years"

    def open_new_contact_window(self):
        new_window = tk.Toplevel(self.window)
        new_window.geometry("400x300")
        new_window.title("New Contact")

        tk.Label(new_window, text="Name:").place(x=20, y=20)
        name_entry = tk.Entry(new_window, width=30)
        name_entry.place(x=100, y=20)

        tk.Label(new_window, text="Surname:").place(x=20, y=60)
        surname_entry = tk.Entry(new_window, width=30)
        surname_entry.place(x=100, y=60)

        tk.Label(new_window, text="Email:").place(x=20, y=100)
        email_entry = tk.Entry(new_window, width=30)
        email_entry.place(x=100, y=100)

        tk.Label(new_window, text="Phone:").place(x=20, y=140)
        phone_entry = tk.Entry(new_window, width=30)
        phone_entry.place(x=100, y=140)

        tk.Label(new_window, text="Date of Birth:").place(x=20, y=180)
        dob_entry = tk.Entry(new_window, width=30)
        dob_entry.place(x=100, y=180)

        def save_new_contact():
            try:
                # Проверка формата даты рождения
                try:
                    dob = datetime.strptime(dob_entry.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Invalid Input", "Invalid date of birth format. Use DD/MM/YYYY.")
                    return

                # Сохранение контакта
                new_contact = {
                    "name": name_entry.get(),
                    "surname": surname_entry.get(),
                    "email": email_entry.get(),
                    "phoneNumber": phone_entry.get(),
                    "dateOfBirth": dob,
                }
                contacts.append(new_contact)
                self.update_list()
                save_contacts()
                new_window.destroy()
                messagebox.showinfo("Success", "New contact saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save contact: {e}")

        save_button = tk.Button(new_window, text="Save", command=save_new_contact)
        save_button.place(x=150, y=230)

    def edit_contact(self):
        if len(self.contact_list.curselection()) == 0:
            messagebox.showwarning("Warning", "Please select a contact to edit.")
            return

        selected_index = self.contact_list.curselection()[0]
        contact = contacts[selected_index]

        edit_window = tk.Toplevel(self.window)
        edit_window.geometry("400x300")
        edit_window.title("Edit Contact")

        tk.Label(edit_window, text="Name:").place(x=20, y=20)
        name_entry = tk.Entry(edit_window, width=30)
        name_entry.place(x=100, y=20)
        name_entry.insert(0, contact["name"])

        tk.Label(edit_window, text="Surname:").place(x=20, y=60)
        surname_entry = tk.Entry(edit_window, width=30)
        surname_entry.place(x=100, y=60)
        surname_entry.insert(0, contact["surname"])

        tk.Label(edit_window, text="Email:").place(x=20, y=100)
        email_entry = tk.Entry(edit_window, width=30)
        email_entry.place(x=100, y=100)
        email_entry.insert(0, contact["email"])

        tk.Label(edit_window, text="Phone:").place(x=20, y=140)
        phone_entry = tk.Entry(edit_window, width=30)
        phone_entry.place(x=100, y=140)
        phone_entry.insert(0, contact["phoneNumber"])

        tk.Label(edit_window, text="Date of Birth:").place(x=20, y=180)
        dob_entry = tk.Entry(edit_window, width=30)
        dob_entry.place(x=100, y=180)
        dob_entry.insert(0, datetime.strptime(contact["dateOfBirth"], "%Y-%m-%d").strftime("%d/%m/%Y"))

        def save_changes():
            try:
                # Проверка формата даты рождения
                try:
                    dob = datetime.strptime(dob_entry.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Invalid Input", "Invalid date of birth format. Use DD/MM/YYYY.")
                    return

                # Сохранение изменений
                contact["name"] = name_entry.get()
                contact["surname"] = surname_entry.get()
                contact["email"] = email_entry.get()
                contact["phoneNumber"] = phone_entry.get()
                contact["dateOfBirth"] = dob
                self.update_list()
                save_contacts()
                edit_window.destroy()
                messagebox.showinfo("Success", "Contact updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update contact: {e}")

        save_button = tk.Button(edit_window, text="Save", command=save_changes)
        save_button.place(x=150, y=230)

    def delete_contact(self):
        if len(self.contact_list.curselection()) == 0:
            messagebox.showwarning("Warning", "Please select a contact to delete.")
            return
        selected_index = self.contact_list.curselection()[0]
        del contacts[selected_index]
        self.update_list()
        save_contacts()

    def on_close(self):
        self.parent.deiconify()
        self.window.destroy()

    def show_about_window(self):
        # Display the "About" window
        messagebox.showinfo(
            "About",
            "Contacts App\n"
            "Created by: Anton Ushakov\n"
            "GitHub: https://github.com/yourusername/yourrepository"
        )
# Основная программа
root = tk.Tk()
root.withdraw()
app = AppWindow(root)
root.mainloop()
