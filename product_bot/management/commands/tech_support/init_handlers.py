from telebot import TeleBot

from product_bot.management.commands.base_call_router import BaseTGCallRouter
from product_bot.management.commands.tech_support.router_setup import (
    setup_join_admin_handler,
    setup_leave_issue_handler,
    setup_request_callback_handler,
    setup_show_contacts_handler,
    setup_tech_support_query_handler,
)


def setup_tech_support_handlers(bot: TeleBot):
    """
    Sets up the handlers for tech support interactions.

    Args:
        bot (TeleBot): The TeleBot instance used
            to register callback query handlers.

    This function initializes various routers
    for different tech support queries and
    sets up the corresponding handlers for those queries.
    """

    # Initialize routers
    tech_router = BaseTGCallRouter("is_patient_tech")
    contacts_router = BaseTGCallRouter("show_contacts")
    callback_router = BaseTGCallRouter("request_callback")
    leave_issue_router = BaseTGCallRouter("leave_issue")
    join_admin_router = BaseTGCallRouter("join_admin")
    # Set up handlers
    setup_tech_support_query_handler(bot, tech_router)
    setup_leave_issue_handler(bot, leave_issue_router)
    setup_show_contacts_handler(bot, contacts_router)
    setup_request_callback_handler(bot, callback_router)
    setup_join_admin_handler(bot, join_admin_router)
