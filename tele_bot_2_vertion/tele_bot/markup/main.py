""" Пример сообщения с разными стилями шрифтов:
    - жирный
    - наклонный
    - ссылка
    - однострочный код
    - многострочный код

    А так же как прикрепить картинку под текст
"""
from logging import getLogger

from telegram import ParseMode
from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from echo.config import load_config
from echo.utils import debug_requests


config = load_config()

logger = getLogger(__name__)


@debug_requests
def bold_text_md(update: Update, context: CallbackContext):
    update.message.reply_text(
        '*Жирный* шрифт',
        parse_mode=ParseMode.MARKDOWN,
    )


@debug_requests
def bold_text_html(update: Update, context: CallbackContext):
    update.message.reply_text(
        '<b>Жирный</b> шрифт',
        parse_mode=ParseMode.HTML,
    )


@debug_requests
def italic_text_md(update: Update, context: CallbackContext):
    update.message.reply_text(
        '_Наклонный_ шрифт. Комбинировать с _*жирным*_ *_нельзя_* :(',
        parse_mode=ParseMode.MARKDOWN,
    )


@debug_requests
def italic_text_html(update: Update, context: CallbackContext):
    update.message.reply_text(
        '<i>Наклонный</i> шрифт',
        parse_mode=ParseMode.HTML,
    )


@debug_requests
def text_with_url_md(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Подпишись на мой [канал](https://www.youtube.com/channel/UCAlRksF5338XmSMbwS3W7eA/)! '
        'Там много информации для самообразования',
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


@debug_requests
def text_with_url_html(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Подпишись на мой <a href="https://www.youtube.com/channel/UCAlRksF5338XmSMbwS3W7eA/">канал</a>! '
        'Там много информации для самообразования',
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


@debug_requests
def code_md(update: Update, context: CallbackContext):
    text = [
        'Примеры с кодом:',
        '',
        'Код на одной строке: `update.message.reply_text()`',
        '',
        'Код на нескольких строках:',
        '```',
        'update.message.reply_text(',
        '   "хех",',
        '   parse_mode=ParseMode.MARKDOWN,',
        ')',
        '```',
    ]
    update.message.reply_text(
        text='\n'.join(text),
        parse_mode=ParseMode.MARKDOWN,
    )


@debug_requests
def code_html(update: Update, context: CallbackContext):
    text = [
        'Примеры с кодом:',
        '',
        'Код на одной строке: <code>update.message.reply_text()</code>',
        '',
        'Код на нескольких строках:',
        '<pre>',
        'update.message.reply_text(',
        '   "хех",',
        '   parse_mode=ParseMode.HTML,',
        ')',
        '</pre>',
    ]
    update.message.reply_text(
        text='\n'.join(text),
        parse_mode=ParseMode.HTML,
    )


@debug_requests
def image_hack_html(update: Update, context: CallbackContext):
    text = [
        'бла-бла <a href="https://picsum.photos/200/300">&#8205;</a>',
        'тут может быть любое количество текста, главное чтобы картинка была <b>первой</b> ссылкой '
        'во всём тексте, и внутри тега "a" был невидимый пробел',
    ]
    update.message.reply_text(
        text='\n'.join(text),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=False,
    )


@debug_requests
def echo_handler(update: Update, context: CallbackContext):
    text = [
        'Возможности Telegram для разметки сообщений:',
        '',
        '*MarkDown*',
        '/bold1 -- жирный шрифт',
        '/italic1 -- наклонный шрифт',
        '/url1 -- ссылка в тексте',
        '/code1 -- работа с кодом',
        '',
        '*HTML*',
        '/bold2 -- жирный шрифт',
        '/italic2 -- наклонный шрифт',
        '/url2 -- ссылка в тексте',
        '/code2 -- работа с кодом',
        '/img -- хак: картинка под текстом',
    ]
    update.message.reply_text(
        text='\n'.join(text),
        parse_mode=ParseMode.MARKDOWN,
    )


def main():
    logger.info('Started Markup-Bot')
    updater = Updater(
        token=config.TG_TOKEN,
        base_url=config.TG_API_URL,
        use_context=True,
    )

    # Произвести демонстрацию разного форматирования
    updater.dispatcher.add_handler(CommandHandler('bold1', bold_text_md))
    updater.dispatcher.add_handler(CommandHandler('bold2', bold_text_html))
    updater.dispatcher.add_handler(CommandHandler('italic1', italic_text_md))
    updater.dispatcher.add_handler(CommandHandler('italic2', italic_text_html))
    updater.dispatcher.add_handler(CommandHandler('url1', text_with_url_md))
    updater.dispatcher.add_handler(CommandHandler('url2', text_with_url_html))
    updater.dispatcher.add_handler(CommandHandler('code1', code_md))
    updater.dispatcher.add_handler(CommandHandler('code2', code_html))
    updater.dispatcher.add_handler(CommandHandler('img', image_hack_html))

    # Если ничего не подошло - отправить список команд
    updater.dispatcher.add_handler(MessageHandler(Filters.all, echo_handler))

    updater.start_polling()
    updater.idle()
    logger.info('Stopped Markup-Bot')


if __name__ == '__main__':
    main()
