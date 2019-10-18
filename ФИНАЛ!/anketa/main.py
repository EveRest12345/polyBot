from logging import getLogger
import telebot
import vk_api

from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters

from echo.config import load_config
from echo.utils import debug_requests
from anketa.validators import GENDER_MAP
from anketa.validators import gender_hru
from anketa.validators import validate_age
from anketa.validators import validate_gender
from anketa.validators import validate_mail
from anketa.validators import validate_phone
config = load_config()

logger = getLogger(__name__)
bot = telebot.TeleBot("914034914:AAEE2H0iw3d-yAKXMo5kucfL2ecfnUM4jNI")
# bot.message_handler(commands=['start'])
# def say_hello(message):
#    msg = bot.send_message(message.chat.id, 'Привет, я PolyBot. Я расскажу тебе об актуальных мероприятиях и помогу зарегистрироваться на них.')
'''
@bot.message_handler(commands=['help'])
def send_help(message):
    msg=bot.send_message(message.chat.id, 'Список команд:\n'
                                          '/start - Команда приветствия \n'
                                          '/Register - Регистрация на мероприятия \n'
                                          '/cancel - Отмена регистрации \n'
                                          '/news - Узнать новости \n'
                                          '/help - Список команд')
'''

file_id = 'id.txt'
url = 'https://vk.com/newsbot0?w=wall-181851081_'


def vk_s():
    login, password = '89500961053', 'idivles3420'

    vk_session = vk_api.VkApi(login, password)

    try:

        vk_session.auth(token_only=True)

    except vk_api.AuthError as error_msg:

        print(error_msg)

        return

    tools = vk_api.VkTools(vk_session)

    wall = tools.get_all('wall.get', 3, {'owner_id': -181851081})

    return wall


def chek_id():
    with open(file_id, 'rt') as file:
        last_id = int(file.read())
    print(last_id)

    items = vk_s()['items']

    # print(items)

    # items.reverse()

    for item in items:

        # print(item['id'])

        if item['id'] <= last_id:
            # last_id = item['id']

            # print(last_id)

            break
        with open(file_id, 'wt') as file:
            file.write(str(item['id']))

    return item['id']

@debug_requests
def send_news(update: Update, context: CallbackContext):
    update.message.reply_text(url + str(chek_id()))



'''
@debug_requests
def send_news(message):
    bot.send_message(message.chat.id, url + str(chek_id()))

#  bot.send_message(message.chat.id, url + str(chek_id()))
'''
@debug_requests
def do_help(update: Update, context: CallbackContext):
    update.message.reply_text('''Список команд:
                                /start - Команда приветствия 
                                /Registration - Регистрация на мероприятия
                                /news - Узнать новости 
                                /help - Список команд
    ''')

NAME, GENDER, AGE, GROUP, PHONE, MAIL, EVENT = range(7)

@debug_requests
def do_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="Привет, я PolyBot. Я расскажу тебе об актуальных мероприятиях и помогу зарегистрироваться на них. Что бы узнать что я умею введи /help"
    )

@debug_requests
def registration_handler(update: Update, context: CallbackContext):
    # Спросить на какое мероприятие
    update.message.reply_text(
        'Какое мероприятие:',
    )
    return EVENT
'''
@debug_requests
def start_handler(update: Update, context: CallbackContext):
    # Спросить имя
    update.message.reply_text(
        'Введи своё Ф.И.О чтобы продолжить:',
    )
    return NAME
'''
@debug_requests
def event_handler(update: Update, context: CallbackContext):
    # Получить на какое мероприятие
    context.user_data[EVENT] = update.message.text
    logger.info('user_data: %s', context.user_data)

    # Спросить имя
    update.message.reply_text(
        'Введи своё Ф.И.О чтобы продолжить:',
    )
    return NAME

@debug_requests
def name_handler(update: Update, context: CallbackContext):
    # Получить имя
    context.user_data[NAME] = update.message.text
    logger.info('user_data: %s', context.user_data)

    # Спросить пол
    genders = [f'{key} - {value}' for key, value in GENDER_MAP.items()]
    genders = '\n'.join(genders)
    update.message.reply_text(f'''
Выберите свой пол чтобы продолжить:
{genders}
''')
    # TODO: кнопки !
    return GENDER
#

@debug_requests
def age_handler(update: Update, context: CallbackContext):
    # Получить пол
    gender = validate_gender(text=update.message.text)
    if gender is None:
        update.message.reply_text('Пожалуйста, укажите корректный пол!')
        return GENDER

    context.user_data[GENDER] = gender
    logger.info('user_data: %s', context.user_data)

    # Спросить группу
    update.message.reply_text('''
Введите свою группу:
''')
    return GROUP

