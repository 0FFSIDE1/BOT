# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
import json
from asgiref.sync import async_to_sync
from django.utils.decorators import async_only_middleware

load_dotenv()

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_ADMIN_CHAT_ID')

# Create an Application instance but don't initialize yet
application = Application.builder().token(bot_token).build()
application_initialized = False

async def start(update: Update, context) -> None:
    await update.message.reply_text('Hello! How can I help you today?')

async def handle_message(update: Update, context) -> None:
    """Handle incoming text messages."""
    text = update.message.text
    if 'help' in text.lower():
        await update.message.reply_text('How can I assist you? Please provide details.')
    else:
        # Directly await the send_message method
        await context.bot.send_message(chat_id=chat_id, text=f'User Message: {text}')
        await update.message.reply_text("Thank you for your message! A support representative will reach out if needed.")

@csrf_exempt
@async_only_middleware
def telegram_webhook(request):
    global application_initialized
    if not application_initialized:
        # Initialize the Application asynchronously
        async_to_sync(application.initialize)()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application_initialized = True

    if request.method == "POST":
        # Parse the request body as JSON
        data = json.loads(request.body.decode("utf-8"))
        update = Update.de_json(data, application.bot)
        
        # Process the update
        async_to_sync(application.process_update)(update)
        
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Invalid request"}, status=400)


