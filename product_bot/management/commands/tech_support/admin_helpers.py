from binotel_api_handler import binotel, create_note_for_patient
from product_bot.management.buttons.bot_buttons import TechSupportButtons
from product_bot.management.commands.tech_support.constants import tags
from product_bot.management.commands.tech_support.request_creation import (
    process_phone_and_create_admin_note,
)
from product_bot.models import Patient


def fetch_patient(chat_id, bot):
    try:
        return Patient.objects.filter(chat_id=chat_id).first()
    except Exception as err:
        bot.send_message(chat_id, "Помилка при пошуку пацієнта: {}".format(err))
        return None


def handle_registered_patient(bot, chat_id, patient, username):
    send_admin_request(bot, chat_id)
    create_admin_note(bot, chat_id, patient, username)
    update_patient_labels(bot, chat_id, patient)


def send_admin_request(bot, chat_id):
    markup = TechSupportButtons.appointment_button_accept()
    try:
        bot.send_message(
            chat_id,
            "Ваш запит передано адміністратору. Будь ласка, очікуйте відповіді.",
            reply_markup=markup,
        )
    except Exception as err:
        bot.send_message(chat_id, "Помилка при надсиланні повідомлення: {}".format(err))


def create_admin_note(bot, chat_id, patient, username):
    try:
        create_note_for_patient(
            "Запит на підключення адміністратора від {}".format(username),
            patient.phone_number,
            patient.customer_id,
            chat_id,
            bot,
        )
    except Exception as err:
        bot.send_message(chat_id, "Помилка при створенні нотатки: {}".format(err))


def update_patient_labels(bot, chat_id, patient):
    try:
        binotel.update_customer_labels(
            customer_id=patient.customer_id,
            email=patient.email,
            tags=tags,
        )
    except Exception as err:
        bot.send_message(chat_id, "Помилка при оновленні міток Binotel: {}".format(err))


def request_phone_number(bot, call):
    chat_id = call.message.chat.id
    try:
        bot.send_message(
            chat_id,
            "{}".format(
                "Будь ласка, вкажіть свій контактний номер телефону "
                + "у форматі +380********* або натисніть кнопку "
                + "'Поділитися номером'",
            ),
        )
    except Exception as err_send:
        bot.send_message(
            chat_id, "Помилка при надсиланні запиту на введення номера: {}".format(err_send),
        )
        return

    try:
        bot.register_next_step_handler(
            call.message,
            lambda msg: process_phone_and_create_admin_note(msg, bot),
        )
    except Exception as err:
        bot.send_message(chat_id, "Помилка при реєстрації обробника номера: {}".format(err))
