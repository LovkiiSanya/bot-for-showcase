from binotel_api_handler import create_note_for_patient
from product_bot.management.buttons.bot_buttons import (
    AnonymousButtons,
    CityButtons,
    TechSupportButtons,
)
from product_bot.management.commands.city.city_patient_update import update_selected_city
from product_bot.management.commands.city.constants import CITY_MESSAGES
from product_bot.management.commands.city.handle_analysis_input import handle_analysis_input
from product_bot.management.lists.list_of_tech import registration_button
from product_bot.models import Patient, TemporaryPatient


def handle_context(call, bot, context_name, handler):
    patient = Patient.objects.filter(chat_id=call.message.chat.id).first()
    if patient:
        city_markup = CityButtons.city_buttons(context_name)
        bot.send_message(
            call.message.chat.id,
            "Будь ласка, оберіть зручне для Вас місто",
            reply_markup=city_markup,
        )
    else:
        temp_patient = TemporaryPatient.objects.filter(
            chat_id=call.message.chat.id,
        ).first()
        if temp_patient:
            markup = AnonymousButtons.temporary_button()
            bot.send_message(
                call.message.chat.id,
                "Ви не зареєстровані. "
                + "Хотіли б ви використати збережені дані або почати заново?",
                reply_markup=markup,
            )
        else:
            markup = TechSupportButtons.create_tech_support_buttons()
            markup.add(registration_button)
            bot.send_message(
                call.message.chat.id,
                "Ви не зареєстровані. Будь ласка, пройдіть процес реєстрації.",
                reply_markup=markup,
            )


def handle_city_selection(call, bot, handler):
    try:
        city_code, context = call.data.split("_", 1)
    except ValueError:
        bot.send_message(call.message.chat.id, "Сталася помилка")
        return

    city_message = CITY_MESSAGES.get(city_code, "Сталася помилка")
    bot.send_message(call.message.chat.id, city_message)
    handler.handle_city_context(
        bot,
        call.message.chat.id,
        city_code,
        context,
    )


def prompt_analysis_input(bot, chat_id, city_code, city_name):
    """
    Prompts the user to enter their desired analysis in free-text form.

    This function updates the patient's state to indicate they are waiting
    for analysis input and sends a message asking them to specify the analysis
    they need.

    Args:
        bot (TeleBot): The bot instance used to send messages to the user.
        chat_id (int): The unique identifier for the user's chat.
        city_code (str): The code representing the selected city.
        city_name (str): The name of the selected city.
    """
    # Update the patient's state to waiting for analysis input
    patient = Patient.objects.filter(chat_id=chat_id).first()
    if patient and patient.customer_id:
        create_note_for_patient(
            "Вибір міста для аналізу: ",
            city_name,
            patient.customer_id,
            chat_id,
            bot,
        )
    else:
        update_selected_city(chat_id, city_name)
    patient.state = "waiting_for_analysis_input"
    patient.save()

    update_selected_city(chat_id, city_name)
    bot.send_message(
        chat_id,
        "Ви обрали м. {}. Вкажіть, який аналіз потрібен".format(city_name),
    )

    bot.register_next_step_handler_by_chat_id(
        chat_id,
        lambda message: handle_analysis_input(message, bot),
    )
