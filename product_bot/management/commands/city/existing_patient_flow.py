from binotel_api_handler import create_note_for_patient
from product_bot.management.buttons.bot_buttons import TechSupportButtons


def handle_existing_patient(bot, chat_id, patient, user_input):
    markup = _try_create_buttons(bot, chat_id)
    if markup is None:
        return

    if not _try_send_message(bot, chat_id, user_input, markup):
        return

    _try_create_analysis_note(bot, chat_id, patient, user_input)


def _try_create_buttons(bot, chat_id):
    try:
        return TechSupportButtons.appointment_button_accept()
    except Exception as err:
        bot.send_message(chat_id, "Помилка при створенні кнопок: {}".format(err))
        return None


def _try_send_message(bot, chat_id, user_input, markup):
    message_text = "Ви обрали наступні аналізи: {}".format(user_input)
    try:
        bot.send_message(chat_id, message_text, reply_markup=markup)
    except Exception as err:
        bot.send_message(chat_id, "Помилка при надсиланні повідомлення: {}".format(err))
        return False
    return True


def _try_create_analysis_note(bot, chat_id, patient, user_input):
    try:
        create_note_for_patient(
            "Запит на аналіз: ",
            user_input,
            patient.customer_id,
            chat_id,
            bot,
        )
    except Exception as err:
        bot.send_message(chat_id, "Помилка при створенні нотатки: {}".format(err))
