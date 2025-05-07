from product_bot.management.buttons.bot_buttons import TechSupportButtons
from product_bot.management.commands.tech_support.admin_helpers import (
    fetch_patient,
    handle_registered_patient,
    request_phone_number,
)


def acknowledge_user(message, bot):
    message_text = (
        "Дякуємо за звернення. Воно зараз в обробці. Ми зв'яжемося з Вами якнайшвидше."
    )
    bot.send_message(message.chat.id, "{}".format(message_text))
    markup = TechSupportButtons.create_tech_support_buttons()
    bot.send_message(
        message.chat.id,
        "Чим ще можемо допомогти?",
        reply_markup=markup,
    )


def join_administrator(call, bot):
    chat_id = call.message.chat.id
    username = "@{}".format(call.from_user.username) if call.from_user.username else "Без імені"

    patient = fetch_patient(chat_id, bot)

    if patient and patient.customer_id and patient.phone_number:
        handle_registered_patient(bot, chat_id, patient, username)
    else:
        request_phone_number(bot, call)
