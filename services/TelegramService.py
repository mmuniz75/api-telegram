import logging
from quart import jsonify
from app import client

logger = logging.Logger('catch_all')


class TelegramService:

    @staticmethod
    async def add_phone(phone):
        try:
            request = await client.send_code_request(phone)
            return jsonify({'token': request.phone_code_hash}), 201
        except Exception as e:
            return TelegramService.handle_error(e)

    @staticmethod
    async def send_message(phone, text, group_id, code, token):
        try:
            await client.sign_in(phone, code, phone_code_hash=token)
            if await client.is_user_authorized():
                await client.send_message(group_id, text)
                return {}, 200
            else:
                return {'message': 'user not authorized'}, 401
        except Exception as e:
            return TelegramService.handle_error(e)

    @staticmethod
    def handle_error(e):
        logger.error(e, exc_info=True)
        message = e.args[0]
        return jsonify({'message': message}), e.code
