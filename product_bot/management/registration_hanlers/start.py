from telebot import TeleBot
from telebot.types import Message

from product_bot.management.registration_hanlers.name import NameHandler


class StartRegistrationHandler:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def start(self, message: Message):
        """Initiate the registration process.

        Sends a message to prompt the user to provide their first name and
        registers the next step to handle the first name input.

        Args:
            message (Message): The Telegram message
                object initiating the registration process."""
        self.bot.send_message(message.chat.id, "Вкажіть Ваше ім'я")
        self.bot.register_next_step_handler(message, NameHandler(self.bot).ask_first_name)
