from product_bot.management.buttons.bot_buttons import QuestionButtons
from product_bot.management.lists.list_of_doctors import (
    androlog_button,
    endokrinolog_button,
    geneticist_button,
    ginekolog_button,
    mamolog_button,
    oncologist_button,
    prenatal_diagnosis_button,
    therapist_button,
)
from product_bot.management.utils.load_texts import load_text


def handle_example5(call, bot):
    questions_markup = QuestionButtons.question_appointment_button()
    questions_markup.add(example_button)
    example5_text = load_text("example5_auto_message")
    bot.send_message(
        call.message.chat.id,
        example5_text,
        reply_markup=questions_markup,
    )


def handle_example6(call, bot):
    questions_markup = QuestionButtons.question_appointment_button()
    questions_markup.add(example_button)
    example6_text = load_text("example6_auto_message")
    bot.send_message(
        call.message.chat.id,
        example6_text,
        reply_markup=questions_markup,
    )


def handle_example7(call, bot):
    questions_markup = QuestionButtons.question_appointment_button()
    questions_markup.add(
        example_button
    )
    example7_text = load_text("example7_auto_message")
    bot.send_message(
        call.message.chat.id,
        example7_text,
        reply_markup=questions_markup,
    )


def handle_example8(call, bot):
    questions_markup = QuestionButtons.question_appointment_button()
    questions_markup.add(example_button)
    example8_text = load_text("example8_auto_message")
    bot.send_message(
        call.message.chat.id,
        example8_text,
        reply_markup=questions_markup,
    )
