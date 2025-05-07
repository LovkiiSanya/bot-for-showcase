from telebot import TeleBot

from product_bot.management.commands.base_call_router import BaseTGCallRouter
from product_bot.management.help_handlers.question_handlers.custom_question import (
    handle_own_question,
)
from product_bot.management.help_handlers.question_handlers.main_questions_first import (
    handle_infertility,
    handle_ivf,
    handle_pregnancy,
    handle_question,
    handle_surgery,
)
from product_bot.management.help_handlers.question_handlers.main_questions_second import (
    handle_andrology,
    handle_genetics,
    handle_gynecology,
    handle_poliklinika,
)


def make_callback(handler, bot):
    return lambda call: handler(call, bot)


def setup_question_handlers(bot: TeleBot):
    handlers = {
        "question": handle_general_question,
        "service_1": handle_service_1,
        "service_2": handle_service_2,
        "service_3": handle_service_3,
        "service_4": handle_service_4,
        "service_5": handle_service_5,
        "service_6": handle_service_6,
        "service_7": handle_service_7,
        "service_8": handle_service_8,
        "custom_question": handle_custom_question,
    }

    for prefix, handler in handlers.items():
        router = BaseTGCallRouter(prefix)
        bot.callback_query_handler(
            func=router.is_call_match_router,
        )(make_callback(handler, bot))

