from crm import User
import pytest
from tinydb import TinyDB, table
from tinydb.storages import MemoryStorage

# Fixture to set up an in-memory database for testing.
@pytest.fixture
def setup_db():
    User.DB = TinyDB(storage=MemoryStorage)

# Fixture to create and return a test user, using the setup_db fixture.
@pytest.fixture
def user(setup_db):
    u = User(first_name="Patrick",
             last_name="Martin",
             address="1 rue du chemin, 75000 Paris",
             phone_number="0123456789")
    u.save()
    return u

# Test to verify the first name attribute of the user.
def test_first_name(user):
    assert user.first_name == "Patrick"

# Test to verify the full name property of the user.
def test_full_name(user):
    assert user.full_name == "Patrick Martin"

# Test to check if a user exists in the database.
def test_exists(user):
    assert user.exists() is True

# Test to verify that a new user is not in the database.
def test_not_exists(setup_db):
    u = User(first_name="Patrick",
             last_name="Martin",
             address="1 rue du chemin, 75000 Paris",
             phone_number="0123456789")
    assert u.exists() is False

# Test to check the db_instance property of the user.
def test_db_instance(user):
    assert isinstance(user.db_instance, table.Document)
    assert user.db_instance["first_name"] == "Patrick"
    assert user.db_instance["last_name"] == "Martin"
    assert user.db_instance["address"] == "1 rue du chemin, 75000 Paris"
    assert user.db_instance["phone_number"] == "0123456789"

# Test to ensure that db_instance is None for a non-existent user.
def test_not_db_instance(setup_db):
    u = User(first_name="Patrick",
             last_name="Martin",
             address="1 rue du chemin, 75000 Paris",
             phone_number="0123456789")
    assert u.db_instance is None

# Test to verify phone number validation.
def test__check_phone_number(setup_db):
    user_good = User(first_name="Jean",
                     last_name="Smith",
                     address="1 rue du chemin, 75015, Paris",
                     phone_number="0123456789")
    user_bad = User(first_name="Jean",
                    last_name="Smith",
                    address="1 rue du chemin, 75015, Paris",
                    phone_number="abcd")

    with pytest.raises(ValueError) as err:
        user_bad._check_phone_number()

    assert "invalide" in str(err.value)

    user_good.save(validate_data=True)
    assert user_good.exists() is True

# Test to verify the validation of empty names.
def test__check_names_empty(setup_db):
    user_bad = User(first_name="",
                    last_name="",
                    address="1 rue du chemin, 75000 Paris",
                    phone_number="0123456789")

    with pytest.raises(ValueError) as err:
        user_bad._check_names()

    assert "Le prénom et le nom de famille ne peuvent pas être vides." in str(err.value)

# Test to verify the validation of names with invalid characters.
def test__check_names_invalid_characters(setup_db):
    user_bad = User(first_name="Patrick%&*$?%&",
                    last_name="#(*%$(*",
                    address="1 rue du chemin, 75000 Paris",
                    phone_number="0123456789")

    with pytest.raises(ValueError) as err:
        user_bad._check_names()

    assert "Nom invalide" in str(err.value)

# Test to verify the delete functionality of a user.
def test_delete(setup_db):
    user_test = User(first_name="John",
                     last_name="Smith",
                     address="1 rue du chemin, 75015, Paris",
                     phone_number="0123456789")
    user_test.save()
    first = user_test.delete()
    second = user_test.delete()
    assert len(first) > 0
    assert isinstance(first, list)
    assert len(second) == 0
    assert isinstance(second, list)

# Test to verify the save functionality of a user.
def test_save(setup_db):
    user_test = User(first_name="John",
                     last_name="Smith",
                     address="1 rue du chemin, 75015, Paris",
                     phone_number="0123456789")
    user_test_dup = User(first_name="John",
                         last_name="Smith",
                         address="1 rue du chemin, 75015, Paris",
                         phone_number="0123456789")
    first = user_test.save()
    second = user_test_dup.save()
    assert isinstance(first, int)
    assert isinstance(second, int)
    assert first > 0
    assert second == -1
