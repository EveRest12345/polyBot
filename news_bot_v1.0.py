import vk_api
import telebot

bot = telebot.TeleBot('956984356:AAG0rg76nok4L6CtkgINb8ChESqw1uAyX7g')

def main():


    url = 'https://vk.com/newsbot1?w=wall-181851081_'

    def vk_s():
        login, password = '*******', '*****'
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
        last_id = 2
        i = 0
        items = vk_s()['items']
        print(items)
        items.reverse()
        for i in items:
            print(items[i]['id'])
            if items[i]['id'] > last_id:
                last_id = items[i]['id']
                return last_id



    @bot.message_handler(content_types='text')
    def send_news(message):
        bot.send_message(message.chat.id, url+str(chek_id()))

    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()
