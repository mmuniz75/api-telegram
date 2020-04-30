from services.TelegramService import TelegramService
from quart import request, jsonify
from app import app


@app.route('/users', methods=['POST'])
async def add_phone():
    form = await request.json
    return await TelegramService.add_phone(form['phone'])


@app.route('/users/<string:phone>', methods=['PUT'])
async def set_code(phone):
    form = await request.json
    return await TelegramService.set_code(phone, form['code'], form['token'])
