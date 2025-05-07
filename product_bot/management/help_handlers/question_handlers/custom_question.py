import logging

from binotel_api_handler import binotel, create_note_for_patient
from product_bot.management.buttons.bot_buttons import TechSupportButtons
from product_bot.management.commands.tech_support.constants import tags
from product_bot.management.lists.list_of_tech import registration_button
from product_bot.models import Patient

logger = logging.getLogger(__name__)


def handle_own_question(call, bot):
    chat_id = call.message.chat.id
    patient = _fetch_patient(chat_id, bot)

    if not patient or not patient.customer_id:
        _handle_patient_not_registered(chat_id, bot)
        return

    bot.send_message(
        chat_id,
        "Будь ласка, напишіть своє питання. Ми відповімо Вам найближчим часом.",
    )

    bot.register_next_step_handler(
        call.message,
        lambda message: receive_own_question(message, bot),
    )


def receive_own_question(message, bot):
    """
    Handle a user's custom question submission.

    This function processes a user's custom free-text question, checks if the
    user is registered, and if so, creates a note and updates their labels in Binotel.
    If the user is not registered, it prompts them to register.

    Args:
        message (Message):
            The Telegram message object containing the user's question.
        bot (TeleBot):
            The bot instance used to send messages and manage interactions.

    Returns:
        None
    """

    chat_id = message.chat.id
    user_question = message.text

    patient = _fetch_patient(chat_id, bot)
    if not patient:
        return

    if not patient.customer_id:
        _handle_patient_not_registered(chat_id, bot)
        return

    _handle_create_note(user_question, patient, chat_id, bot)
    _handle_update_labels(patient)
    _send_confirmation_message(chat_id, bot)


def _fetch_patient(chat_id, bot):
    try:
        return Patient.objects.filter(chat_id=chat_id).first()
    except Exception as err:
        markup = TechSupportButtons.appointment_button_accept()
        bot.send_message(
            chat_id,
            "Виникла помилка пошуку пацієнта. Будь ласка, спробуйте ще раз пізніше.",
            reply_markup=markup,
        )
        logger.exception("Error fetching patient: {}".format(err))
        return None


def _handle_patient_not_registered(chat_id, bot):
    markup = TechSupportButtons.create_tech_support_buttons()
    markup.add(registration_button)
    bot.send_message(
        chat_id,
        "Ви не зареєстровані. Будь ласка, пройдіть процес реєстрації.",
        reply_markup=markup,
    )


def _handle_create_note(user_question, patient, chat_id, bot):
    try:
        create_note_for_patient(
            "Користувацьке питання: ",
            user_question,
            patient.customer_id,
            chat_id,
            bot,
        )
    except Exception as err:
        logger.exception("Error creating note: {}".format(err))
        bot.send_message(
            chat_id,
            "Виникла помилка при створенні нотатки. Будь ласка, спробуйте ще раз пізніше.",
        )
        raise


def _handle_update_labels(patient):
    try:
        binotel.update_customer_labels(
            customer_id=patient.customer_id,
            email=patient.email,
            tags=tags,
        )
    except Exception as err:
        logger.exception("Error updating customer labels: {}".format(err))


def _send_confirmation_message(chat_id, bot):
    markup = TechSupportButtons.appointment_button_accept()
    try:
        bot.send_message(
            chat_id,
            "Ваше питання буде передано спеціалістам.",
            reply_markup=markup,
        )
    except Exception as err:
        logger.exception("Error sending confirmation message: {}".format(err))
