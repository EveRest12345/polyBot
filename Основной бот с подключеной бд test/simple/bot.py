from logging import getLogger

from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters

from echo.config import load_config
from echo.utils import debug_requests


config = load_config()

logger = getLogger(__name__)


@debug_requests
def message_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    if user:
        name = user.first_name
    else:
        name = 'аноним'

    text = update.effective_message.text
    reply_text = f'Привет, {name}!\n\n{text}'

    update.message.reply_text(
        text=reply_text,
    )


def main():
    logger.info('Start')
    updater = Updater(
        token=config.TG_TOKEN,
        base_url=config.TG_API_URL,
        use_context=True,
    )

    handler = MessageHandler(Filters.all, message_handler)
    updater.dispatcher.add_handler(handler)

    updater.start_polling()
    updater.idle()
    logger.info('Finish')


if __name__ == '__main__':
    main()
