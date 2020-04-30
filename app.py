import os
from quart import Quart

from telethon import TelegramClient
from telethon.sessions import StringSession

app = Quart(__name__)
app.secret_key = os.environ['TELEGRAM_TOKEN']

API_ID = os.environ['TELEGRAM_ID']
API_HASH= os.environ['TELEGRAM_HASH']

client = TelegramClient(StringSession(), API_ID, API_HASH)
