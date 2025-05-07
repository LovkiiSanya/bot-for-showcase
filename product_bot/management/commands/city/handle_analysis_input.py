from product_bot.management.commands.city.existing_patient_flow import handle_existing_patient
from product_bot.management.commands.city.fetch_patient import fetch_patient
from product_bot.management.commands.city.new_patient_flow import handle_new_patient


def handle_analysis_input(message, bot):
    """
    Handle the patient's input for the requested analysis.

    This function processes the patient's free-text input regarding their
    requested medical analysis. It first checks if the patient exists
    and has a customer ID. If so, it updates the existing patient record
    with the analysis information. If the patient does not exist or lacks
    a customer ID, a new record is created or updated accordingly.

    Args:
        message (Message): The Telegram message object containing the analysis input.
        bot (TeleBot): The bot instance used to send messages and handle user interactions.

    Returns:
        None
    """
    chat_id = message.chat.id
    user_input = message.text.strip()

    patient = fetch_patient(chat_id, bot)
    if not patient:
        return

    if patient.customer_id:
        handle_existing_patient(bot, chat_id, patient, user_input)
    else:
        handle_new_patient(bot, chat_id, user_input)
