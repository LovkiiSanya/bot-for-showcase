from types import MappingProxyType
from telebot import types

# Placeholder buttons for demo purposes
sample_button_1 = types.InlineKeyboardButton("Doctor A", callback_data="doctor_a")
sample_button_2 = types.InlineKeyboardButton("Doctor B", callback_data="doctor_b")
sample_button_3 = types.InlineKeyboardButton("Doctor C", callback_data="doctor_c")
sample_button_4 = types.InlineKeyboardButton("Doctor D", callback_data="doctor_d")
tech_support_button = types.InlineKeyboardButton("Tech Support", callback_data="tech_support")

# Example doctor buttons mapped to cities
CITY_BUTTONS = MappingProxyType({
    "city_a": [sample_button_1, sample_button_2, tech_support_button],
    "city_b": [sample_button_2, sample_button_3, sample_button_4, tech_support_button],
    "city_c": [sample_button_1, sample_button_4, tech_support_button],
})


class SampleDoctorButtons:

    @classmethod
    def get_doctors_buttons(cls, city_name: str) -> types.InlineKeyboardMarkup:
        """
        Retrieve placeholder doctor buttons for a given city.

        Args:
            city_name (str): The name of the city for which to retrieve buttons.

        Returns:
            InlineKeyboardMarkup: An inline keyboard with doctor options.

        Raises:
            ValueError: If the city is not supported.
        """
        buttons = CITY_BUTTONS.get(city_name.lower())
        if not buttons:
            raise ValueError("No buttons defined for city: {}".format(city_name))

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(*buttons)
        return markup
