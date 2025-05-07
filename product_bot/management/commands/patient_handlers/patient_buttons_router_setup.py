from functools import partial

from telebot import TeleBot

from product_bot.management.commands.base_call_router import BaseTGCallRouter
from product_bot.management.commands.patient_handlers.patient_buttons_handlers import (
    handle_help,
    handle_patient_no,
    handle_patient_yes,
    show_info,
)


def setup_patient_yes_handler(bot, registration_handler, patient_yes_router):
    bot.callback_query_handler(func=patient_yes_router.is_call_match_router)(
        partial(handle_patient_yes, bot=bot, handler=registration_handler),
    )


def setup_patient_no_handler(bot: TeleBot, patient_no_router: BaseTGCallRouter):
    bot.callback_query_handler(func=patient_no_router.is_call_match_router)(
        partial(handle_patient_no, bot=bot),
    )


def setup_help_handler(bot: TeleBot, help_router: BaseTGCallRouter):
    bot.callback_query_handler(func=help_router.is_call_match_router)(
        partial(handle_help, bot=bot),
    )


def setup_show_info_handler(bot: TeleBot, show_info_router: BaseTGCallRouter):
    bot.callback_query_handler(func=show_info_router.is_call_match_router)(
        partial(show_info, bot=bot),
    )
