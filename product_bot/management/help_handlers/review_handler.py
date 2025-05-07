from telebot import TeleBot

from binotel_api_handler import create_note_for_patient
from product_bot.management.buttons.bot_buttons import AnonymousButtons, TechSupportButtons
from product_bot.management.commands.base_call_router import BaseTGCallRouter
from product_bot.management.commands.bot_validation.message_validation import (
    is_multimedia_content,
    is_valid_issue_description,
)
from product_bot.management.commands.bot_validation.phone_validation import process_phone_number
from product_bot.management.commands.city.contextual_handler import ContextualHandler
from product_bot.models import Patient

ANONYMOUS_REVIEW_ID = "your-id"
TEXT_ONLY_WARNING = (
    "Будь ласка, використовуйте тільки текстові повідомлення без смайликів та мультимедіа."
)


def handle_review(call, bot):
    """Prompt user to choose between anonymous and non-anonymous review.

    This function prompts the user to choose between
    leaving an anonymous or non-anonymous review.
    It sends a message with options to the user,
    allowing them to select the review type.

    Args:
        call: The callback query object that contains
            the message and related data from the user's interaction.
        bot: The bot instance used to send messages and handle interactions.
    """
    chat_id = call.message.chat.id
    markup = AnonymousButtons.anonymous_buttons()
    bot.send_message(
        chat_id,
        "Бажаєте залишити анонімний відгук?",
        reply_markup=markup,
    )


def handle_anonymous_review(call, bot: TeleBot):
    """
    Handle anonymous review submission.

    This function handles the submission of an anonymous review.
    It sends a confirmation message to the user and registers
    the next step to receive and save the anonymous review text.

    Args:
        call (CallbackQuery): The callback query object that contains
            the message and other related data.
        bot (TeleBot): The bot instance used to send messages and handle interactions.
    """
    chat_id = call.message.chat.id
    try:
        bot.send_message(chat_id, "Ваш відгук буде додано анонімно.")
    except Exception as send_error:
        bot.send_message(chat_id, "Помилка відправки повідомлення: {}".format(send_error))
        return

    try:
        bot.register_next_step_handler(
            call.message,
            lambda message: create_note_for_patient(
                "Анонімний відгук: ",
                message.text,
                ANONYMOUS_REVIEW_ID,
                chat_id,
                bot,
            ),
        )
    except Exception as register_error:
        bot.send_message(chat_id, "Помилка реєстрації наступного кроку: {}".format(register_error))


def save_anonymous_review(message, chat_id, bot):
    """Save the anonymous review in the Patient model using chat_id.

    This function handles the process of saving
    an anonymous review for a patient.
    It checks if the message contains multimedia content,
    validates the review text,
    and saves it in the Patient model using the provided chat_id.
    If the review is invalid,
    it asks the user to provide a valid text message.

    Args:
        message: The message object containing the review text to be saved.
        chat_id: The chat ID of the user providing the anonymous review.
        bot: The bot instance used to send messages and handle interactions.

    Returns:
        None
    """

    if is_multimedia_content(message):
        bot.send_message(
            chat_id,
            TEXT_ONLY_WARNING,
        )
        return

    review_text = message.text.strip()
    if not is_valid_issue_description(review_text):
        bot.send_message(
            chat_id,
            TEXT_ONLY_WARNING,
        )
        bot.register_next_step_handler(
            message,
            lambda msg: save_anonymous_review(msg, chat_id, bot),
        )
        return

    patient, created = Patient.objects.get_or_create(
        chat_id=chat_id,
        defaults={"is_anonymous": True},
    )
    patient.review = review_text
    patient.is_anonymous = True
    patient.save()

    bot.send_message(chat_id, "Дякуємо за анонімний відгук!")


