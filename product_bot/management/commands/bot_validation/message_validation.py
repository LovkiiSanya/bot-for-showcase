import re


def is_multimedia_content(message):
    """
    Check if the message contains multimedia
    content like stickers, videos, or photos.

    Args:
        message (Message): The message object to check for multimedia content.

    Returns:
        bool: True if the message contains multimedia content, otherwise False.
    """
    return message.content_type in {"sticker", "video", "audio", "photo"}


def is_valid_issue_description(description):
    """
    Validate the issue description using a regex pattern.

    Args:
        description (str): The issue description to validate.

    Returns:
        bool: True if the description matches
        the valid pattern, otherwise False.
    """
    pattern = r"^[\w\s.,!?()'\"‘’“”—-]*$"
    return bool(re.match(pattern, description))
