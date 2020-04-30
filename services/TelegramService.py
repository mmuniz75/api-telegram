import logging

logger = logging.Logger('catch_all')


class TelegramService:

    @staticmethod
    def addPhone(phone):
        try:
            logger.info(phone + "added")
        except Exception as e:
            logger.error(e, exc_info=True)



