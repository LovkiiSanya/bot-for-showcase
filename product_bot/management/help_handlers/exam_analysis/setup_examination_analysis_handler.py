from telebot import TeleBot

from product_bot.management.commands.city.contextual_handler import ContextualHandler
from product_bot.management.commands.city.router_setup import setup_context_handlers
from product_bot.management.help_handlers.exam_analysis.city_selection_entry import (
    handle_city_selection,
)


def city_selection_callback(call, bot, handler):
    return handle_city_selection(call, bot, handler)


def setup_examination_analysis_handler(bot: TeleBot):
    context_name = "examination_analysis"
    contextual_handler = ContextualHandler()

    setup_context_handlers(bot, context_name, contextual_handler)

    bot.callback_query_handler(
        func=lambda call: call.data in contextual_handler.cities.keys(),
    )(lambda call: city_selection_callback(call, bot, contextual_handler))
