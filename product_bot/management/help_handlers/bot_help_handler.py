from telebot import TeleBot
from telebot.types import CallbackQuery

from product_bot.management.buttons.bot_buttons import InfoButtons
from product_bot.management.commands.base_call_router import BaseTGCallRouter


class HelpHandler:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def handle_help_button(self, call: CallbackQuery):
        markup = InfoButtons.additional_buttons()
        self.bot.send_message(
            call.message.chat.id,
            "Чим ми можемо Вам допомогти?",
            reply_markup=markup,
        )


def setup_help_handlers(bot: TeleBot):
    handler = HelpHandler(bot)
    can_help_router = BaseTGCallRouter("can_help")

    bot.callback_query_handler(func=can_help_router.is_call_match_router)(
        handler.handle_help_button,
    )
