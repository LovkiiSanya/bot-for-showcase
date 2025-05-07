from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from django.db import transaction
from telebot import TeleBot
from telebot.types import Message

from binotel_api_handler import binotel
from product_bot.management.buttons.bot_buttons import InfoButtons
from product_bot.management.commands.bot_validation.email_validation import validate_birthdate
from product_bot.management.help_handlers.patient_registration_handler import OPEN_REQUEST_TAG
from product_bot.models import Patient


@dataclass
class RegistrationData:
    message: Message
    first_name: str
    last_name: str
    phone_number: str
    email: str


@dataclass
class CustomerData:
    patient: Optional[Patient]
    first_name: str
    last_name: str
    phone_number: str
    email: str
    birthdate: date
    message: Message


class BirthdateHandler:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def handle(self, registration_data: RegistrationData) -> None:
        """
        Handle the birthdate input during the registration process.

        This method validates the birthdate entered by the user. If the birthdate is invalid,
        it prompts the user to re-enter it in the correct format (dd/mm/yyyy).
        If the birthdate is valid, it proceeds to register the patient
        by creating a new record with the provided information.

        Args:
            registration_data (RegistrationData):
                An object containing the user's registration details including
                message, first name, last name, phone number, and email.

        Returns:
            None
        """
        birthdate_str = (
            registration_data.message.text.strip() if registration_data.message.text else None
        )

        if not birthdate_str or not validate_birthdate(birthdate_str):
            self.bot.send_message(
                registration_data.message.chat.id,
                "Невірний формат. Будь ласка, введіть свою дату народження (формат: дд/мм/рррр).",
            )
            self.bot.register_next_step_handler(
                registration_data.message,
                lambda msg: self.handle(registration_data),
            )
            return

        try:
            birthdate = datetime.strptime(birthdate_str, "%d/%m/%Y").date()
        except ValueError:
            self.bot.send_message(
                registration_data.message.chat.id, "Помилка: Невірний формат дати.",
            )
            return

        self._register_patient(
            CustomerData(
                patient=None,
                first_name=registration_data.first_name,
                last_name=registration_data.last_name,
                phone_number=registration_data.phone_number,
                email=registration_data.email,
                birthdate=birthdate,
                message=registration_data.message,
            ),
        )

    def _register_patient(self, data: CustomerData) -> None:
        with transaction.atomic():
            patient, created = Patient.objects.get_or_create(
                first_name=data.first_name,
                last_name=data.last_name,
                phone_number=data.phone_number,
                email=data.email,
                defaults={
                    "birthdate": data.birthdate,
                    "chat_id": data.message.chat.id,
                },
            )

            if not created:
                patient.birthdate = data.birthdate
                patient.save()

            data.patient = patient  # assign newly created patient into data
            self._create_binotel_customer(data)

        self.bot.send_message(
            data.message.chat.id,
            "Дякуємо, інформацію збережено",
            reply_markup=InfoButtons.create_info_buttons(),
        )

    def _create_binotel_customer(self, data: CustomerData):
        customer_id = self._create_client_with_tag(data)

        if not customer_id:
            return

        data.patient.customer_id = customer_id
        data.patient.save()

        self._add_email_note(customer_id, data)
        self._add_birthdate_note(customer_id, data)

    def _create_client_with_tag(self, data: CustomerData) -> str | None:
        try:
            return binotel.create_client_with_tag(
                name="{} {}".format(data.first_name, data.last_name),
                phone=data.phone_number[3:],
                tag_id=OPEN_REQUEST_TAG,
                tag_name="Відкрита заявка",
            )["id"]
        except Exception as err:
            self.bot.send_message(
                data.message.chat.id,
                "Помилка створення клієнта: {}".format(err),
            )
            return None

    def _add_email_note(self, customer_id: str, data: CustomerData) -> None:
        try:
            binotel.create_note(
                customer_id=str(customer_id),
                comment="Пошта клієнта: {}".format(data.email),
            )
        except Exception as err:
            self.bot.send_message(
                data.message.chat.id,
                "Помилка додавання пошти: {}".format(err),
            )

    def _add_birthdate_note(self, customer_id: str, data: CustomerData) -> None:
        try:
            binotel.create_note(
                customer_id=str(customer_id),
                comment="Дата народження: {}".format(data.birthdate),
            )
        except Exception as err:
            self.bot.send_message(
                data.message.chat.id,
                "Помилка додавання дати народження: {}".format(err),
            )
