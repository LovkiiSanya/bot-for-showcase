from telebot import TeleBot

from product_bot.management.commands.base_call_router import BaseTGCallRouter
from product_bot.management.commands.city.city_context_flow import (
    handle_city_selection,
    handle_context,
)
from product_bot.management.commands.city.constants import CITY_MESSAGES
from product_bot.management.commands.city.contextual_handler import ContextualHandler
from product_bot.management.commands.city.handle_analysis_input import handle_analysis_input


def context_handler(call, bot: TeleBot, context_name: str, handler: ContextualHandler):
    handle_context(call, bot, context_name, handler)


def city_selection_handler(call, bot: TeleBot, handler: ContextualHandler):
    handle_city_selection(call, bot, handler)


def analysis_input_handler(message, bot: TeleBot):
    handle_analysis_input(message, bot)


def is_city_callback(call) -> bool:
    """
    Check if the callback relates to a city selection.

    This function inspects the callback data to determine whether it matches
    one of the predefined city keys in CITY_MESSAGES.

    Args:
        call: The callback query object containing user interaction data.

    Returns:
        bool: True if the callback corresponds to a city selection, False otherwise.
    """
    city_key = call.data.split("_")[0]
    return city_key in CITY_MESSAGES


def setup_context_handlers(bot: TeleBot, context_name: str, handler: ContextualHandler):
    """
    Set up Telegram handlers for a specific context.

    This function registers two types of callback handlers:
    one for handling general context-related callbacks and
    another for handling city-specific selections.

    Args:
        bot (TeleBot): The Telegram bot instance to register handlers on.
        context_name (str): The name of the context to associate handlers with.
        handler (ContextualHandler): The contextual handler responsible
            for managing city-based interactions.
    """
    router = BaseTGCallRouter(context_name)

    # Register context callback handler
    bot.callback_query_handler(func=router.is_call_match_router)(
        lambda call: context_handler(call, bot, context_name, handler),
    )

    # Register city selection callback handler
    bot.callback_query_handler(func=is_city_callback)(
        lambda call: city_selection_handler(call, bot, handler),
    )
