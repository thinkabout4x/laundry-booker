import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
import os
from laundry_booker.user_handler import UserHandler

#token for bot
token = os.environ['token']

options = ['08:00-10:00','10:00-12:00','12:00-14:00','14:00-16:00','16:00-18:00','18:00-20:00','20:00-21:00']


if __name__ == "__main__":
    userhandler = UserHandler(15)
    userhandler.run()
    bot = telebot.TeleBot(token)

    @bot.callback_query_handler(func=lambda call: call.data in options)
    def options_callback_query(call: CallbackQuery):
        chat_id = call.message.chat.id   
        userhandler.users[chat_id].target_time = call.data
        bot.answer_callback_query(call.id, f'Answer is {call.data}')
        # remove keyboard
        bot.edit_message_reply_markup(chat_id, call.message.message_id) 
        process_final_step(call.message)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call: CallbackQuery):
        chat_id = call.message.chat.id
        if call.data == "Authorize" or call.data == "Change":
            msg = bot.send_message(chat_id, "Now you need to type your data:\nURI for your site:")
            bot.register_next_step_handler(msg, process_uri_enter_login_step)
        if call.data == "Time":
            bot.send_message(chat_id, 'Please choose from this options:', reply_markup = book_time_markup())
        if call.data == "Start":
            msg = bot.send_message(chat_id, f'Booking process started! Target time: {userhandler.users[chat_id].target_time}')
            result = userhandler.start_booking(chat_id)
            if result is not None:
                if result.isbooked:
                    bot.send_message(chat_id, f'Successfully book time for you! Day: {result.day} Target time: {result.time}')
                else:
                    bot.send_message(chat_id, f'Didnt book time, try later...')
            else:
                bot.send_message(chat_id, f'Something went wrong with your booking, please check your input data')
                welcome(call.message)
        if call.data == "Stop":
            msg = bot.send_message(chat_id, f'Booking process stopped!')
            userhandler.stop_booking(chat_id)        
            
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
    
    def process_uri_enter_login_step(message: Message):
        try:
            chat_id = message.chat.id
            userhandler.append_user(chat_id, message.text)
            msg = bot.reply_to(message, 'Login for your site:')
            bot.register_next_step_handler(msg, process_login_enter_password_step)
        except Exception as e:
            print(e)
            bot.reply_to(message, 'Can\'t process your uri')

    def process_login_enter_password_step(message: Message):
        try:
            chat_id = message.chat.id
            user = userhandler.users[chat_id]
            user.login = message.text
            msg = bot.reply_to(message, 'Password for your site:')
            bot.register_next_step_handler(msg, process_password_enter_time_step)
        except Exception as e:
            print(e)
            bot.reply_to(message, 'Can\'t process your login')

    def process_password_enter_time_step(message: Message):
        try:
            chat_id = message.chat.id
            user = userhandler.users[chat_id]
            user.password = message.text
            bot.reply_to(message, 'Target booking time:')
            bot.send_message(chat_id, 'Please choose from this options:', reply_markup = book_time_markup())
        except Exception as e:
            print(e)
            bot.reply_to(message, 'Can\'t process your password')

    def process_final_step(message: Message):
        try:
            chat_id = message.chat.id
            user = userhandler.users[chat_id]
            bot.send_message(chat_id, 'Your data: 1) uri: '+ user.uri + ' 2) Login: '+ user.login + " 3) Password: " + user.password + ' 4) Target time: '+ user.target_time + ' was succesfully added!')
            welcome(message)
        except Exception as e:
            print(e)
            bot.reply_to(message, 'Can\'t process your target time')

    @bot.message_handler(commands=['start', 'help'])
    def welcome(message: Message):
        chat_id = message.chat.id
        if chat_id in userhandler.users:
            bot.send_message(message.chat.id, "Hello dear user! What you want to do?", reply_markup = aut_user_markup())
        else:
            bot.send_message(message.chat.id, "This is a bot to book your Pesula! You need to share credentials to proceed", reply_markup = authorize_markup())


    bot.infinity_polling()