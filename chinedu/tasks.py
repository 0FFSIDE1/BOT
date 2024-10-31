# tasks.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from django.conf import settings
import os
# Celery task for processing updates
from celery import shared_task
from asgiref.sync import async_to_sync

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_ADMIN_CHAT_ID')

application = ApplicationBuilder().token(bot_token).build()


async def start(update: Update, context) -> None:
    await update.message.reply_text('Hello! How can I help you today?')

async def handle_message(update: Update, context) -> None:
    """Handle incoming text messages."""
    text = update.message.text
    if 'help' in text.lower():
        await update.message.reply_text('How can I assist you? Please provide details.')
    else:
        await context.bot.send_message(chat_id=chat_id, text=f'User Message: {text}')
        await update.message.reply_text("Thank you for your message! A support representative will reach out if needed.")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


@shared_task
def process_update_task(data):
    update = Update.de_json(data, application.bot)
    async_to_sync(application.process_update)(update)
