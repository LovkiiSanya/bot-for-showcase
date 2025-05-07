from telebot import TeleBot
from telebot.types import Message

from product_bot.management.commands.bot_validation.email_validation import validate_email
from product_bot.management.registration_hanlers.birthdate import BirthdateHandler, RegistrationData


class EmailHandler:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def handle(
        self,
        message: Message,
        first_name: str,
        last_name: str,
        phone_number: str,
    ):
        """Handle email input.

        Validates the email input from the user. If the input is invalid,
        prompts the user to re-enter the email. If valid, proceeds to request
        the user's birthdate.

        Args:
            message (Message): The Telegram message object containing the email.
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            phone_number (str): The user's phone number."""
        email = message.text.strip() if message.text else None

        if not email or not validate_email(email):
            self.bot.send_message(
                message.chat.id,
                "Недійсний формат електронної пошти. "
                + "Введіть дійсну електронну адресу "
                + "(наприклад, test@gmail.com).",
            )
            self.bot.register_next_step_handler(
                message,
                lambda msg: self.handle(
                    msg,
                    first_name,
                    last_name,
                    phone_number,
                ),
            )
            return

        self.bot.send_message(
            message.chat.id,
            "Будь ласка, введіть свою дату народження (формат: дд/мм/рррр).",
        )

        self.bot.register_next_step_handler_by_chat_id(
            message.chat.id,
            lambda msg: BirthdateHandler(self.bot).handle(
                RegistrationData(
                    message=msg,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    email=email,
                ),
            ),
        )
