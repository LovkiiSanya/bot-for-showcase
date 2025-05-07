from telebot import TeleBot

from binotel_api_handler import create_note_for_patient
from product_bot.models import Patient


def handle_analysis_input(message, bot: TeleBot):
    chat_id = message.chat.id
    requested_analysis = message.text.strip()

    patient = _fetch_patient(chat_id, bot)
    if not patient:
        return

    if patient.customer_id:
        _process_existing_patient(patient, requested_analysis, chat_id, bot)
    else:
        _process_new_patient(chat_id, requested_analysis, bot)


def _fetch_patient(chat_id, bot):
    try:
        return Patient.objects.filter(chat_id=chat_id).first()
    except Exception as err:
        bot.send_message(chat_id, "Помилка при пошуку пацієнта: {}".format(err))
        return None


def _process_existing_patient(patient, requested_analysis, chat_id, bot):
    try:
        create_note_for_patient(
            "Запит на аналіз: ",
            requested_analysis,
            patient.customer_id,
            chat_id,
            bot,
        )
    except Exception as err_create:
        bot.send_message(chat_id, "Помилка при створенні нотатки: {}".format(err_create))

    patient.state = None
    try:
        patient.save()
    except Exception as err:
        bot.send_message(chat_id, "Помилка при збереженні стану пацієнта: {}".format(err))
        return

    _send_success_message(chat_id, requested_analysis, bot)


def _process_new_patient(chat_id, requested_analysis, bot):
    try:
        patient, created = Patient.objects.get_or_create(
            chat_id=chat_id,
            defaults={"requested_analysis": requested_analysis},
        )
    except Exception as err:
        bot.send_message(chat_id, "Помилка при створенні нового пацієнта: {}".format(err))
        return

    if not created:
        patient.requested_analysis = requested_analysis
        patient.state = None
        try:
            patient.save()
        except Exception as err_save:
            bot.send_message(chat_id, "Помилка при збереженні пацієнта: {}".format(err_save))
            return

    _send_success_message(chat_id, requested_analysis, bot)


def _send_success_message(chat_id, requested_analysis, bot):
    try:
        bot.send_message(
            chat_id,
            "Ваш запит на аналіз '{}' збережено. Дякуємо!".format(requested_analysis),
        )
    except Exception as err:
        bot.send_message(chat_id, "Помилка при надсиланні повідомлення: {}".format(err))
