from telebot import TeleBot
from telebot.types import CallbackQuery

from product_bot.management.buttons.bot_buttons import CityButtons
from product_bot.management.commands.base_call_router import BaseTGCallRouter
from product_bot.management.commands.city.contextual_handler import ContextualHandler
from product_bot.management.commands.city.router_setup import setup_context_handlers


class PriceHandler:
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.context_name = "price"
        self.contextual_handler = ContextualHandler()

    def handle_prices(self, call: CallbackQuery):
        """
        Prompt the user to select a city for viewing prices.

        Sends a message to the user with a set of buttons representing available cities.
        The user can select a city to proceed with viewing prices.

        Args:
            call (CallbackQuery):
                The callback query object containing the user's interaction data.
        """
        city_markup = CityButtons.city_buttons(self.context_name)
        self.bot.send_message(
            call.message.chat.id,
            "Будь ласка, оберіть місто для визначення цін:",
            reply_markup=city_markup,
        )

    def handle_city_for_prices(self, call: CallbackQuery):
        """
        Handle the user's city selection for price lookup.

        After the user selects a city, this method delegates the handling
        of the context to the contextual handler. If an error occurs during
        processing, it sends an error message to the user.

        Args:
            call (CallbackQuery):
                The callback query object containing the user's selection data.
        """
        chat_id = call.message.chat.id
        city_code = call.data.split("_")[0]
        try:
            self.contextual_handler.handle_city_context(
                self.bot,
                chat_id,
                city_code,
                self.context_name,
            )
        except Exception as err:
            self.bot.send_message(chat_id, "Виникла помилка: {}".format(err))


def setup_prices_handler(bot: TeleBot):
    handler = PriceHandler(bot)
    prices_router = BaseTGCallRouter(handler.context_name)
    contextual_handler = ContextualHandler()

    setup_context_handlers(bot, handler.context_name, contextual_handler)

    bot.callback_query_handler(func=prices_router.is_call_match_router)(
        handler.handle_prices,
    )
    bot.callback_query_handler(func=lambda call: call.data.endswith("_price"))(
        handler.handle_city_for_prices,
    )
