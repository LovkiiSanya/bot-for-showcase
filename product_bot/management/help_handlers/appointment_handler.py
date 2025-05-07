from types import MappingProxyType

from telebot import TeleBot
from telebot.types import CallbackQuery, Message

from binotel_api_handler import create_note_for_patient
from product_bot.management.buttons.bot_buttons import CityButtons, TechSupportButtons
from product_bot.management.commands.city.contextual_handler import ContextualHandler
from product_bot.management.commands.city.router_setup import setup_context_handlers
from product_bot.management.lists.list_of_tech import registration_button
from product_bot.models import Patient, TemporaryPatient

DOCTOR_NAMES = MappingProxyType({
    "select_doctor_general": "General Practitioner",
    "select_doctor_specialist_1": "Specialist 1",
    "select_doctor_specialist_2": "Specialist 2",
    "select_doctor_specialist_3": "Specialist 3",
    "select_doctor_specialist_4": "Specialist 4",
    "select_doctor_specialist_5": "Specialist 5",
    "select_doctor_specialist_6": "Specialist 6",
    "select_doctor_specialist_7": "Specialist 7",
    "select_doctor_specialist_8": "Specialist 8",
    "select_doctor_specialist_9": "Specialist 9",
    "select_doctor_specialist_10": "Specialist 10",
    "select_doctor_specialist_11": "Specialist 11",
    "select_doctor_specialist_12": "Specialist 12",
    "select_doctor_specialist_13": "Specialist 13",
    "select_doctor_specialist_14": "Specialist 14",
})



def handle_doctor_selection(call: CallbackQuery, bot: TeleBot):
    """
    Handle the user's selection of a doctor and save it.

    This function processes the user's doctor choice. If the user is already
    registered, it saves the selection to the patient record or creates a
    note in Binotel if a customer ID exists. If the user is not registered,
    a temporary patient record is created. After saving, prompts the user
    to provide a preferred appointment date and time.

    Args:
        call (CallbackQuery): The callback query object containing the selected doctor.
        bot (TeleBot): The bot instance used to send messages and manage interactions.

    Returns:
        None
    """
    chat_id = call.message.chat.id
    doctor_code = call.data
    selected_doctor = DOCTOR_NAMES.get(doctor_code, "Невідомий лікар")

    patient = Patient.objects.filter(chat_id=chat_id).first()
    if not patient:
        return _handle_temp_patient(chat_id, selected_doctor, bot)

    if patient.customer_id:
        create_note_for_patient(
            "Вибір лікаря: ",
            selected_doctor,
            patient.customer_id,
            chat_id,
            bot,
        )
    else:
        patient.selected_doctor = selected_doctor
        patient.save()

    bot.send_message(
        chat_id,
        "Ви обрали {}. Вкажіть дату та час зручного для Вас візиту до клініки.".format(
            selected_doctor,
        ),
    )

    bot.register_next_step_handler(
        call.message,
        lambda message: process_appointment_request(message, bot),
    )


def _handle_temp_patient(chat_id: int, selected_doctor: str, bot: TeleBot):
    """
    Handle the case where a temporary patient needs to be created or updated.

    This function ensures that a TemporaryPatient record exists for the given
    chat ID. It sets the selected doctor, saves the record, and sends a message
    prompting the user to complete the registration process.

    Args:
        chat_id (int): The unique identifier for the user's chat.
        selected_doctor (str): The name of the doctor selected by the user.
        bot (TeleBot): The bot instance used to send messages to the user.
    """
    temp_patient, _ = TemporaryPatient.objects.get_or_create(chat_id=chat_id)
    temp_patient.selected_doctor = selected_doctor
    temp_patient.save()

    markup = TechSupportButtons.create_tech_support_buttons()
    markup.add(registration_button)

    bot.send_message(
        chat_id,
        "Обліковий запис не знайдено. Будь ласка, пройдіть процес реєстрації.",
        reply_markup=markup,
    )


def process_appointment_request(message: Message, bot: TeleBot):
    """
    Handles patient appointment request input.

    This function processes the patient's appointment request by storing
    the requested appointment details in the database. If the patient has
    not been registered, the bot sends a message asking the user to complete
    the registration process. If the patient is registered, the appointment
    information is stored in their record, and a confirmation message is sent.

    Args:
        message (Message): The message object containing the patient's
            chat information and the requested appointment details.
        bot (TeleBot): The bot instance used to send messages and handle
            interactions with the user.

    Returns:
        None
    """
    chat_id = message.chat.id
    patient = Patient.objects.filter(chat_id=chat_id).first()

    if not patient:
        markup = TechSupportButtons.create_tech_support_buttons()
        bot.send_message(
            chat_id,
            "Обліковий запис не знайдено. Будь ласка, пройдіть процес реєстрації.",
            reply_markup=markup,
        )
        return

    appointment_text = message.text.strip()
    if not appointment_text:
        bot.send_message(
            chat_id,
            "Треба надати інформацію про зручну для Вас дату та час.",
        )
        bot.register_next_step_handler(
            message,
            lambda msg: process_appointment_request(msg, bot),
        )
        return

    if patient.customer_id:
        create_note_for_patient(
            "Дата  на запис до лікаря: ",
            appointment_text,
            patient.customer_id,
            chat_id,
            bot,
        )
    else:
        patient.appointment_date = appointment_text
        patient.appointment_status = "pending"
        patient.save()

    bot.send_message(
        chat_id,
        "Ваш запит прийнято. Будь ласка очікуйте на підтвердження.",
        reply_markup=TechSupportButtons.appointment_button_accept(),
        parse_mode="Markdown",
    )


def dont_use_temporary_data(call: CallbackQuery, bot: TeleBot):
    city_markup = CityButtons.city_buttons("appointment")
    bot.send_message(
        call.message.chat.id,
        "Будь ласка, оберіть зручне для Вас місто",
        reply_markup=city_markup,
    )


def setup_appointment_handlers(bot: TeleBot):
    context_name = "appointment"
    contextual_handler = ContextualHandler()
    setup_context_handlers(bot, context_name, contextual_handler)

    bot.callback_query_handler(
        func=lambda call: call.data.startswith("select_doctor_"),
    )(
        lambda call: handle_doctor_selection(call, bot),
    )
    bot.callback_query_handler(
        func=lambda call: call.data == "dont_use_temporary",
    )(
        lambda call: dont_use_temporary_data(call, bot),
    )
