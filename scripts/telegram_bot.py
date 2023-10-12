import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

#token for bot
token = os.environ['token']

options = ['08:00-10:00','10:00-12:00','12:00-14:00','14:00-16:00','16:00-18:00','18:00-20:00','20:00-21:00']

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

    @bot.callback_query_handler(func=lambda call: call.data in options)
    def options_callback_query(call):
        chat_id = call.message.chat.id   
        user_dict[chat_id].target_time = call.data
        bot.answer_callback_query(call.id, f'Answer is {call.data}')
        process_final_step(call.message)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        chat_id = call.message.chat.id
        if call.data == "Authorize" or call.data == "Change":
            msg = bot.send_message(chat_id, "Now you need to type your data:\nURI for your site:")
            bot.register_next_step_handler(msg, process_uri_enter_login_step)
        if call.data == "Time":
            bot.send_message(chat_id, 'Please choose from this options:', reply_markup = book_time_markup())
        if call.data == "Start":
            msg = bot.send_message(chat_id, f'Booking process started! Target time: {user_dict[chat_id].target_time}')

    def authorize_markup():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Authorize", callback_data="Authorize"))
        return markup
    
    def aut_user_markup():
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(InlineKeyboardButton("Start looking for booking", callback_data="Start"),
                   InlineKeyboardButton("Stop booking process", callback_data="Stop"),
                   InlineKeyboardButton("Change target time", callback_data="Time"),
                   InlineKeyboardButton("Change data", callback_data="Change"))
        return markup
    
    def book_time_markup():
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        buttons = []
        for option in options:
            buttons.append(InlineKeyboardButton(option, callback_data=option))
        markup.add(*buttons)
        return markup
    
    def process_uri_enter_login_step(message):
        try:
            chat_id = message.chat.id
            user_dict[chat_id] = User(message.text)
            msg = bot.reply_to(message, 'Login for your site:')
            bot.register_next_step_handler(msg, process_login_enter_password_step)
        except Exception as e:
            print(e)
            bot.reply_to(message, 'Can\'t process your uri')

    def process_login_enter_password_step(message):
        try:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.login = message.text
            msg = bot.reply_to(message, 'Password for your site:')
            bot.register_next_step_handler(msg, process_password_enter_time_step)
        except Exception as e:
            print(e)
            bot.reply_to(message, 'Can\'t process your login')

    def process_password_enter_time_step(message):
        try:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.password = message.text
            bot.reply_to(message, 'Target booking time:')
            bot.send_message(chat_id, 'Please choose from this options:', reply_markup = book_time_markup())
        except Exception as e:
            print(e)
            bot.reply_to(message, 'Can\'t process your password')

    def process_final_step(message):
        try:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            bot.send_message(chat_id, 'Your data: 1) uri: '+ user.uri + ' 2) Login: '+ user.login + " 3) Password: " + user.password + ' 4) Target time: '+ user.target_time + ' was succesfully added!')
            welcome(message)
        except Exception as e:
            print(e)
            bot.reply_to(message, 'Can\'t process your target time')

    @bot.message_handler(commands=['start', 'help'])
    def welcome(message):
        chat_id = message.chat.id
        if chat_id in user_dict:
            bot.send_message(message.chat.id, "Hello dear user! What you want to do?", reply_markup = aut_user_markup())
        else:
            bot.send_message(message.chat.id, "This is a bot to book your Pesula! You need to share credentials to proceed", reply_markup = authorize_markup())


    bot.infinity_polling()