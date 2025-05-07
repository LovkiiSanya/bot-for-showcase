from dataclasses import dataclass
from functools import partial

from telebot import TeleBot

from product_bot.management.commands.base_call_router import BaseTGCallRouter
from product_bot.management.commands.patient_handlers.patient_buttons_router_setup import (
    setup_help_handler,
    setup_patient_no_handler,
    setup_patient_yes_handler,
    setup_show_info_handler,
)
from product_bot.management.commands.patient_handlers.registration_handlers import (
    setup_registration_handler,
)
from product_bot.management.commands.patient_handlers.start_handlers import (
    handle_contact,
    setup_restart_handler,
    start_command,
)
from product_bot.management.registration_hanlers.name import NameHandler
from product_bot.management.registration_hanlers.phone import PhoneHandler


@dataclass
class PatientRouters:
    restart_router: BaseTGCallRouter
    patient_yes_router: BaseTGCallRouter
    patient_no_router: BaseTGCallRouter
    help_router: BaseTGCallRouter
    show_info_router: BaseTGCallRouter
    registration_router: BaseTGCallRouter


def setup_patient_handlers(bot: TeleBot):

    phone_handler = PhoneHandler(bot)
    name_handler = NameHandler(bot)

    routers = PatientRouters(
        restart_router=BaseTGCallRouter("restart_communication"),
        patient_yes_router=BaseTGCallRouter("is_patient_yes"),
        patient_no_router=BaseTGCallRouter("is_patient_no"),
        help_router=BaseTGCallRouter("help"),
        show_info_router=BaseTGCallRouter("show_info"),
        registration_router=BaseTGCallRouter("registration"),
    )

    setup_message_handlers(bot, phone_handler)

    setup_callback_query_handlers(
        bot,
        name_handler,
        phone_handler,
        routers,
    )


def setup_message_handlers(bot: TeleBot, phone_handler: PhoneHandler):

    bot.message_handler(commands=["start"])(
        partial(start_command, bot=bot),
    )
    bot.message_handler(content_types=["contact"])(
        partial(handle_contact, registration_handler=phone_handler),
    )


def setup_callback_query_handlers(
    bot: TeleBot,
    name_handler: NameHandler,
    phone_handler: PhoneHandler,
    routers: PatientRouters,
):
    setup_restart_handler(bot, routers.restart_router)
    setup_patient_yes_handler(bot, phone_handler, routers.patient_yes_router)
    setup_patient_no_handler(bot, routers.patient_no_router)
    setup_help_handler(bot, routers.help_router)
    setup_show_info_handler(bot, routers.show_info_router)
    setup_registration_handler(bot, name_handler, routers.registration_router)
