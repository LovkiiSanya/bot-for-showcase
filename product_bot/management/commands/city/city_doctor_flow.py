from product_bot.management.buttons.doctor_buttons import DoctorButtons
from product_bot.management.commands.city.city_analysis_flow import create_city_note
from product_bot.management.commands.city.city_patient_update import update_patient_city
from product_bot.management.commands.city.fetch_patient import fetch_patient


def show_doctors(bot, chat_id, city_code, city_name):
    """
    Prompts the user to select a doctor after choosing a city.

    Args:
        bot (TeleBot): The bot instance used to send messages to the user.
        chat_id (int): The unique identifier for the user's chat.
        city_code (str): The code representing the selected city.
        city_name (str): The name of the selected city.
    """
    patient = fetch_patient(chat_id, bot)
    if patient is None:
        return

    if patient and patient.customer_id:
        if not create_city_note(patient, city_name, chat_id, bot):
            return
    elif not update_patient_city(chat_id, city_name, bot):
        return

    markup = _create_doctor_buttons(city_code, chat_id, bot)
    if markup:
        _send_doctor_choice_message(bot, chat_id, city_name, markup)


def _create_doctor_buttons(city_code, chat_id, bot):
    try:
        return DoctorButtons.get_doctors_buttons(city_code)
    except Exception as err:
        bot.send_message(chat_id, "Помилка при створенні кнопок докторів: {}".format(err))
        return None


def _send_doctor_choice_message(bot, chat_id, city_name, markup):
    try:
        bot.send_message(
            chat_id,
            "Ви обрали м.{}. Оберіть, будь ласка, доктора:".format(city_name),
            reply_markup=markup,
        )
    except Exception as err:
        bot.send_message(chat_id, "Помилка при надсиланні повідомлення: {}".format(err))
