from product_bot.models import Patient, TemporaryPatient


def update_selected_city(chat_id, city_name):
    """
    Updates the selected city for a Patient or TemporaryPatient.
    Handles both models consistently to maintain data integrity.

    Args:
        chat_id (int): The unique identifier for the user's chat.
        city_name (str): The name of the selected city to be updated.
    """
    # Check for an existing Patient record
    patient = Patient.objects.filter(chat_id=chat_id).first()

    if patient:
        patient.selected_city = city_name
        patient.save()
    else:
        # Fall back to TemporaryPatient if Patient does not exist
        temp_patient, _ = TemporaryPatient.objects.get_or_create(
            chat_id=chat_id,
        )
        temp_patient.selected_city = city_name
        temp_patient.save()


def update_patient_city(chat_id, city_name, bot):
    try:
        update_selected_city(chat_id, city_name)
    except Exception as err:
        bot.send_message(chat_id, "Помилка при оновленні міста: {}".format(err))
        return False
    return True


def update_patient_analysis(patient, user_input, bot, chat_id):
    if not _try_assign_field(patient, "requested_analysis", user_input, bot, chat_id):
        return False

    if not _try_assign_field(patient, "state", "analysis_received", bot, chat_id):
        return False

    return _try_save_patient(patient, bot, chat_id)


def _try_assign_field(patient, field_name, value, bot, chat_id):
    try:
        setattr(patient, field_name, value)
    except Exception as err:
        bot.send_message(chat_id, "Помилка при оновленні '{}': {}".format(field_name, err))
        return False
    return True


def _try_save_patient(patient, bot, chat_id):
    try:
        patient.save()
    except Exception as err:
        bot.send_message(chat_id, "Помилка при збереженні пацієнта: {}".format(err))
        return False
    return True
