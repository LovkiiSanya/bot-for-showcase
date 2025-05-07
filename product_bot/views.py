import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telebot import types

from product_bot.management.commands.runbot import bot, initialize_bot

logger = logging.getLogger(__name__)

HTTP_NOT_ALLOWED = 405
BAD_REQUEST = 400

initialize_bot()


@csrf_exempt
def webhook(request):
    """
    Handle Telegram webhook requests.

    Args:
        request: Django HTTP request object.

    Returns:
        JsonResponse indicating success or failure.
    """
    if request.method != "POST":
        logger.warning(
            "Invalid request method: {}".format(request.method),
        )
        return JsonResponse(
            {"message": "Method not allowed"},
            status=HTTP_NOT_ALLOWED,
        )

    return _process_telegram_update(request)


def _process_telegram_update(request):
    """
    Processes the actual update from Telegram.

    Args:
        request: Django HTTP request object.

    Returns:
        JsonResponse: Success or error message.
    """
    json_str = _decode_request_body(request)
    if not json_str:
        return JsonResponse(
            {"error": "Invalid request body"},
            status=BAD_REQUEST,
        )

    update = _parse_telegram_update(json_str)
    if not update:
        return JsonResponse(
            {"error": "Invalid Telegram update format"},
            status=BAD_REQUEST,
        )

    if not _process_update(update):
        return JsonResponse(
            {"error": "Failed to process update"},
            status=BAD_REQUEST,
        )

    return JsonResponse({"status": "success"})


def _decode_request_body(request):
    """
    Helper function to decode the request body.

    Args:
        request: Django HTTP request object.

    Returns:
        str or None: Decoded request body if successful, otherwise None.
    """
    try:
        return request.body.decode("UTF-8")
    except Exception as decode_err:
        logger.error(
            "Failed to decode request body: {}".format(str(decode_err)),
            exc_info=True,
        )
        return None


def _parse_telegram_update(json_str):
    """
    Helper function to parse the Telegram update.

    Args:
        json_str: The JSON string representing the update.

    Returns:
        Update or None: Parsed Telegram Update
        object if successful, otherwise None.
    """
    try:
        return types.Update.de_json(json_str)
    except Exception as parse_err:
        logger.error(
            "Failed to parse Telegram update: {}".format(str(parse_err)),
            exc_info=True,
        )
        return None


def _process_update(update):
    """
    Helper function to process the update.

    Args:
        update: Telegram Update object.

    Returns:
        bool: True if update is processed successfully, otherwise False.
    """
    try:
        bot.process_new_updates([update])
    except Exception as process_err:
        logger.error(
            "Failed to process update: {}".format(str(process_err)),
            exc_info=True,
        )
        return False

    return True
