"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
from django.core.asgi import get_asgi_application
import os
import django
import asyncio
from telegram.ext import Application
from dotenv import load_dotenv


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

load_dotenv()

application = get_asgi_application()
app = application

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
if bot_token:
    async def initialize_bot():
        telegram_app = Application.builder().token(bot_token).build()
        await telegram_app.initialize()

    asyncio.run(initialize_bot())
else:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
