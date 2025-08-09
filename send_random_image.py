# kittybot/send_random_image.py
import requests
from telebot import TeleBot, types


bot = TeleBot(token='8422173125:AAEt3pY9URFZcl8HErXBhdQN7PKNUKgjOiw')

URL = 'https://api.thecatapi.com/v1/images/search'

# Код запроса к thecatapi.com и обработку ответа обернём в функцию:
def get_new_image():
    response = requests.get(URL).json()
    random_cat = response[0].get('url')
    return random_cat


# Добавляем хендлер для команды /newcat:
@bot.message_handler(commands=['newcat'])
def new_cat(message):
    chat = message.chat
    bot.send_photo(chat.id, get_new_image())


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = chat.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(  # Первая строка кнопок.
        types.KeyboardButton('Который час?'),  # Создаём первую кнопку в строке.
        types.KeyboardButton('Определи мой ip'),  # Создаём вторую кнопку в строке.
    )
    keyboard.row(  # Вторая строка кнопок.
        types.KeyboardButton('/random_digit'),  # Создаём кнопку в строке.
    )
    
    bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо, что вы включили меня, {name}!',
        reply_markup=keyboard,  # Отправляем пользователю текстовый ответ и клавиатуру.
    )

@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text='Привет, я KittyBot!')

bot.polling()
