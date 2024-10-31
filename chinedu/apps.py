from django.apps import AppConfig
import os
from telegram.ext import Application
from dotenv import load_dotenv
import asyncio

load_dotenv()


class ChineduConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chinedu'

   