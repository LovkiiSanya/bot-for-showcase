import phonenumbers

LENGTH_PHONE_NUMBER = 13


def normalize_phone_number(phone_number: str) -> str:
    """
    Normalize phone number by ensuring it has a '+' prefix.
    This method also removes spaces and non-digit characters.

    Args:
        phone_number (str): The phone number to normalize, which may contain
                             spaces or non-digit characters.

    Returns:
        str: The normalized phone number with a '+' prefix and only digits.
    """
    # Remove all non-digit characters except for '+'
    cleaned_chars = []
    for char in phone_number:
        if char.isdigit() or char == "+":
            cleaned_chars.append(char)

    phone_number = "".join(cleaned_chars)

    if not phone_number.startswith("+"):
        phone_number = "+{}".format(phone_number)

    return phone_number


def validate_ukr_phone_number(phone_number: str) -> bool:
    """
    Basic check for Ukrainian numbers
    (+380 format, 13 digits with or without '+').

    Args:
        phone_number (str): The phone number to validate,
            in a format like +380********* or 380*********.

    Returns:
        bool: True if the phone number is valid according
        to Ukrainian phone number rules, False otherwise.
    """
    phone_number = normalize_phone_number(phone_number)
    try:
        parsed_number = phonenumbers.parse(phone_number, "UA")
    except phonenumbers.NumberParseException:
        return False

    return phonenumbers.is_valid_number(parsed_number) and len(phone_number) == LENGTH_PHONE_NUMBER


def validate_int_phone_number(phone_number: str) -> bool:
    """
    Validate international phone number format.
    Handles phone numbers from any country with country code.

    Args:
        phone_number (str): The phone number
            to validate in international format.

    Returns:
        bool: True if the phone number is valid, otherwise False.
    """
    phone_number = normalize_phone_number(phone_number)
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
    except phonenumbers.NumberParseException:
        return False

    return phonenumbers.is_valid_number(parsed_number)


def process_phone_number(message, bot):
    """
    Process the phone number from the message and return it
    if valid, otherwise send an error.

    Args:
        message (Message): The message object containing the phone number.
        bot (TeleBot): The instance of the bot to send messages with.

    Returns:
        str or None: The valid phone number
        if the input is valid, otherwise None.
    """

    # Extract phone number from contact or plain text
    phone_number = message.contact.phone_number if message.contact else message.text.strip()

    # If no phone number is provided, prompt the user to provide it again
    if not phone_number:
        bot.send_message(
            message.chat.id,
            "Не можемо зчитати Ваш номер телефону. "
            + "Будь ласка, повторіть введення або натисніть "
            + 'на кнопку "поділитися номером".',
        )
        return None

    phone_number = normalize_phone_number(phone_number)

    # Validate phone number format (Ukrainian and international formats)
    is_ukr = validate_ukr_phone_number(phone_number)
    is_intl = validate_int_phone_number(phone_number)

    if not is_ukr and not is_intl:
        message_text = (
            "Будь ласка, вкажіть свій контактний номер телефону у форматі +380********* або "
            + "натисніть кнопку 'Поділитися номером'."
        )
        bot.send_message(message.chat.id, message_text)

        return None

    # Return the valid phone number
    return phone_number
