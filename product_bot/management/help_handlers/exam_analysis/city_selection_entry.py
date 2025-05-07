from telebot import TeleBot

from product_bot.management.help_handlers.exam_analysis.city_selection_helpers import (
    get_or_create_patient,
    send_city_selection_prompt,
)
from product_bot.management.help_handlers.exam_analysis.city_selection_logic import (
    handle_existing_patient,
)
from product_bot.models import Patient


def handle_city_selection(call, bot: TeleBot, contextual_handler):
    chat_id = call.message.chat.id
    city_code = call.data

    patient = fetch_patient(chat_id, bot)
    if not patient:
        return

    if patient.customer_id:
        handle_existing_patient(call, bot, patient, chat_id)
    else:
        patient = get_or_create_patient(chat_id, city_code, bot)
        if patient:
            send_city_selection_prompt(bot, chat_id, city_code)


def fetch_patient(chat_id, bot):
    try:
        return Patient.objects.filter(chat_id=chat_id).first()
    except Exception as err:
        bot.send_message(chat_id, "Помилка при пошуку пацієнта: {}".format(err))
        return None
