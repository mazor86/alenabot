import random
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '7224377423:AAEG4zgC1upN_XOmla-3k631BimfGhkmK-o'
ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
HANGMAN_GAME = 'Игра "Виселица"'
bot = telebot.TeleBot(TOKEN)
data = {
    'game': None,
    'answer': None
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я умный бот с играми. Выбери игру из главного меню.",
                     reply_markup=get_main_menu())


@bot.message_handler(func=lambda message: message.text == HANGMAN_GAME)
def hangman_game(message):
    answer = choose_word()
    data['game'] = HANGMAN_GAME
    data['answer'] = answer.upper()
    data['guessed_letters'] = []
    data['letters'] = [letter for letter in ALPHABET]
    data['attempts'] = 6

    reply = '_ ' * len(answer)

    bot.send_message(message.chat.id, "Игра виселица началась.")
    bot.send_message(
        message.chat.id,
        text=reply,
        reply_markup=get_keyboard())


@bot.message_handler(func=lambda message: message.text in ALPHABET)
def hangman_game_realise(message):
    guess = message.text
    data['letters'].remove(guess)
    data['guessed_letters'].append(guess)
    if guess not in data['answer']:
        data['attempts'] -= 1
        bot.send_message(message.chat.id, text="Неверная буква")
        print_hangman(message)
        bot.send_message(message.chat.id, text=display_word(), reply_markup=get_keyboard())
        if data['attempts'] == 0:
            bot.send_message(message.chat.id, f"Game over. Ты не угадал слово '{data['answer']}'", reply_markup=get_main_menu())
    else:
        bot.send_message(message.chat.id, text=display_word(), reply_markup=get_keyboard())

        if all(letter in data['guessed_letters'] for letter in data['answer']):
            bot.send_message(message.chat.id, text=f"Поздравляю! Ты угадал слово '{data['answer']}'.",
                             reply_markup=get_main_menu())


def get_keyboard():
    keyboard = [KeyboardButton(letter) for letter in data['letters']]
    markup = ReplyKeyboardMarkup(input_field_placeholder='Выберите букву')
    markup.add(*keyboard, row_width=8)
    return markup


def get_main_menu():
    main_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    main_menu.add(KeyboardButton(HANGMAN_GAME))
    return main_menu


def choose_word():
    words = ["виселица", "телеграмм", "бот", "друг", "игра", "телепатия", "зал", "фильтр", "башня", "кордебалет", "обещание", "клавиатура", "леденец", "абзац", "комбинация", "развлечение", "фундамент", "ресница", "самовар", "кондитер", "банк"]  # и т.д.
    return random.choice(words)


def display_word():
    word = data['answer']
    answer = data['guessed_letters']
    display = ""
    for letter in word:
        if letter in answer:
            display += letter + " "
        else:
            display += "_ "
    return display


def print_hangman(message):
    data['hangman_pic'] = [
"""
------
|    |
|   O
|   /|\\
|   / \\
|   
|   
----------
""",
"""
------
|    |
|   O
|   /|\\
|   /
|   
|    
----------
""",
"""
------
|    |
|   O
|   /|\\
|   
|   
|     
----------
""",
"""
------
|    |
|   O
|   /|
|   
|   
|   
----------
""",
"""
------
|    |
|   O
|    |
| 
|   
|    
----------
""",
"""
------
|    |
|   O
|
|
|
|
----------
""",
"""
------
|    |
|
|
|
|
|
----------
"""
    ]
    bot.send_message(message.chat.id, text=data['hangman_pic'][data['attempts']], reply_markup=get_keyboard())
bot.polling()