@debug_requests
def group_handler(update: Update, context: CallbackContext):
    # Получить ГРУППУ
    context.user_data[GROUP] = update.message.text
    # group = context.user_data[GROUP]
    # group = validate_gender(text=update.message.text)
    #if group is None:
    #    update.message.reply_text('Пожалуйста, укажите корректный пол!')
    #    return GENDER

   # context.user_data[GROUP] = group
    logger.info('user_data: %s', context.user_data)

    # Спросить телефон
    update.message.reply_text('''
Нам нужен твой телефон:
''')
    return PHONE


@debug_requests
def phone_handler(update: Update, context: CallbackContext):
    # Получить телефон
    phone = validate_phone(text=update.message.text)
    if phone is None:
        update.message.reply_text('Пожалуйста, укажите корректный номер телефона! Например: 89*********(11 цифр)')
        return PHONE

    context.user_data[PHONE] = phone
    logger.info('user_data: %s', context.user_data)

    # Спросить mail
    update.message.reply_text('''
Введите свой e-mail:
''')
    return MAIL


@debug_requests
def mail_handler(update: Update, context: CallbackContext):
    # Получить mail
    mail = validate_mail(text=update.message.text)
    if mail is None:
        update.message.reply_text('Пожалуйста, укажите корректный e-mail')
        return MAIL

    context.user_data[MAIL] = mail
    logger.info('user_data: %s', context.user_data)

    # Спросить возраст
    update.message.reply_text('''
Введите свой возраст:
''')
    return AGE

@debug_requests
def finish_handler(update: Update, context: CallbackContext):
    # Получить возраст
    age = validate_age(text=update.message.text)
    if age is None:
        update.message.reply_text('Пожалуйста, введите корректный возраст!')
        return AGE

    context.user_data[AGE] = age
    # logger.info('user_data: %s', context.user_data)

    # TODO: вот тут запись в базу финала
    # TODO 2: очистить `user_data`

    # Завершить диалог
    update.message.reply_text(f'''
Все данные успешно сохранены! 
Мероприятие: {context.user_data[EVENT]},
Вы: {context.user_data[NAME]}, пол: {gender_hru(context.user_data[GENDER])}, возраст: {context.user_data[AGE]}, группа: {context.user_data[GROUP]},
 ваш номер: {context.user_data[PHONE]} и почта {context.user_data[MAIL]}
''')
    from firebase import firebase
    event = context.user_data[EVENT]
    token ='/hackaton-9de63/' + event
    firebase = firebase.FirebaseApplication("https://hackaton-9de63.firebaseio.com/")
    data = {

        'Name': context.user_data[NAME],
        'Age': context.user_data[AGE],
        'Gender': gender_hru(context.user_data[GENDER]),
        'Group': context.user_data[GROUP],
        'Phone number':context.user_data[PHONE],
        'Email':context.user_data[MAIL],



    }
    result = firebase.post(token , data)
    print(result)
    return ConversationHandler.END


@debug_requests
def cancel_handler(update: Update, context: CallbackContext):
    """ Отменить весь процесс диалога. Данные будут утеряны
    """
    update.message.reply_text('Отмена. Для начала с нуля нажмите /Registration')
    return ConversationHandler.END


@debug_requests
def echo_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Упс, что то пошло не так. Попробуй ввести команду /help чтобы увидеть доступные команды')


def main():
    file_id = 'id.txt'
    url = 'https://vk.com/newsbot0?w=wall-181851081_'

    logger.info('Started Anketa-bot')
    updater = Updater(
        token=config.TG_TOKEN,
        base_url=config.TG_API_URL,
        use_context=True,
    )

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('Registration', registration_handler),
        ],
        states={
            EVENT: [
                MessageHandler(Filters.all, event_handler, pass_user_data=True),
            ],
            NAME: [
                MessageHandler(Filters.all, name_handler, pass_user_data=True),
            ],
            GENDER: [
                MessageHandler(Filters.all, age_handler, pass_user_data=True),
            ],
            GROUP: [
                MessageHandler(Filters.all, group_handler, pass_user_data=True),
            ],
            PHONE: [
                MessageHandler(Filters.all, phone_handler, pass_user_data=True),
            ],
            MAIL: [
                MessageHandler(Filters.all, mail_handler, pass_user_data=True),
            ],
            AGE: [
                MessageHandler(Filters.all, finish_handler, pass_user_data=True),
            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler),
        ],
    )














    news_handler = CommandHandler("news", send_news)
    help_handler = CommandHandler("help", do_help)
    start_handler = CommandHandler("start", do_start)

    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo_handler))
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(news_handler)
    updater.dispatcher.add_handler(start_handler)

    updater.start_polling()
    updater.idle()
    logger.info('Stopped Anketa-bot')


if __name__ == '__main__':
    main()