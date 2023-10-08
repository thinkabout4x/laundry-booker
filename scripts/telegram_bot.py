import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

#token for bot
token = os.environ['token']

user_dict = {}

class User:
    def __init__(self, uri):
        # url for the site to book on
        self.uri = uri
        # log and password for site
        self.login = None
        self.password = None
        # target time for booking in string format (title to find on a web page)
        self.target_time = None

if __name__ == "__main__":
    bot = telebot.TeleBot(token)

    def authorize_markup():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Authorize", callback_data="Authorize"))
        return markup
    
    def aut_user_markup():
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(InlineKeyboardButton("Start looking for booking", callback_data="booking"),
                   InlineKeyboardButton("Change target time", callback_data="time"),
                   InlineKeyboardButton("Change data", callback_data="change"))
        return markup
    
    def process_uri_step(message):
        try:
            chat_id = message.chat.id
            user_dict[chat_id] = User(message.text)
            msg = bot.reply_to(message, 'Login for your site:')
            bot.register_next_step_handler(msg, process_login_step)
        except Exception as e:
            bot.reply_to(message, 'Can\'t process your uri')

    def process_login_step(message):
        try:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.login = message.text
            msg = bot.reply_to(message, 'Password for your site:')
            bot.register_next_step_handler(msg, process_password_step)
        except Exception as e:
            bot.reply_to(message, 'Can\'t process your login')

    def process_password_step(message):
        try:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.password = message.text
            msg = bot.reply_to(message, 'Target booking time:')
            bot.register_next_step_handler(msg, process_booking_time_step)
        except Exception as e:
            bot.reply_to(message, 'Can\'t process your password')

    def process_booking_time_step(message):
        try:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.target_time = message.text
            bot.send_message(chat_id, 'Your data: 1) uri: '+ user.uri + ' 2) Login: '+ user.login + " 3) Password: " + user.password + ' 4) Target time: '+ user.target_time + ' was succesfully added!')
        except Exception as e:
            bot.reply_to(message, 'Can\'t process your target time')

    
    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == "Authorize":
            msg = bot.send_message(call.message.chat.id, "Now you need to type your data:\nURI for your site:")
            bot.register_next_step_handler(msg, process_uri_step)

    @bot.message_handler(commands=['start', 'help'])
    def welcome(message):
        chat_id = message.chat.id
        if chat_id in user_dict:
            bot.send_message(message.chat.id, "Hello dear user! What you want to do?", reply_markup = aut_user_markup())
        else:
            bot.send_message(message.chat.id, "This is a bot to book your Pesula! You need to share credentials to proceed", reply_markup = authorize_markup())


    # Enable saving next step handlers to file "./.handlers-saves/step.save" with 2 sec delay.
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()

    bot.infinity_polling()