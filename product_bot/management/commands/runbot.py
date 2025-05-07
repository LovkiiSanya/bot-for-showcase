import logging
import os
import time

import django
from django.core.management.base import BaseCommand
from telebot import TeleBot

from product_bot import settings
from product_bot.management.commands.patient_handlers.setup import setup_patient_handlers
from product_bot.management.commands.tech_support.init_handlers import (
    setup_tech_support_handlers,
)
from product_bot.management.help_handlers.appointment_handler import setup_appointment_handlers
from product_bot.management.help_handlers.bot_help_handler import setup_help_handlers
from product_bot.management.help_handlers.exam_analysis.setup_examination_analysis_handler import (
    setup_examination_analysis_handler,
)
from product_bot.management.help_handlers.prices_handler import setup_prices_handler
from product_bot.management.help_handlers.question_handlers.setup import setup_question_handlers
from product_bot.management.help_handlers.review_handler import setup_review_handler

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "product_bot.settings")
django.setup()

logger = logging.getLogger(__name__)

# Initialize the bot globally
bot = TeleBot(settings.TELEGRAM_TOKEN)


def initialize_bot():
    """Initialize the Telegram bot and register all handlers."""

    setup_patient_handlers(bot)
    setup_tech_support_handlers(bot)
    setup_help_handlers(bot)
    setup_appointment_handlers(bot)
    setup_question_handlers(bot)
    setup_review_handler(bot)
    setup_examination_analysis_handler(bot)
    setup_prices_handler(bot)

    logger.info("Bot handlers initialized.")


class Command(BaseCommand):
    help = "Starts the Telegram bot"

    def handle(self, *args, **options):
        if not settings.TELEGRAM_TOKEN:
            self.stdout.write(self.style.ERROR("TELEGRAM_TOKEN is not set."))
            return

        self.stdout.write(self.style.SUCCESS("Starting the Telegram bot..."))

        if "localhost" in settings.ALLOWED_HOSTS or "127.0.0.1" in settings.ALLOWED_HOSTS:
            webhook_url = "https://{}/webhook/".format(settings.ALLOWED_HOSTS[3])
        else:
            webhook_url = "https://{}/webhook/".format(settings.ALLOWED_HOSTS[4])

        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook(url=webhook_url)

        webhook_info = bot.get_webhook_info()
        logger.info("Webhook Info: {}".format(webhook_info))
        self.stdout.write(self.style.SUCCESS("Webhook set to {}".format(webhook_url)))

        try:
            while True:
                logger.info("Bot is running and waiting for updates...")
                time.sleep(1000)
        except KeyboardInterrupt:
            logger.info("Bot shutdown requested.")
