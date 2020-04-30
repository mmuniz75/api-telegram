from services.TelegramService import TelegramService
from quart import request, jsonify
from app import app


@app.route('/users', methods=['POST'])
async def addPhone():
    return jsonify({'message': 'ok'})
