from telebot import TeleBot

from binotel_api_handler import binotel, create_note_for_patient
from product_bot.management.buttons.bot_buttons import TechSupportButtons
from product_bot.management.commands.bot_validation.message_validation import (
    is_multimedia_content,
    is_valid_issue_description,
)
from product_bot.management.commands.tech_support.constants import (
    TECH_SUPPORT_NUMBERS,
    TECHNICAL_ISSUE_REQUEST,
    UNAUTHORIZED_EMAIL_TECH,
    tags,
)
from product_bot.management.commands.tech_support.request_creation import (
    create_new_request_chatback,
)
from product_bot.management.commands.tech_support.tech_support_flow import (
    handle_patient_request,
    handle_phone_request,
)
from product_bot.models import Patient, TechSupportRequest


def handle_tech_support_query(call, bot):
    """
    Handle tech support query and present options to the user.

    Args:
        call (CallbackQuery): The callback query object that
            contains the user's interaction with the bot.
        bot (TeleBot): The bot instance used to send messages.
    """
    markup = TechSupportButtons.tech_buttons()
    bot.send_message(
        call.message.chat.id,
        "Будь ласка, оберіть варіант",
        reply_markup=markup,
    )


def handle_leave_issue_description(call, bot):
    """
    Handle issue description leaving.

    Args:
        call (CallbackQuery): The callback query object that
            contains the user's interaction with the bot.
        bot (TeleBot): The bot instance used to send messages.
    """
    bot.send_message(
        call.message.chat.id,
        "{}".format(
            "Опишіть проблему. Якщо потрібен зворотній зв'язок, залиште контактні дані.",
        ),
    )

    bot.register_next_step_handler(
        call.message,
        lambda msg: process_issue_description(msg, bot),
    )


def handle_show_contacts(call, bot):
    """
    Show tech support contact numbers.

    Args:
        call (CallbackQuery): The callback query object that
            contains the user's interaction with the bot.
        bot (TeleBot): The bot instance used to send messages.
    """
    support_numbers_message = "Наші телефони:\n{}".format(
        "\n".join(TECH_SUPPORT_NUMBERS),
    )
    markup = TechSupportButtons.appointment_button_accept()
    bot.send_message(
        call.message.chat.id,
        support_numbers_message,
        reply_markup=markup,
    )


def handle_request_callback(call, bot):
    """
    Request a callback from the user.

    Args:
        call (CallbackQuery): The callback query object that
            contains the user's interaction with the bot.
        bot (TeleBot): The bot instance used to send messages.
    """
    chat_id = call.message.chat.id
    try:
        patient = Patient.objects.filter(chat_id=chat_id).first()
    except Exception as err:
        bot.send_message(chat_id, "Помилка при пошуку пацієнта: {}".format(err))
        return

    if patient and patient.customer_id and patient.phone_number:
        handle_patient_request(bot, chat_id, patient)
    else:
        handle_phone_request(bot, call.message, patient)


def process_issue_description(message, bot: TeleBot):
    """
    Process the user's issue description.

    Args:
        message (Message): The incoming message
            object containing the issue description.
        bot (TeleBot): The TeleBot instance used to send responses to the user.

    """

    chat_id = message.chat.id

    # Check if the message contains multimedia content
    if is_multimedia_content(message):
        bot.send_message(
            chat_id,
            "Будь ласка, використовуйте тільки текстові повідомлення "
            + "без смайликів та мультимедіа.",
        )
        return

    issue_description = message.text.strip()

    # Validate the issue description
    if not is_valid_issue_description(issue_description):
        bot.send_message(
            chat_id,
            "Будь ласка, використовуйте тільки текстові повідомлення "
            + "без смайликів та мультимедіа.",
        )
        bot.register_next_step_handler(
            message,
            lambda msg: process_issue_description(msg, bot),
        )
        return

    create_note_for_patient(
        "Технічна несправність: ",
        issue_description,
        TECHNICAL_ISSUE_REQUEST,
        chat_id,
        bot,
    )
    binotel.update_customer_labels(
        customer_id=TECHNICAL_ISSUE_REQUEST,
        email=UNAUTHORIZED_EMAIL_TECH,
        tags=tags,
    )

    # Check if there's already an open request for this chat ID
    existing_request = TechSupportRequest.objects.filter(
        chat_id=chat_id,
        status="open",
    ).first()

    if existing_request:
        markup = TechSupportButtons.appointment_button_accept()
        bot.send_message(
            chat_id,
            "Дякуємо, Вашу заявку прийнято.",
            reply_markup=markup,
        )
    else:
        # Create a new tech support request
        markup = TechSupportButtons.appointment_button_accept()
        create_new_request_chatback(chat_id, issue_description)
        bot.send_message(
            chat_id,
            "Ваша заявка збережена та передана на обробку.",
            reply_markup=markup,
        )
