from unittest.mock import MagicMock

import pytest
from django.contrib.auth.models import User

from product_bot.management.registration_hanlers.name import NameHandler
from product_bot.management.registration_hanlers.phone import PhoneHandler
from product_bot.management.registration_hanlers.start import StartRegistrationHandler
from product_bot.models import Patient


@pytest.fixture
def user_fixture(db):
    """Fixture to create and return a test user instance.

    This fixture creates a user in the database with the specified username,
    email, and password. It is useful for testing user-related functionality
    without affecting real data.

    Args:
        db: The database fixture, which ensures that the test user is created
            in the test database.

    Returns:
        User: An instance of the User model with the specified username,
              email, and password."""
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="password",
    )


@pytest.fixture
def patient_fixture(db):
    """
    Creates and returns a test patient.

    Parameters:
        db: Django database fixture to enable database access.

    Returns:
        Patient: A test patient instance.
    """
    return Patient.objects.create(
        first_name="Test",
        last_name="Patient",
        phone_number="+380123456789",
        email="test@example.com",
        birthdate=None,
        chat_id="12345",
    )


@pytest.fixture
def bot_fixture():
    """
    Fixture to initialize the bot.

    Returns:
        MagicMock: A mocked instance of the TeleBot that can be used in tests.
    """
    bot = MagicMock()
    bot.send_message = MagicMock()
    bot.register_next_step_handler = MagicMock()
    return bot


@pytest.fixture
def handler_fixture(bot_fixture):  # noqa: WPS442
    """
    Creates and returns the PatientRegistrationHandler with mocked bot.

    Parameters:
        bot_fixture (MagicMock): A mocked bot instance.

    Returns:
        PatientRegistrationHandler: The handler initialized with the mock bot.
    """
    return StartRegistrationHandler(bot_fixture)


@pytest.fixture
def handler_fixture_name(bot_fixture):  # noqa: WPS442
    """
    Pytest fixture for initializing the NameHandler with a mocked bot.

    Args:
        bot_fixture (MagicMock): A mocked bot instance used for testing.

    Returns:
        NameHandler: An instance of NameHandler initialized with a mock bot.
    """
    return NameHandler(bot_fixture)


@pytest.fixture
def handler_fixture_phone(bot_fixture):  # noqa: WPS442
    """
    Pytest fixture for initializing the PhoneHandler with a mocked bot.

    Args:
        bot_fixture (MagicMock): A mocked bot instance used for testing.

    Returns:
        PhoneHandler: An instance of PhoneHandler initialized with a mock bot.
    """
    return PhoneHandler(bot_fixture)
