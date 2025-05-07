from product_bot.models import Patient


def fetch_patient(chat_id, bot):
    try:
        return Patient.objects.filter(chat_id=chat_id).first()
    except Exception as err:
        bot.send_message(chat_id, "Помилка при пошуку пацієнта: {}".format(err))
        return None
