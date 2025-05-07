from telebot import types

from product_bot.management.buttons.inline_markup import inline_markup
from product_bot.management.lists.template_buttons import (
    sample_button_a,
    sample_button_b,
    sample_button_c,
    sample_button_d,
    sample_button_e,
    sample_button_f,
    sample_button_g,
    sample_button_h,
    sample_button_i,
    sample_button_j,
)


class SamplePatientButtons:
    @classmethod
    def create_patient_buttons(cls):
        markup = inline_markup()
        markup.add(
            sample_button_a,
            sample_button_b,
            sample_button_c,
        )
        return markup

    @classmethod
    def create_not_found_patient_buttons(cls):
        markup = inline_markup()
        markup.add(
            sample_button_d,
            sample_button_e,
            sample_button_c,
        )
        return markup

    @classmethod
    def create_non_patient_buttons(cls):
        markup = inline_markup(row_width=2)
        markup.add(
            sample_button_e,
            sample_button_c,
        )
        return markup


class SampleSupportButtons:
    @classmethod
    def create_support_buttons(cls):
        markup = inline_markup()
        markup.add(sample_button_f)
        return markup

    @classmethod
    def support_options(cls):
        markup = inline_markup()
        markup.add(
            sample_button_e,
            sample_button_g,
            sample_button_h,
            sample_button_i,
            sample_button_j,
        )
        return markup

    @classmethod
    def appointment_confirmation(cls):
        markup = inline_markup()
        markup.add(
            sample_button_e,
            sample_button_g,
        )
        return markup


class SamplePhoneButtons:
    @classmethod
    def share_number(cls):
        markup = types.ReplyKeyboardMarkup(
            row_width=1,
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        share_number_button = types.KeyboardButton(
            text="Share Contact",
            request_contact=True,
        )
        markup.add(share_number_button)
        return markup


class SampleInfoButtons:
    @classmethod
    def create_info_buttons(cls):
        markup = inline_markup(row_width=2)
        markup.add(sample_button_e)
        return markup

    @classmethod
    def additional_buttons(cls):
        markup = inline_markup()
        markup.add(
            sample_button_a,
            sample_button_d,
            sample_button_f,
            sample_button_g,
            sample_button_c,
        )
        return markup

    @classmethod
    def analysis_buttons(cls):
        markup = inline_markup()
        markup.add(
            sample_button_a,
            sample_button_d,
            sample_button_g,
            sample_button_h,
            sample_button_b,
            sample_button_f,
            sample_button_i,
            sample_button_j,
            sample_button_c,
        )
        return markup


class SampleQuestionButtons:
    @classmethod
    def question_appointment_buttons(cls):
        markup = inline_markup()
        markup.add(
            sample_button_a,
            sample_button_d,
            sample_button_j,
        )
        return markup


class SampleCityButtons:
    @classmethod
    def city_buttons(cls, context):
        markup = inline_markup()
        markup.add(
            types.InlineKeyboardButton("City A", callback_data="city_a_{}".format(context)),
            types.InlineKeyboardButton("City B", callback_data="city_b_{}".format(context)),
            types.InlineKeyboardButton("City C", callback_data="city_c_{}".format(context)),
            types.InlineKeyboardButton("City D", callback_data="city_d_{}".format(context)),
            types.InlineKeyboardButton("City E", callback_data="city_e_{}".format(context)),
            types.InlineKeyboardButton("City F", callback_data="city_f_{}".format(context)),
            types.InlineKeyboardButton("City G", callback_data="city_g_{}".format(context)),
            types.InlineKeyboardButton("City H", callback_data="city_h_{}".format(context)),
            sample_button_d,
        )
        return markup


class SampleAnonymousButtons:
    @classmethod
    def anonymous_buttons(cls):
        markup = inline_markup()
        markup.add(
            sample_button_a,
            sample_button_b,
        )
        return markup

    @classmethod
    def temporary_button(cls):
        markup = inline_markup()
        markup.add(
            sample_button_i,
            sample_button_j,
        )
        return markup
