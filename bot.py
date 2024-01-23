from telebot import TeleBot
from config import BOT_TOKEN
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from quest import *

bot = TeleBot(BOT_TOKEN)

help_message = '''Я - квест "Попробуй понравиться Миранде Присли", составленный по фильму "Дьявол носит Prada".

Вот что я умею:
/help - узнать обо мне
/quest - начать проходить квест
'''

markup1 = ReplyKeyboardMarkup(resize_keyboard=True)
markup1.add(KeyboardButton('/quest'))
markup1.add(KeyboardButton('/help'))
@bot.message_handler(commands=['start'])
def bot_start(message):
    bot.send_message(message.chat.id,
                    text=f"Привет, {message.from_user.first_name}!\n"
                         f"Чтобы начать прохождение квеста, жми на /quest.\n"
                         f"/help - узнать обо мне", reply_markup=markup1
                    )

@bot.message_handler(commands=['help'])
def bot_help(message):
    bot.send_message(message.chat.id,
                     text=help_message, reply_markup=markup1
                     )

class Player():
    def __init__(self, id=None, location=None):
        self.id = id
        self.location = location

data = {}
player = Player()
player.location = "start"
@bot.message_handler(commands=['quest'])
def quest(message):
    global data, player
    player.id = message.from_user.id
    data = {player.id: player.location}
    player.location = data[player.id]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(locations[player.location]["markup"][0]))

    msg = bot.reply_to(message, text=locations[player.location]["description"], reply_markup=markup)
    with open(locations[player.location]["photo"], 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    bot.register_next_step_handler(msg, process_next_step)
def process_next_step(message):
    global data, player
    player.id = message.from_user.id
    player.location = locations[player.location]["options"][message.text]
    data[player.id] = player.location

    if "options" in locations[player.location]:
        markup2 = ReplyKeyboardMarkup(resize_keyboard=True)
        markup2.add(KeyboardButton(locations[player.location]["markup"][0]))
        markup2.add(KeyboardButton(locations[player.location]["markup"][1]))

        msg = bot.reply_to(message, text=locations[player.location]["description"], reply_markup=markup2)
        bot.register_next_step_handler(msg, process_next_step)
        with open(locations[player.location]["photo"], 'rb') as photo:
            bot.send_photo(message.chat.id, photo)

    else:
        markup3 = ReplyKeyboardMarkup(resize_keyboard=True)
        markup3.add(KeyboardButton("/restart"))
        msg = bot.reply_to(message, text=locations[player.location]["description"])
        bot.send_message(message.chat.id,
                         text="Если хотите пройти квест заново, жмите на /restart", reply_markup=markup3)

@bot.message_handler(commands=['restart'])
def restart(message):
    global data, player
    player.location = "start"
    data = {player.id: player.location}
    markup4 = ReplyKeyboardMarkup(resize_keyboard=True)
    markup4.add(KeyboardButton("/quest"))
    bot.send_message(message.chat.id,
                     text="Теперь нажмите на /quest", reply_markup=markup4)



bot.polling()