from binotel_api_handler import create_note_for_patient
from product_bot.management.buttons.bot_buttons import TechSupportButtons


def create_city_note(patient, city_name, chat_id, bot):
    try:
        create_note_for_patient(
            "Вибір міста для лікаря: ",
            city_name,
            patient.customer_id,
            chat_id,
            bot,
        )
    except Exception as err:
        bot.send_message(chat_id, "Помилка при створенні нотатки: {}".format(err))
        return False

    return True


def send_analysis_saved_message(bot, chat_id, user_input):
    try:
        markup = TechSupportButtons.appointment_button_accept()
    except Exception as create_err:
        bot.send_message(chat_id, "Помилка при створенні кнопок: {}".format(create_err))
        return

    try:
        bot.send_message(
            chat_id,
            "Ви обрали наступні аналізи: {}".format(user_input),
            reply_markup=markup,
        )
    except Exception as err:
        bot.send_message(chat_id, "Помилка при надсиланні повідомлення: {}".format(err))
