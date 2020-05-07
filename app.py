import os
from quart import Quart

app = Quart(__name__)
app.secret_key = os.environ['TELEGRAM_TOKEN']

API_ID = os.environ['TELEGRAM_ID']
API_HASH = os.environ['TELEGRAM_HASH']

DB_URL = os.environ['DB_URL']


