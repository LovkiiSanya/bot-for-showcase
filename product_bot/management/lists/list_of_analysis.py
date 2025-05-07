from telebot import types

# Example/Showcase analysis buttons (renamed for abstraction)
fertility_button = types.InlineKeyboardButton(
    "Fertility Treatment",
    callback_data="fertility",
)
reproductive_button = types.InlineKeyboardButton(
    "Reproductive Support",
    callback_data="reproductive_support",
)
surgical_button = types.InlineKeyboardButton(
    "Surgical Procedures",
    callback_data="surgical",
)
maternity_button = types.InlineKeyboardButton(
    "Maternity Care",
    callback_data="maternity",
)
general_health_button = types.InlineKeyboardButton(
    "General Health",
    callback_data="general_health",
)
men_health_button = types.InlineKeyboardButton(
    "Men’s Health",
    callback_data="mens_health",
)
clinic_services_button = types.InlineKeyboardButton(
    "Clinic Services",
    callback_data="clinic_services",
)
genetic_testing_button = types.InlineKeyboardButton(
    "Genetic Testing",
    callback_data="genetic_testing",
)
