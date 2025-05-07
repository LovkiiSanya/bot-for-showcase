from telebot import types

support_button = types.InlineKeyboardButton(
    "Technical Support",
    callback_data="support_request",
)

pricing_button = types.InlineKeyboardButton(
    "View Pricing",
    callback_data="view_prices",
)

help_button = types.InlineKeyboardButton(
    "Need Help?",
    callback_data="help_options",
)

contact_admin_button = types.InlineKeyboardButton(
    "Contact Administrator",
    callback_data="contact_admin",
)

confirm_user_button = types.InlineKeyboardButton(
    "Yes, I’m a registered user",
    callback_data="user_confirm_yes",
)

register_button = types.InlineKeyboardButton(
    "Register",
    callback_data="start_registration",
)

decline_user_button = types.InlineKeyboardButton(
    "No, not yet registered",
    callback_data="user_confirm_no",
)

restart_button = types.InlineKeyboardButton(
    "Restart Conversation",
    callback_data="restart_conversation",
)

local_number_button = types.InlineKeyboardButton(
    "Local Number",
    callback_data="phone_type_local",
)

international_number_button = types.InlineKeyboardButton(
    "International Number",
    callback_data="phone_type_international",
)

view_profile_button = types.InlineKeyboardButton(
    "View My Info",
    callback_data="view_user_info",
)

submit_review_button = types.InlineKeyboardButton(
    "Submit Feedback",
    callback_data="submit_feedback",
)

book_consultation_button = types.InlineKeyboardButton(
    "Book Consultation",
    callback_data="book_consultation",
)

submit_analysis_button = types.InlineKeyboardButton(
    "Submit Analysis",
    callback_data="submit_analysis",
)

ask_question_button = types.InlineKeyboardButton(
    "I Have a Question",
    callback_data="ask_question",
)

report_issue_button = types.InlineKeyboardButton(
    "Report an Issue",
    callback_data="report_issue",
)

contact_info_button = types.InlineKeyboardButton(
    "Contact Info",
    callback_data="view_contacts",
)

request_callback_button = types.InlineKeyboardButton(
    "Request Callback",
    callback_data="request_callback",
)

anonymous_yes_button = types.InlineKeyboardButton(
    "Anonymously",
    callback_data="feedback_anonymous",
)

anonymous_no_button = types.InlineKeyboardButton(
    "With My Info",
    callback_data="feedback_named",
)

custom_question_button = types.InlineKeyboardButton(
    "Ask My Own Question",
    callback_data="custom_user_question",
)

use_saved_data_button = types.InlineKeyboardButton(
    "Use Saved Data",
    callback_data="use_saved_data",
)

restart_from_scratch_button = types.InlineKeyboardButton(
    "Start from Scratch",
    callback_data="restart_fresh",
)
