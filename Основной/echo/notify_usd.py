from logging import getLogger

from telegram import Bot

from apis.cbrf import get_rate
from apis.cbrf import CentralBankError
from echo.config import load_config


config = load_config()

logger = getLogger(__name__)


def main():
    try:
        item = get_rate()
    except CentralBankError:
        logger.exception('Ошибка при получении курса $:')
        item = None

    if item:
        message = f'Курс {item.name} = {item.rate} руб.'
    else:
        message = 'Ошибка при поиске курса'

    bot = Bot(
        token=config.TG_TOKEN,
        base_url=config.TG_API_URL,
    )
    bot.send_message(
        chat_id=config.USD_NOTIFY_USER_ID,
        text=message,
    )
    logger.info('Success: %s', message)


if __name__ == '__main__':
    main()
