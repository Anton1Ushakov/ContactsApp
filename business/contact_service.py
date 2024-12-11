from data.contact_repository import ContactRepository
from datetime import datetime

class ContactService:
    def __init__(self):
        self.contacts = ContactRepository.load_contacts()

    def get_contacts(self):
        """Retrieve all contacts."""
        return self.contacts

    def add_contact(self, contact_data):
        """Add a new contact."""
        try:
            # Validate and format date of birth
            contact_data["dateOfBirth"] = datetime.strptime(
                contact_data["dateOfBirth"], "%d/%m/%Y"
            ).strftime("%Y-%m-%d")
            self.contacts.append(contact_data)
            ContactRepository.save_contacts(self.contacts)
        except ValueError as e:
            raise ValueError("Invalid date of birth format. Use DD/MM/YYYY.") from e

    def update_contact(self, index, updated_data):
        """Update an existing contact."""
        try:
            # Validate and format date of birth
            updated_data["dateOfBirth"] = datetime.strptime(
                updated_data["dateOfBirth"], "%d/%m/%Y"
            ).strftime("%Y-%m-%d")
            self.contacts[index] = updated_data
            ContactRepository.save_contacts(self.contacts)
        except ValueError as e:
            raise ValueError("Invalid date of birth format. Use DD/MM/YYYY.") from e

    def delete_contact(self, index):
        """Delete a contact."""
        if 0 <= index < len(self.contacts):
            del self.contacts[index]
            ContactRepository.save_contacts(self.contacts)
        else:
            raise IndexError("Contact index out of range.")

    def filter_contacts(self, query):
        """Filter contacts by name or surname."""
        query = query.lower()
        return [
            contact for contact in self.contacts
            if query in contact["name"].lower() or query in contact["surname"].lower()
        ]

    def calculate_age(self, date_of_birth):
        """Calculate the age from the date of birth."""
        birthday = datetime.strptime(date_of_birth, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - birthday.year
        if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
            age -= 1
        return age
