from telebot import TeleBot
from telebot.types import Message

from product_bot.management.commands.bot_validation.email_validation import is_valid_name
from product_bot.management.registration_hanlers.phone import PhoneHandler


class NameHandler:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def ask_first_name(self, message: Message):
        """Handle first name input.

        Validates the first name input from the user. If the input is invalid,
        prompts the user to re-enter their first name.
        If valid, proceeds to request the user's last name.

        Args:
            message (Message): The Telegram message
                object containing the first name."""
        first_name = message.text.strip() if message.text else None
        if not first_name or not is_valid_name(first_name):
            self.bot.send_message(
                message.chat.id,
                "Ім'я не може містити спеціальні символи. Будь ласка спробуйте ще раз.",
            )
            self.bot.register_next_step_handler(message, self.ask_first_name)
            return

        self.bot.send_message(message.chat.id, "Вкажіть Ваше прізвище")
        self.bot.register_next_step_handler(
            message,
            lambda msg: self.ask_last_name(
                msg,
                first_name,
            ),
        )

    def ask_last_name(self, message: Message, first_name: str):
        """Handle last name input.

        Validates the last name input from the user. If the input is invalid,
        prompts the user to re-enter the last name. If valid, proceeds to request
        the user's phone number.

        Args:
            message (Message): The Telegram message
                object containing the last name.
            first_name (str): The user's first name."""

        last_name = message.text.strip() if message.text else None
        if not last_name or not is_valid_name(last_name):
            self.bot.send_message(
                message.chat.id,
                "Прізвище не може містити спеціальні символи. Будь ласка спробуйте ще раз.",
            )
            self.bot.register_next_step_handler(
                message,
                lambda msg: self.ask_last_name(msg, first_name),
            )
            return

        self.bot.send_message(
            message.chat.id,
            "Будь ласка, вкажіть свій контактний номер телефону у "
            + "форматі +380********* або натисніть кнопку "
            + "'Поділитися номером'",
        )
        self.bot.register_next_step_handler(
            message,
            lambda msg: PhoneHandler(self.bot).handle(
                msg,
                first_name,
                last_name,
            ),
        )
