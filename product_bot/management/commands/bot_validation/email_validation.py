import re
from datetime import datetime


def validate_email(email):
    # Simple regex for validating emails
    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+$"
    return re.match(pattern, email) is not None


def validate_birthdate(birthdate_str):
    try:
        datetime.strptime(birthdate_str, "%d/%m/%Y")
    except ValueError:
        return False
    return True


def is_valid_name(name):
    # Allow letters (including accented), hyphens, and apostrophes
    return bool(re.match(r"^[\w'’\-]+$", name))
