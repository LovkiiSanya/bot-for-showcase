import os
from typing import Optional

from product_bot.models import Patient

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

OPEN_REQUEST_TAG = "your-id"


def get_patient_by_phone(phone_number: str) -> Optional[Patient]:
    """Retrieve the patient by phone number.

    This function queries the database to find a patient with the given
    phone number and returns the first matching patient, or None if no
    patient is found.

    Args:
        phone_number (str): The phone number of the patient to retrieve.

    Returns:
        Optional[Patient]: The patient with the given phone number, or None
        if no such patient exists."""
    return Patient.objects.filter(phone_number=phone_number).first()
