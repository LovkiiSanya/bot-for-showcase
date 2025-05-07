from unittest.mock import MagicMock

import pytest
from telebot import TeleBot
from telebot.types import CallbackQuery, Chat, Message

from product_bot.management.help_handlers.review_handler import setup_review_handler
from product_bot.models import Patient

TEST_ID = 12345


@pytest.mark.django_db
def test_handle_review(db):
    bot = MagicMock(spec=TeleBot)
    setup_review_handler(bot)

    call = MagicMock(
        spec=CallbackQuery,
        data="new_review",
        message=MagicMock(
            spec=Message,
            chat=MagicMock(
                spec=Chat,
                id=TEST_ID,
            ),
        ),
    )

    for handler_args, _ in bot.callback_query_handler.call_args_list:
        if handler_args and handler_args[0](call):
            bot.send_message.assert_called_once_with(
                TEST_ID,
                "Бажаєте залишити анонімний відгук?",
                reply_markup="mock_markup",
            )
            break


@pytest.mark.django_db
def test_handle_anonymous_review(db):
    bot = MagicMock(spec=TeleBot)
    setup_review_handler(bot)

    call = MagicMock(
        spec=CallbackQuery,
        data="review_anonymous",
        message=MagicMock(
            spec=Message,
            chat=MagicMock(
                spec=Chat,
                id=TEST_ID,
            ),
        ),
    )

    message = MagicMock(spec=Message, text="Anonymous review text")
    patient = MagicMock(spec=Patient)
    MagicMock(return_value=(patient, True))

    for handler_args, _ in bot.callback_query_handler.call_args_list:
        if handler_args and handler_args[0](call):
            bot.register_next_step_handler_by_chat_id.call_args[0][1](message)
            patient.save.assert_called_once()
            bot.send_message.assert_any_call(
                TEST_ID,
                "Дякуємо за анонімний відгук!",
            )
            break
