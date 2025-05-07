from unittest.mock import MagicMock

import pytest

from product_bot.management.registration_hanlers.name import NameHandler
from product_bot.management.registration_hanlers.phone import PhoneHandler
from product_bot.management.registration_hanlers.start import StartRegistrationHandler
from product_bot.models import Patient


def test_start_registration(
    db,
    bot_fixture: MagicMock,  # noqa: WPS442
    handler_fixture: StartRegistrationHandler,  # noqa: WPS442
):
    """
    Test the initiation of the registration process.

    This test simulates a user starting the registration process by sending
    a message to the bot. It ensures that the `start_registration` method
    correctly sends a message to the user requesting their first name.

    Args:
        db: The database fixture for accessing the test database.
        handler_fixture: The mocked bot instance used
            to simulate bot interactions.
        bot_fixture: The handler instance responsible for starting
            the registration process and handling user inputs.

    Assertions:
        Verifies that:
            1. The bot sends a message asking the
            user to provide their first name.
    """
    chat_id = 12345
    message = MagicMock(chat=MagicMock(id=chat_id))

    handler_fixture.start(message)

    bot_fixture.send_message.assert_called_once_with(
        chat_id,
        "Вкажіть Ваше ім'я",
    )


def test_get_first_name_invalid(
    db,
    bot_fixture: MagicMock,  # noqa: WPS442
    handler_fixture_name: NameHandler,  # noqa: WPS442
):
    chat_id = 12345
    message = MagicMock(chat=MagicMock(id=chat_id), text="")

    handler_fixture_name.ask_first_name(message)

    bot_fixture.send_message.assert_called_once_with(
        chat_id,
        "Ім'я не може містити спеціальні символи. Будь ласка спробуйте ще раз.",
    )
    bot_fixture.register_next_step_handler.assert_called_once_with(
        message,
        handler_fixture_name.ask_first_name,
    )


def test_get_phone_number_valid(
    db,
    bot_fixture: MagicMock,  # noqa: WPS442
    patient_fixture: Patient,  # noqa: WPS442
    handler_fixture_phone: PhoneHandler,  # noqa: WPS442
):
    chat_id = patient_fixture.chat_id
    message = MagicMock(chat=MagicMock(id=chat_id), text="+380123456789")

    handler_fixture_phone.handle(
        message,
        patient_fixture.first_name,
        patient_fixture.last_name,
    )

    bot_fixture.send_message.assert_called_once_with(
        chat_id,
        "Будь ласка, вкажіть свій контактний номер телефону у форматі "
        + "+380********* або натисніть кнопку 'Поділитися номером'",
    )


if __name__ == "__main__":
    pytest.main()
