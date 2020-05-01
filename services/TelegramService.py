import logging
from quart import jsonify
from app import API_ID, API_HASH
from telethon import TelegramClient

logger = logging.Logger('catch_all')


class TelegramService:

    @staticmethod
    async def login(phone):
        try:
            client = await TelegramService.get_client(phone)
            request = await client.send_code_request(phone)
            return jsonify({'token': request.phone_code_hash}), 201
        except Exception as e:
            return TelegramService.handle_error(e)
        finally:
            await TelegramService.close(client)

    @staticmethod
    async def send_message(phone, text, group_id, code, token):

        try:
            client = await TelegramService.get_client(phone)
            await client.sign_in(phone, code, phone_code_hash=token)
            if await client.is_user_authorized():
                await client.send_message(group_id, text)
                return {}, 200
            else:
                return {'message': 'user not authorized'}, 401
        except Exception as e:
            return TelegramService.handle_error(e)
        finally:
            await TelegramService.close(client)

    @staticmethod
    async def logout(phone):
        try:
            client = await TelegramService.get_client(phone)
            await client.log_out()
            del TelegramService.poolsClient[phone]
            return {}, 200
        except Exception as e:
            return TelegramService.handle_error(e)

    @staticmethod
    def handle_error(e):
        logger.error(e, exc_info=True)
        message = e.args[0]
        return jsonify({'message': message}), e.code

    poolsClient = {}

    @staticmethod
    async def get_client(phone):
        if phone in TelegramService.poolsClient:
            client = TelegramService.poolsClient[phone]
        else:
            client = TelegramClient(phone, API_ID, API_HASH)
            TelegramService.poolsClient[phone] = client

        await client.connect()
        return client

    @staticmethod
    async def close(client):
        if client:
            await client.disconnect()
