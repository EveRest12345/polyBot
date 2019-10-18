from logging import getLogger

from telegram import Bot

from apis.bittrex import BittrexClient
from apis.bittrex import BittrexError
from echo.config import load_config


logger = getLogger(__name__)


NOTIFY_PAIR = "USD-BTC"
NOTIFY_USER_ID = 720951086


def main():
    client = BittrexClient()

    try:
        current_price = client.get_last_price(pair=NOTIFY_PAIR)
        message = "{} = {}".format(NOTIFY_PAIR, current_price)
    except BittrexError:
        logger.error("BittrexError")
        message = "Произошла ошибка"

    config = load_config()
    bot = Bot(
        token=config.TG_TOKEN,
        base_url=config.TG_API_URL,
    )
    bot.send_message(
        chat_id=NOTIFY_USER_ID,
        text=message,
    )
    logger.info('Success: %s', message)


if __name__ == '__main__':
    main()
