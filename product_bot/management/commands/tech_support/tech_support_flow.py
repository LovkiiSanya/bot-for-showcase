from binotel_api_handler import binotel, create_note_for_patient
from product_bot.management.buttons.bot_buttons import TechSupportButtons
from product_bot.management.commands.bot_validation.phone_validation import (
    normalize_phone_number,
    validate_int_phone_number,
    validate_ukr_phone_number,
)
from product_bot.management.commands.tech_support.constants import (
    TECHNICAL_ISSUE_REQUEST,
    UNAUTHORIZED_EMAIL_TECH,
    tags,
)


def handle_patient_request(bot, chat_id, patient):
    """
    Handle a request from a known patient.

    Args:
        bot (TeleBot): The bot instance used to send messages to the user.
        chat_id (int): The ID of the chat where the message will be sent.
        patient (Patient): The patient object
            containing the patient's information.
    """
    markup = TechSupportButtons.appointment_button_accept()
    bot.send_message(
        chat_id,
        "Ваш запит передано до технічної підтримки.",
        reply_markup=markup,
    )
    create_note_for_patient(
        "Запит на зворотній дзвінок: ",
        patient.phone_number,
        patient.customer_id,
        chat_id,
        bot,
    )
    binotel.update_customer_labels(
        customer_id=patient.customer_id,
        email=patient.email,
        tags=tags,
    )


def handle_phone_request(bot, message, patient):
    """
    Request the phone number from the user.

    Args:
        bot (TeleBot): The bot instance used to send messages to the user.
        message (Message): The message object containing the user's input.
        patient (Patient): The patient object associated with the user.

    """
    bot.send_message(
        message.chat.id,
        "Будь ласка, введіть телефон у форматі +380********* "
        + "або натисніть кнопку 'Поділитися номером'.",
    )
    bot.register_next_step_handler(
        message,
        lambda msg: handle_phone_validation(bot, msg, patient),
    )


def handle_phone_validation(bot, message, patient):
    """
    Validate and process the phone number.

    Args:
        bot (TeleBot): The bot instance used to send messages to the user.
        message (Message): The message object containing the user's input.
        patient (Patient): The patient object associated with the user.

    """
    chat_id = message.chat.id
    phone_number = message.text.strip() if message.text else None
    username = (
        "@{}".format(message.from_user.username) if message.from_user.username else "Без імені"
    )

    if message.contact:
        phone_number = message.contact.phone_number

    if not phone_number:
        bot.send_message(
            chat_id,
            "Телефонний номер не знайдено. Будь ласка, спробуйте ще раз.",
        )
        bot.register_next_step_handler(
            message,
            lambda msg: handle_phone_validation(bot, msg, patient),
        )

        return

    phone_number = normalize_phone_number(phone_number)

    if not (validate_ukr_phone_number(phone_number) or validate_int_phone_number(phone_number)):
        bot.send_message(
            chat_id,
            "Будь ласка, введіть правильний номер телефону у форматі +380*********.",
        )
        bot.register_next_step_handler(
            message,
            lambda msg: handle_phone_validation(bot, msg, patient),
        )

        return

    handle_create_note(bot, chat_id, phone_number, username)


def handle_create_note(bot, chat_id, phone_number, username):
    """
    Create a support request note for an unregistered user.

    Args:
        bot (TeleBot): The bot instance used to send messages to the user.
        chat_id (int): The chat ID of the user.
        phone_number (str): The phone number of the user.
        username (str): The username of the user, or None if not provided.

    """
    customer_id = TECHNICAL_ISSUE_REQUEST
    email = UNAUTHORIZED_EMAIL_TECH
    markup = TechSupportButtons.appointment_button_accept()

    # Format username correctly
    username_display = "{}".format(username) if username else "Без імені"

    # Send confirmation message to the user
    bot.send_message(
        chat_id,
        "Ваш запит передано до технічної підтримки.",
        reply_markup=markup,
    )

    # Create a note with username included
    note_text = "Запит на зворотній дзвінок (неавторизований кліент): {} або ".format(
        username_display,
    )
    create_note_for_patient(note_text, phone_number, customer_id, chat_id, bot)
    binotel.update_customer_labels(
        customer_id=customer_id,
        email=email,
        tags=tags,
    )
