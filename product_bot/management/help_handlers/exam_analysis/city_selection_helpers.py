from product_bot.management.help_handlers.exam_analysis.analysis_input_handler import (
    handle_analysis_input,
)
from product_bot.models import Patient


def get_or_create_patient(chat_id, city_code, bot):
    patient = _try_get_or_create_patient(chat_id, city_code, bot)
    if not patient:
        return None

    if not patient.customer_id:
        updated = _try_update_patient_city(patient, city_code, bot)
        if not updated:
            return None

    return patient


def _try_get_or_create_patient(chat_id, city_code, bot):
    try:
        patient_data = Patient.objects.get_or_create(
            chat_id=chat_id,
            defaults={"selected_city": city_code},
        )
    except Exception as create_err:
        bot.send_message(chat_id, "Помилка при створенні пацієнта: {}".format(create_err))
        return None

    patient, _ = patient_data
    return patient


def _try_update_patient_city(patient, city_code, bot):
    try:
        patient.selected_city = city_code
    except Exception as assign_err:
        bot.send_message(patient.chat_id, "Помилка при встановленні міста: {}".format(assign_err))
        return False

    try:
        patient.save()
    except Exception as save_err:
        bot.send_message(patient.chat_id, "Помилка при збереженні міста: {}".format(save_err))
        return False

    return True


def send_city_selection_prompt(bot, chat_id, city_code):
    try:
        bot.send_message(
            chat_id,
            "Ви обрали місто: {}. Введіть текстом, який аналіз Вам потрібен:".format(city_code),
        )
    except Exception as err:
        bot.send_message(chat_id, "Помилка при надсиланні повідомлення: {}".format(err))
        return

    try:
        bot.register_next_step_handler_by_chat_id(
            chat_id,
            lambda message: handle_analysis_input(message, bot),
        )
    except Exception as err_reg:
        bot.send_message(chat_id, "Помилка при реєстрації обробника: {}".format(err_reg))
