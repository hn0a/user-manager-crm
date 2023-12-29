# User Management System

This User Management System, implemented in Python, is designed for efficient handling of user data. It provides functionalities for creating, validating, and storing user information, using TinyDB for data persistence. The system is ideal for small-scale applications requiring user data management.

## Features

- **User Data Handling (`crm.py`)**: Allows the creation and management of user data including names, phone numbers, and addresses.
- **Data Validation**: Ensures the integrity of user data by validating phone numbers and checking for invalid characters in names.
- **Database Operations**: Facilitates operations like saving, deleting, and checking for the existence of users in the database.
- **Automated Testing (`test_crm.py`)**: Includes tests for validating the functionality of the User Management System using PyTest.

## Installation

Before using this system, make sure Python is installed on your system. Install the necessary dependencies as follows:

```bash
pip install tinydb
pip install pytest
```

## Usage

### Basic Usage (`crm.py`)

Import the `User` class from the `crm` module to manage user data. Here's an example:

```python
from crm import User

# Create a new user
user = User(first_name="John", last_name="Doe", phone_number="0123456789", address="123 Main St")

# Save the user to the database
user.save()

# Check if the user exists in the database
print(user.exists())

# Output user details
print(user)
```

### Testing (`test_crm.py`)

To ensure the system works as expected, a series of tests are provided. Run these tests using PyTest:

```bash
pytest test_crm.py
```

Make sure PyTest is installed:

```bash
pip install pytest
```

## File Structure

- `crm.py`: Contains the User class and database interaction logic.
- `test_crm.py`: Includes tests for validating the functionalities in `crm.py`.

## License

This User Management System is released under the [MIT License](https://opensource.org/licenses/MIT).
