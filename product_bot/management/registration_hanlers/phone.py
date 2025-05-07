from telebot import TeleBot
from telebot.types import Message

from product_bot.management.buttons.bot_buttons import InfoButtons, PatientButtons
from product_bot.management.commands.bot_validation.phone_validation import (
    normalize_phone_number,
    validate_int_phone_number,
    validate_ukr_phone_number,
)
from product_bot.management.help_handlers.patient_registration_handler import get_patient_by_phone
from product_bot.management.registration_hanlers.email import EmailHandler


class PhoneHandler:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def handle(self, message: Message, first_name: str, last_name: str):
        """Handle phone number input.

        Validates the phone number input from the user. If the input is invalid,
        prompts the user to re-enter the phone number.
        If valid, proceeds to request the user's email.

        Args:
            message (Message): The Telegram message object
                containing the phone number or contact.
            first_name (str): The user's first name.
            last_name (str): The user's last name."""
        if message.contact:
            phone_number = message.contact.phone_number
        else:
            phone_number = message.text.strip() if message.text else None

        if not phone_number:
            self.bot.send_message(
                message.chat.id,
                "Телефонний номер не знайдено. Будь ласка, спробуйте ще раз.",
            )
            self.bot.register_next_step_handler(
                message,
                lambda msg: self.handle(
                    msg,
                    first_name,
                    last_name,
                ),
            )
            return

        phone_number = normalize_phone_number(phone_number)

        if not (validate_ukr_phone_number(phone_number) or validate_int_phone_number(phone_number)):
            self.bot.send_message(
                message.chat.id,
                "Будь ласка, вкажіть свій контактний номер телефону "
                + "у форматі +380********* або натисніть кнопку "
                + "'Поділитися номером'",
            )
            self.bot.register_next_step_handler(
                message,
                lambda msg: self.handle(
                    msg,
                    first_name,
                    last_name,
                ),
            )
            return

        self.bot.send_message(message.chat.id, "Введіть вашу електронну пошту:")
        self.bot.register_next_step_handler(
            message,
            lambda msg: EmailHandler(self.bot).handle(
                msg,
                first_name,
                last_name,
                phone_number,
            ),
        )

    def process_contact_or_manual_entry(self, message: Message):
        """
        Process the phone number provided manually or shared as a contact.

        This method handles user input where the phone number is either
        typed manually or shared through Telegram's contact sharing feature.
        It validates the phone number format, and based on the existence
        of a corresponding patient record, directs the user accordingly.

        Args:
            message (Message): The Telegram message object containing
                the text or contact data from the user.

        Returns:
            None
        """
        if message.contact:
            phone_number = message.contact.phone_number
        else:
            phone_number = message.text.strip() if message.text else None

        if not phone_number:
            self.bot.send_message(
                message.chat.id,
                "Телефонний номер не знайдено. Будь ласка, спробуйте ще раз.",
            )
            self.bot.register_next_step_handler(
                message,
                self.process_contact_or_manual_entry,
            )
            return

        phone_number = normalize_phone_number(phone_number)

        if not (validate_ukr_phone_number(phone_number) or validate_int_phone_number(phone_number)):
            self.bot.send_message(
                message.chat.id,
                "Будь ласка, вкажіть свій контактний номер телефону "
                + "у форматі +380********* або натисніть кнопку "
                + "'Поділитися номером'",
            )
            self.bot.register_next_step_handler(
                message,
                self.process_contact_or_manual_entry,
            )
            return

        patient = get_patient_by_phone(phone_number)

        if patient:
            self.handle_existing_patient(message.chat.id, patient)
        else:
            self.handle_new_patient(message.chat.id)

    def process_shared_contact(self, message: Message):
        """
        Process a shared phone number directly from the contact.

        This method extracts the phone number from a shared Telegram contact
        and proceeds with the patient lookup or registration process.

        Args:
            message (Message): The Telegram message object containing the contact.

        Returns:
            None
        """
        if not message.contact or not message.contact.phone_number:
            self.bot.send_message(
                message.chat.id,
                "Будь ласка, спробуйте ще раз.",
            )
            return

        phone_number = normalize_phone_number(message.contact.phone_number.strip())
        self._process_phone_number(message.chat.id, phone_number)

    def handle_existing_patient(self, chat_id: int, patient):
        """
        Handle the case where a patient is found in the database.

        Sends a welcome message to the returning patient and displays
        available options.

        Args:
            chat_id (int): The chat ID of the user.
            patient (Patient): The patient object retrieved from the database.
        """
        self.bot.send_message(
            chat_id,
            "Вітаємо знову, {}!".format(patient.first_name),
            reply_markup=InfoButtons.create_info_buttons(),
        )

    def handle_new_patient(self, chat_id: int):
        """
        Handle the case where no patient is found.

        Sends a message to the user indicating that no patient record
        was found and provides options to retry or re-register.

        Args:
            chat_id (int): The chat ID of the user to whom the message is sent.
        """
        markup = PatientButtons.create_not_found_patient_buttons()
        self.bot.send_message(
            chat_id,
            "У нас немає таких даних. "
            + "Будь ласка, перевірте введені дані або пройдіть повторну реєстрацію.",
            reply_markup=markup,
        )

    def _process_phone_number(self, chat_id: int, phone_number: str):
        """Common handler for phone number processing.

        This method handles the phone number input by checking if the phone number
        belongs to an existing patient or a new patient.
        It processes the input accordingly.

        Args:
            chat_id (int): The unique ID of the user's chat.
            phone_number (str): The phone number provided by the user."""
        if not (validate_ukr_phone_number(phone_number) or validate_int_phone_number(phone_number)):
            self.bot.send_message(
                chat_id,
                "Неправильний формат номера. Використайте +380********* або поділіться номером.",
            )
            return

        patient = get_patient_by_phone(phone_number)

        if patient:
            self.handle_existing_patient(chat_id, patient)
        else:
            self.handle_new_patient(chat_id)
