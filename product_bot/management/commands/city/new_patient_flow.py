from product_bot.management.commands.city.city_analysis_flow import send_analysis_saved_message
from product_bot.management.commands.city.city_patient_update import update_patient_analysis
from product_bot.models import Patient


def handle_new_patient(bot, chat_id, user_input):
    patient = _create_or_fetch_patient(chat_id, user_input, bot)
    if not patient:
        return

    if patient.customer_id is None:
        if not update_patient_analysis(patient, user_input, bot, chat_id):
            return

    send_analysis_saved_message(bot, chat_id, user_input)


def _create_or_fetch_patient(chat_id, user_input, bot):
    try:
        patient, _ = Patient.objects.get_or_create(
            chat_id=chat_id,
            defaults={"requested_analysis": user_input},
        )
    except Exception as err:
        bot.send_message(chat_id, "Помилка при створенні нового пацієнта: {}".format(err))
        return None

    return patient
