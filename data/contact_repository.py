import json
import os

CONTACTS_FILE = "contacts.json"

class ContactRepository:
    @staticmethod
    def load_contacts():
        """Load contacts from a JSON file."""
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
                contacts = json.load(f)
                for contact in contacts:
                    if "surname" not in contact:
                        contact["surname"] = ""  # Add empty surname if missing
                return contacts
        return []

    @staticmethod
    def save_contacts(contacts):
        """Save contacts to a JSON file."""
        with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
            json.dump(contacts, f, ensure_ascii=False, indent=4)
