from binotel_api_handler import create_note_for_patient


def handle_existing_patient(call, bot, patient, chat_id):
    try:
        bot.send_message(
            chat_id,
            "Ви обрали місто: {}. Введіть текстом, який аналіз Вам потрібен:".format(call.data),
        )
    except Exception as send_err:
        bot.send_message(chat_id, "Помилка при надсиланні повідомлення: {}".format(send_err))
        return

    try:
        bot.register_next_step_handler(
            call.message,
            lambda message: create_note_for_patient(
                "Запит на аналіз: ",
                message.text,
                patient.customer_id,
                chat_id,
                bot,
            ),
        )
    except Exception as register_err:
        bot.send_message(chat_id, "Помилка при реєстрації обробника: {}".format(register_err))
