import logging
from quart import jsonify
from app import client

logger = logging.Logger('catch_all')


class TelegramService:

    @staticmethod
    async def add_phone(phone):
        try:
            #client.session.filename = phone
            request = await client.send_code_request(phone)
            return jsonify({'token': request.phone_code_hash}), 201
        except Exception as e:
            return TelegramService.handle_error(e)

    @staticmethod
    async def set_code(phone, code, token):
        try:
            await client.sign_in(phone, code, phone_code_hash=token)
            return {}, 200
        except Exception as e:
            return TelegramService.handle_error(e)

    @staticmethod
    def handle_error(e):
        logger.error(e, exc_info=True)
        message = e.args[0]
        return jsonify({'message': message}), e.code