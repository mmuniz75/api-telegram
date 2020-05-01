from services.TelegramService import TelegramService
from quart import request
from app import app


@app.route('/users', methods=['POST'])
async def login():
    form = await request.json
    return await TelegramService.login(form['phone'])


@app.route('/messages', methods=['POST'])
async def send_messages():
    form = await request.json
    header = request.headers
    return await TelegramService.send_message(header['phone'], form['text'], form['groupId'], header['code'], header['token'])


@app.route('/groups', methods=['POST'])
async def create_groups():
    form = await request.json
    header = request.headers
    return await TelegramService.create_group(header['phone'], header['code'], header['token'],
                                              form['groupName'], form['membersName'])


@app.route('/users/logout', methods=['POST'])
async def logout():
    form = await request.json
    return await TelegramService.logout(form['phone'])

