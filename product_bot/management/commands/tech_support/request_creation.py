from binotel_api_handler import binotel, create_note_for_patient
from product_bot.management.buttons.bot_buttons import TechSupportButtons
from product_bot.management.commands.tech_support.constants import (
    ADMIN_JOIN,
    UNAUTHORIZED_EMAIL_admin,
    tags,
)
from product_bot.models import TechSupportRequest


def create_new_request_chatback(chat_id, issue_description):
    TechSupportRequest.objects.create(
        chat_id=chat_id,
        issue_description=issue_description,
    )


def process_phone_and_create_admin_note(message, bot):
    chat_id = message.chat.id
    if message.from_user.username:
        username = "@{}".format(message.from_user.username)
    else:
        username = "Без імені"

    phone_number = message.text.strip() if message.text else None
    if message.contact:
        phone_number = message.contact.phone_number

    if not phone_number:
        bot.send_message(
            chat_id,
            "Телефонний номер не знайдено. Будь ласка, спробуйте ще раз.",
        )
        bot.register_next_step_handler(
            message,
            lambda msg: process_phone_and_create_admin_note(msg, bot),
        )
        return

    create_note_for_patient(
        "Запит на підключення адміністратора від {} (неавторизований клієнт)".format(username),
        phone_number,
        ADMIN_JOIN,
        chat_id,
        bot,
    )
    binotel.update_customer_labels(
        customer_id=ADMIN_JOIN,
        email=UNAUTHORIZED_EMAIL_admin,
        tags=tags,
    )

    markup = TechSupportButtons.appointment_button_accept()
    bot.send_message(
        chat_id,
        "Ваш запит передано адміністратору. Будь ласка, очікуйте відповіді.",
        reply_markup=markup,
    )
