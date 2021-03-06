import logging
from quart import jsonify
from app import API_ID, API_HASH, DB_URL
from telethon import TelegramClient
from telethon.tl.functions.messages import CreateChatRequest

from alchemysession import AlchemySessionContainer
container = AlchemySessionContainer(DB_URL)
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
        if hasattr(e, 'code'):
            code = e.code
        else:
            code = 500
        return jsonify({'message': message}), code

    poolsClient = {}

    @staticmethod
    async def get_client(phone):
        if phone in TelegramService.poolsClient:
            client = TelegramService.poolsClient[phone]
        else:
            session = container.new_session(phone)
            client = TelegramClient(session, API_ID, API_HASH)
            #client = TelegramClient(phone, API_ID, API_HASH)
            TelegramService.poolsClient[phone] = client

        await client.connect()
        return client

    @staticmethod
    async def close(client):
        if client:
            await client.disconnect()

    @staticmethod
    async def create_group(phone, code, token, group_name, members):
        try:
            client = await TelegramService.get_client(phone)
            await client.sign_in(phone, code, phone_code_hash=token)
            if await client.is_user_authorized():
                await client(CreateChatRequest(
                    users=members,
                    title=group_name
                ))
                return {}, 201
            else:
                return {'message': 'user not authorized'}, 401
        except Exception as e:
            return TelegramService.handle_error(e)

