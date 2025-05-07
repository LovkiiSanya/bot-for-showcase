from telebot import TeleBot

from product_bot.management.commands.tech_support.admin_handlers import join_administrator
from product_bot.management.commands.tech_support.handlers import (
    handle_leave_issue_description,
    handle_request_callback,
    handle_show_contacts,
    handle_tech_support_query,
)


def setup_tech_support_query_handler(bot, tech_router):
    bot.callback_query_handler(func=tech_router.is_call_match_router)(
        lambda call: handle_tech_support_query(call, bot),
    )


def setup_leave_issue_handler(bot, leave_issue_router):
    bot.callback_query_handler(func=leave_issue_router.is_call_match_router)(
        lambda call: handle_leave_issue_description(call, bot),
    )


def setup_show_contacts_handler(bot, contacts_router):
    bot.callback_query_handler(func=contacts_router.is_call_match_router)(
        lambda call: handle_show_contacts(call, bot),
    )


def setup_request_callback_handler(bot, callback_router):
    bot.callback_query_handler(func=callback_router.is_call_match_router)(
        lambda call: handle_request_callback(call, bot),
    )


def setup_join_admin_handler(bot: TeleBot, join_admin_router):
    bot.callback_query_handler(
        func=join_admin_router.is_call_match_router,
    )(lambda call: join_administrator(call, bot))
