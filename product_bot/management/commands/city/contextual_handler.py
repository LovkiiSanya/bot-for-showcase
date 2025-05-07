from product_bot.management.commands.city.city_context_flow import prompt_analysis_input
from product_bot.management.commands.city.city_doctor_flow import show_doctors


class ContextualHandler:
    """Dynamic handler for context-specific actions."""

    def __init__(self):
        self.locations = {
            "city_a": "City A",
            "city_b": "City B",
            "city_c": "City C",
            "city_d": "City D",
            "city_e": "City E",
            "city_f": "City F",
            "city_g": "City G",
            "city_h": "City H",
        }

        self.prices = {
            "city_a": "Service A - $50\nService B - $70",
            "city_b": "Service C - $40\nService D - $60",
            "city_c": "Service E - $45\nService F - $65",
            "city_d": "Service G - $50\nService H - $75",
            "city_e": "Service I - $55\nService J - $80",
            "city_f": "Service K - $50\nService L - $70",
            "city_g": "Service M - $60\nService N - $90",
            "city_h": "Service O - $65\nService P - $85",
        }

        self.context_actions = {
            "appointment": show_specialists,
            "examination_analysis": prompt_test_selection,
            "price": self.show_prices,
            # Extend with other generic actions as needed
        }

    def handle_city_context(self, bot, chat_id, city_code, context):
        """
            Call the appropriate action based on the context.

        This function retrieves the selected city using the city code and
        calls the corresponding action from the context actions dictionary.
        If no action is found for the given context, an error message is sent.

        Args:
            bot (TeleBot): The bot instance used to send messages to the user.
            chat_id (int): The unique identifier for the user's chat.
            city_code (str): The code representing the selected city.
            context (str): The context in which the action should be performed.
        """
        selected_city = self.cities.get(city_code, "Сталася помилка.")
        action = self.context_actions.get(context)

        if action:
            action(bot, chat_id, city_code, selected_city)
        else:
            bot.send_message(chat_id, "Сталася помилка")

    def show_prices(self, bot, chat_id, city_code, city_name):
        """
        Displays prices for the selected city.

        This function fetches and sends the prices for the specified city to
        the user's chat. If prices are unavailable for the selected city,
        a default message is sent.

        Args:
            bot (TeleBot): The bot instance used to send messages to the user.
            chat_id (int): The unique identifier for the user's chat.
            city_code (str): The code representing the selected city.
            city_name (str): The name of the selected city.
        """
        price_message = self.prices.get(
            city_code,
            "Prices are currently unavailable for this city.",
        )
        bot.send_message(chat_id, price_message)
