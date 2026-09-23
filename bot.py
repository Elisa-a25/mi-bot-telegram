"""A simple Telegram bot that greets, shows help, and echoes text."""

import logging
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(name)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    if update.message:
        await update.message.reply_text(
            "Hello! I'm an echo bot. Send me any text and I'll repeat it back."
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    if update.message:
        await update.message.reply_text(
            "Available commands:\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n\n"
            "Send any text message to have me echo it back."
        )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo any text message received."""
    if update.message:
        await update.message.reply_text(update.message.text)


def main() -> None:
    """Create the bot application and start polling for updates."""
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "BOT_TOKEN is not set. Create a Telegram bot with BotFather and "
            "set its token in the BOT_TOKEN environment variable."
        )

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Bot is starting...")
    application.run_polling()


if name == "main":
    main()
