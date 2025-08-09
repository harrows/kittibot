# kittybot/kittybot.py
import os
import logging
import requests
from telebot import TeleBot, types
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise RuntimeError("Переменная окружения TOKEN не задана")


bot = TeleBot(TOKEN)
URL = 'https://api.thecatapi.com/v1/images/search'

def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        print(error)      
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat 

@bot.message_handler(commands=['newcat'])
def new_cat(message):
    chat = message.chat
    bot.send_photo(chat.id, get_new_image())


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = message.chat.first_name
    # Создаём объект клавиатуры:
    keyboard = types.ReplyKeyboardMarkup()
    # Создаём объект кнопки:
    button_newcat = types.KeyboardButton('/newcat')
    # Добавляем объект кнопки на клавиатуру:
    keyboard.add(button_newcat)

    bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}. Посмотри, какого котика я тебе нашёл',
        # Отправляем клавиатуру в сообщении бота: передаём объект клавиатуры
        # в параметр reply_markup объекта send_message.
        # Telegram-клиент "запомнит" клавиатуру и будет отображать её в интерфейсе бота.
        reply_markup=keyboard,
    )

    bot.send_photo(chat.id, get_new_image())


@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text='Привет, я KittyBot!')



bot.polling()