def handle_review_with_info(call, bot):
    """
    Handle review with patient information,
    ask for phone number if not registered.

    This function handles the process of asking
    the user for their phone number
    if they are not registered in the system.
    It prompts the user to provide
    their phone number and registers the
    next step to process the phone number.

    Args:
        call: The callback query object containing
            information about the call
                and the associated message.
        bot: The bot instance used to send
            messages and handle interactions.
    """
    chat_id = call.message.chat.id
    bot.send_message(
        chat_id,
        "Будь ласка, вкажіть свій контактний номер телефону у форматі "
        + "+380********* або натисніть кнопку 'Поділитися номером'",
    )
    bot.register_next_step_handler(
        call.message,
        lambda msg: process_phone_number_review(msg, bot),
    )


def process_phone_number_review(message, bot, selected_city_code=None):
    """Process phone number and proceed with city or doctor selection.

    This function processes the phone number
    provided by the user, verifies if
    the phone number is registered with an
    existing patient, and proceeds with
    either the city or doctor selection.
    If the phone number is valid, the function
    will prompt the user to leave a review,
    or proceed to handle the city context.

    Args:
        message: The message object containing the user's input (phone number).
        bot: The bot instance used to send messages and handle interactions.
        selected_city_code: An optional city code for
            handling city-specific context defaults to None.

    Returns:
        None
    """
    phone_number = process_phone_number(message, bot)
    if not phone_number:
        return

    try:
        patient = Patient.objects.get(phone_number=phone_number)
    except Patient.DoesNotExist:
        markup = TechSupportButtons.create_tech_support_buttons()
        bot.send_message(
            message.chat.id,
            "Обліковий запис не знайдено. Будь ласка, пройдіть процес реєстрації.",
            reply_markup=markup,
        )
        return  # Important: stop execution if patient not found

    contextual_handler = ContextualHandler()

    if selected_city_code:
        contextual_handler.handle_city_context(
            bot,
            message.chat.id,
            selected_city_code,
            "appointment",
        )
    else:
        bot.send_message(
            message.chat.id,
            "Мобільний номер підтверджено. Будь ласка, залиште ваш відгук",
        )
        bot.register_next_step_handler(
            message,
            lambda msg: save_patient_review(msg, patient, bot),
        )


def save_patient_review(message, patient, bot):
    """Save review associated with patient's account after validation.

    This function validates the review input, checks for multimedia content,
    and saves the review to the patient's account.
    If the patient has a customer ID,
    the review is associated with the
    customer's profile; otherwise, the review is
    saved directly on the patient's record.

    Args:
        message: The message object containing
            the review text from the patient.
        patient: The patient object associated with the review.
        bot: The bot instance used to send messages and handle interactions.

    Returns:
        None
    """
    if is_multimedia_content(message):
        bot.send_message(
            message.chat.id,
            TEXT_ONLY_WARNING,
        )
        return

    review_text = message.text.strip()
    if not is_valid_issue_description(review_text):
        bot.send_message(
            message.chat.id,
            TEXT_ONLY_WARNING,
        )
        bot.register_next_step_handler(
            message,
            lambda msg: save_patient_review(msg, patient, bot),
        )
        return

    try:
        if patient.customer_id:
            bot.send_message(message.chat.id, "Ваш відгук буде збережено.")
            create_note_for_patient(
                "Відгук пацієнта: ",
                review_text,
                patient.customer_id,
                message.chat.id,
                bot,
            )
        else:
            patient.review = review_text
            patient.is_anonymous = False
            patient.save()
            bot.send_message(message.chat.id, "Дякуємо вам за ваш відгук!")
    except Exception as err:
        bot.send_message(message.chat.id, "Помилка: {}".format(err))


def setup_review_handler(bot: TeleBot):
    new_review_router = BaseTGCallRouter("new_review")
    review_anonymous_router = BaseTGCallRouter("review_anonymous")
    review_with_info_router = BaseTGCallRouter("review_with_info")

    bot.callback_query_handler(
        func=new_review_router.is_call_match_router,
    )(
        lambda call: handle_review(call, bot),
    )

    bot.callback_query_handler(
        func=review_anonymous_router.is_call_match_router,
    )(
        lambda call: handle_anonymous_review(call, bot),
    )

    bot.callback_query_handler(
        func=review_with_info_router.is_call_match_router,
    )(
        lambda call: handle_review_with_info(call, bot),
    )
