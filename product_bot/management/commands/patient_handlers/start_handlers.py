from functools import partial

from telebot import TeleBot, logger
from telebot.types import CallbackQuery, Message

from product_bot.management.buttons.bot_buttons import PatientButtons
from product_bot.management.commands.base_call_router import BaseTGCallRouter
from product_bot.management.registration_hanlers.phone import PhoneHandler


def handle_start(bot: TeleBot, message: Message):
    """
    Welcome message and prompt to determine patient status.

    Args:
        bot (TeleBot): The Telegram bot instance used to send messages.
        message (Message): The incoming message containing
                details about the user's chat,
                    including the chat ID and text of the message.
    """
    markup = PatientButtons.create_patient_buttons()
    bot.send_message(
        message.chat.id,
        "Ви є пацієнтом Клініки академіка Грищенка?",
        reply_markup=markup,
    )


def start_command(message: Message, bot: TeleBot):
    logger.info("Received /start command from {}".format(message.chat.id))
    handle_start(bot, message)


def handle_restart(call: CallbackQuery, bot: TeleBot):
    handle_start(bot, call.message)


def setup_restart_handler(bot: TeleBot, restart_router: BaseTGCallRouter):
    bot.callback_query_handler(func=restart_router.is_call_match_router)(
        partial(handle_restart, bot=bot),
    )


def handle_contact(message: Message, registration_handler: PhoneHandler):
    registration_handler.process_shared_contact(message)
