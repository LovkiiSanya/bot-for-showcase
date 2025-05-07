from functools import partial

from telebot import TeleBot
from telebot.types import CallbackQuery

from product_bot.management.commands.base_call_router import BaseTGCallRouter
from product_bot.management.registration_hanlers.name import NameHandler


def handle_registration(
    call: CallbackQuery,
    bot: TeleBot,
    handler: NameHandler,
):
    bot.send_message(call.message.chat.id, "Вкажіть Ваше ім'я")
    bot.register_next_step_handler(
        call.message,
        lambda msg: handler.ask_first_name(msg),
    )


def setup_registration_handler(
    bot: TeleBot,
    registration_handler: NameHandler,
    registration_router: BaseTGCallRouter,
):
    bot.callback_query_handler(func=registration_router.is_call_match_router)(
        partial(handle_registration, bot=bot, handler=registration_handler),
    )
