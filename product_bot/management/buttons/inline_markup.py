from telebot import types


def inline_markup(row_width=1):
    return types.InlineKeyboardMarkup(row_width=row_width)
