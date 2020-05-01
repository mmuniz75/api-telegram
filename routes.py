from services.TelegramService import TelegramService
from quart import request, jsonify
from app import app


@app.route('/users', methods=['POST'])
async def add_phone():
    form = await request.json
    return await TelegramService.add_phone(form['phone'])



@app.route('/messages', methods=['POST'])
async def send_messages():
    form = await request.json
    header = request.headers
    return await TelegramService.send_message(header['phone'], form['text'], form['groupId'], header['code'], header['token'])
