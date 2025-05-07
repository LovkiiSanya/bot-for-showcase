from telebot import TeleBot
from telebot.types import CallbackQuery

from product_bot.management.buttons.bot_buttons import InfoButtons, PhoneButtons
from product_bot.management.registration_hanlers.phone import PhoneHandler


def handle_patient_yes(call: CallbackQuery, bot: TeleBot, handler: PhoneHandler):
    markup = PhoneButtons.share_number()
    message_text = "{} {}".format(
        "Будь ласка, вкажіть свій контактний номер телефону у форматі +380*********,",
        "або натисніть кнопку 'Поділитися номером'",
    )

    bot.send_message(call.message.chat.id, "{}".format(message_text), reply_markup=markup)
    bot.register_next_step_handler(
        call.message,
        handler.process_contact_or_manual_entry,
    )


def handle_patient_no(call: CallbackQuery, bot: TeleBot):
    markup = InfoButtons.additional_buttons()
    bot.send_message(
        call.message.chat.id,
        "Чим ми можемо Вам допомогти?",
        reply_markup=markup,
    )


def handle_help(call: CallbackQuery, bot: TeleBot):
    markup = InfoButtons.additional_buttons()
    bot.send_message(
        call.message.chat.id,
        "Чим ми можемо Вам допомогти?",
        reply_markup=markup,
    )


def show_info(call: CallbackQuery, bot: TeleBot):
    bot.send_message(call.message.chat.id, "Displaying user info...")
