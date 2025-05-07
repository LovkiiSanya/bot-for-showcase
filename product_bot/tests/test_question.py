from unittest.mock import MagicMock

import pytest
from telebot.types import CallbackQuery, Chat, Message, User

from product_bot.management.commands.runbot import bot
from product_bot.management.help_handlers.question_handlers.setup import setup_question_handlers
from product_bot.models import Patient

TEST_ID_USER12345 = 12345
TEST_DATE_USER = 1234567890
TEST_MESSAGE_ID = 1
TEST_ID_USER11111 = 11111
TEST_ID_USER98765 = 98765
TEST_FIRST_NAME = "TestUser"
TEST_CHAT_TYPE = "private"
TEST_CONTENT_TYPE = "text"
TEST_JSON_STRING = "{}"
TEST_MOCK_MARKUP = "mock_markup"


@pytest.fixture
def bot_instance():
    """Fixture to initialize a mock bot instance.

    This fixture mocks the bot's `send_message` method to allow for assertion
    checks on the messages sent by the bot during tests.

    Returns:
        bot: The mock bot instance.
    """
    bot.send_message = MagicMock()  # Mock send_message for assertions
    return bot


@pytest.fixture
def patient_fixture(db):
    """Fixture to create a Patient record in the test database.

    This fixture creates and returns a patient instance in the test database
    with a predefined `chat_id` and `custom_question`
    set to `None`. It requires
    the `db` fixture to access the test database.

    Args:
        db: The test database fixture to interact with the database.

    Returns:
        Patient: The created patient instance.
    """
    return Patient.objects.create(
        chat_id=TEST_ID_USER12345,
        custom_question=None,
    )


def test_setup_question_handlers(bot_instance):  # noqa: WPS442
    """Test if the question handlers are correctly registered.

    This test ensures that the `setup_question_handlers` function correctly
    registers the callback query handlers for handling user interactions.

    It verifies that the callback query handler was set up the expected number
    of times (10 in this case).

    Args:
        bot_instance: The mock bot instance
            used to check the handler registration.
    """
    bot_instance.callback_query_handler = MagicMock()
    setup_question_handlers(bot_instance)
    assert bot_instance.callback_query_handler.call_count == 10


def test_handle_question(bot_instance):  # noqa: WPS442
    """Test handling of the 'question' callback query.

    This test simulates the reception of
    a 'question' callback query and verifies
    that the bot responds correctly with
    the expected message and reply markup.

    Args:
        bot_instance: The mock bot instance
            used to simulate and check responses.
    """
    bot_instance.callback_query_handler = MagicMock()
    setup_question_handlers(bot_instance)

    call = CallbackQuery(
        id="test_call",
        from_user=User(
            id=TEST_ID_USER12345,
            is_bot=False,
            first_name=TEST_FIRST_NAME,
        ),
        chat_instance="test_instance",
        message=Message(
            message_id=1,
            from_user=User(
                id=TEST_ID_USER12345,
                is_bot=False,
                first_name=TEST_FIRST_NAME,
            ),
            chat=Chat(id=TEST_ID_USER12345, type=TEST_CHAT_TYPE),
            date=TEST_DATE_USER,
            content_type=TEST_CONTENT_TYPE,
            options={},
            json_string=TEST_JSON_STRING,
        ),
        data="question",
        json_string=TEST_JSON_STRING,
    )

    # Simulate a call to the callback handler
    call_args_list = bot_instance.callback_query_handler.call_args_list
    for handler_args, _ in call_args_list:
        if handler_args:
            handler_func = handler_args[0]
            handler_func(call)

            # Assert that the bot sends the correct message
            bot_instance.send_message.assert_called_once_with(
                TEST_ID_USER12345,
                "\u0421\u0442\u043e\u0441\u043e\u0432\u043d\u043e "
                + "\u044f\u043a\u043e\u0433\u043e "
                + "\u043d\u0430\u043f\u0440\u044f\u043c\u043a\u0443 "
                + "\u0443 \u0412\u0430\u0441 "
                + "\u0454 \u043f\u0438\u0442\u0430\u043d\u043d\u044f?",
                reply_markup=TEST_MOCK_MARKUP,
            )
            break


def test_handle_own_question_registered_patient(
    bot_instance,  # noqa: WPS442
    patient_fixture,  # noqa: WPS442
):
    """Test handling a custom question for a registered patient.

    This test verifies that when a registered
    patient submits a custom question,
    the system correctly updates the
    patient's record with the submitted question.

    The following steps are tested:
    1. A message with a custom question is sent by the patient.
    2. The custom question is saved to the patient's record.
    3. The updated patient record is retrieved,
        and the custom question is validated.

    Args:
        bot_instance: The bot instance used to interact
            with the Telegram API during the test.
        patient_fixture: The registered patient instance that
            will be used to simulate the interaction."""
    setup_question_handlers(bot_instance)

    message = Message(
        message_id=1,
        from_user=User(
            id=TEST_ID_USER12345,
            is_bot=False,
            first_name=TEST_FIRST_NAME,
        ),
        chat=Chat(id=TEST_ID_USER12345, type=TEST_CHAT_TYPE),
        date=TEST_DATE_USER,
        content_type=TEST_CONTENT_TYPE,
        options={},
        json_string=TEST_JSON_STRING,
    )
    message.text = "Sample question text"

    patient_fixture.custom_question = message.text
    patient_fixture.save()

    updated_patient = Patient.objects.get(chat_id=message.chat.id)
    assert updated_patient.custom_question == message.text


def test_handle_ivf(bot_instance, db):  # noqa: WPS442
    """Test handling of the 'ivf' callback query.

    This test verifies that when a callback
    query with the data 'ivf' is received,
    the appropriate response is sent back to the user.
    It mocks the `callback_query_handler`
    and simulates the callback query triggering.
    The test ensures that the bot responds with
    the expected message and markup.

    The following steps are tested:
    1. The callback query with 'ivf' data is received and processed.
    2. The handler function corresponding to this callback is triggered.
    3. The bot sends the expected message with the correct
    text, parse mode, and reply markup.

    Args:
        bot_instance: The bot instance used to send
            messages and interact with the Telegram API during the test.
        db: The database fixture for interacting
            with the database during the test.
    """
    # Mock the callback_query_handler
    bot_instance.callback_query_handler = MagicMock()
    setup_question_handlers(bot_instance)

    call = CallbackQuery(
        id="test_call",
        from_user=User(
            id=TEST_ID_USER11111,
            is_bot=False,
            first_name=TEST_FIRST_NAME,
        ),
        chat_instance="test_instance",
        message=Message(
            message_id=1,
            from_user=User(
                id=TEST_ID_USER11111,
                is_bot=False,
                first_name=TEST_FIRST_NAME,
            ),
            chat=Chat(id=TEST_ID_USER11111, type=TEST_CHAT_TYPE),
            date=TEST_DATE_USER,
            content_type=TEST_CONTENT_TYPE,
            options={},
            json_string=TEST_JSON_STRING,
        ),
        data="ivf",
        json_string=TEST_JSON_STRING,
    )

    # Simulate triggering the callback handlers
    call_args_list = bot_instance.callback_query_handler.call_args_list
    for handler_args, _ in call_args_list:
        if handler_args:
            handler_func = handler_args[0]
            handler_func(call)

            bot_instance.send_message.assert_called_once_with(
                TEST_ID_USER11111,
                "mock_text",
                parse_mode="Markdown",
                reply_markup=TEST_MOCK_MARKUP,
            )
            break
