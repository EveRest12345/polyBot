import telebot

bot = telebot.TeleBot('956984356:AAG0rg76nok4L6CtkgINb8ChESqw1uAyX7g')

@bot.message_handler(content_types= 'text')
def send_news(message):
    bot.send_message(message.chat.id, 'https://vk.com/newsbot1?w=wall-181851081_2%2Fall')


bot.polling( none_stop= True)