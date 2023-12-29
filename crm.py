import re
import string
from tinydb import TinyDB, where, table
from pathlib import Path
from typing import List

# Define the User class to handle user data and interact with a TinyDB database.
class User:
    # Initialize a TinyDB instance to store user data in a JSON file.
    DB = TinyDB(Path(__file__).resolve().parent / 'db.json', indent=4)

    # Constructor for the User class, initializing basic user details.
    def __init__(self, first_name: str, last_name: str, phone_number: str = "", address: str = ""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address

    # Representation method for the User class, useful for debugging.
    def __repr__(self):
        return f"User({self.first_name}, {self.last_name})"

    # String method to return a readable string representation of a User instance.
    def __str__(self):
        return f"{self.full_name}\n{self.phone_number}\n{self.address}"

    # Property to get the full name of the user.
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # Property to get a user's document from the database.
    @property
    def db_instance(self) -> table.Document:
        return User.DB.get((where('first_name') == self.first_name) & (where('last_name') == self.last_name))

    # Private method to perform checks on user data.
    def _checks(self):
        self._check_phone_number()
        self._check_names()

    # Private method to validate the phone number format.
    def _check_phone_number(self):
        phone_number = re.sub(r"[+()\s]*", "", self.phone_number)
        if len(phone_number) < 10 or not phone_number.isdigit():
            raise ValueError(f"Numéro de téléphone {self.phone_number} invalide.")

    # Private method to validate first and last names.
    def _check_names(self):
        if not (self.first_name and self.last_name):
            raise ValueError("Le prénom et le nom de famille ne peuvent pas être vides.")

        special_characters = string.punctuation + string.digits

        for character in self.first_name + self.last_name:
            if character in special_characters:
                raise ValueError(f"Nom invalide {self.full_name}.")

    # Method to check if a user exists in the database.
    def exists(self):
        return bool(self.db_instance)

    # Method to delete a user from the database.
    def delete(self) -> List[int]:
        if self.exists():
            return User.DB.remove(doc_ids=[self.db_instance.doc_id])
        return []

    # Method to save a new user to the database.
    def save(self, validate_data: bool = False) -> int:
        if validate_data:
            self._checks()

        if self.exists():
            return -1
        else:
            return User.DB.insert(self.__dict__)

# Function to retrieve all users from the database.
def get_all_users():
    return [User(**user) for user in User.DB.all()]

# Main block to create a User instance.
if __name__ == "__main__":
    martin = User("Martin", "Voisin")
