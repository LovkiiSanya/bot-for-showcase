from product_bot.management.buttons.bot_buttons import InfoButtons, QuestionButtons
from product_bot.management.lists.list_of_doctors import (
    androlog_button,
    ginekolog_button,
    reproduktolog_button,
)
from product_bot.management.lists.list_of_tech import custom_question
from product_bot.management.utils.load_texts import load_text


def handle_question(call, bot):
    analysis_info_markup = InfoButtons.analysis_buttons()

    analysis_info_markup.add(custom_question)

    bot.send_message(
        call.message.chat.id,
        "Стосовно якого напрямку у Вас є питання?",
        reply_markup=analysis_info_markup,
    )


def handle_example1(call, bot):
    questions_markup = QuestionButtons.question_appointment_button()
    questions_markup.add(example_button)
    example1_text = load_text("example1_auto_message")
    bot.send_message(
        call.message.chat.id,
        example1_text,
        reply_markup=questions_markup,
    )


def handle_example2(call, bot):
    questions_markup = QuestionButtons.question_appointment_button()
    questions_markup.add(example_button)
    example2_text = load_text("example2auto_message")
    bot.send_message(
        call.message.chat.id,
        example2_text,
        reply_markup=questions_markup,
    )


def handle_example3(call, bot):
    questions_markup = QuestionButtons.question_appointment_button()
    questions_markup.add(example_button)
    example3_text = load_text("example3_auto_message")
    bot.send_message(
        call.message.chat.id,
        example3_text,
        reply_markup=questions_markup,
    )


def handle_example4(call, bot):
    questions_markup = QuestionButtons.question_appointment_button()
    questions_markup.add(example_button)
    example4_text = load_text("example4_auto_message")
    bot.send_message(
        call.message.chat.id,
        example4_text,
        reply_markup=questions_markup,
    )
