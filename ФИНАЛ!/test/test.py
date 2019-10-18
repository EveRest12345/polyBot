import telebot
bot = telebot.TeleBot("914034914:AAEE2H0iw3d-yAKXMo5kucfL2ecfnUM4jNI")
@bot.message_handler(commands=['start'])
def say_hello(message):
    msg = bot.send_message(message.chat.id, 'Привет, я PolyBot. Я расскажу тебе об актуальных мероприятиях и помогу зарегистрироваться на них.')
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)

@bot.message_handler(commands=['help'])
def send_help(message):
    msg=bot.send_message(message.chat.id, 'Список команд:\n'
                                          '/start - Команда приветствия \n'
                                          '/Register - Регистрация на мероприятия \n'
                                          '/cancel - Отмена регистрации \n'
                                          '/news - Узнать новости \n'
                                          '/help - Список команд')
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока')

@bot.message_handler(commands=['button'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)
bot.polling()