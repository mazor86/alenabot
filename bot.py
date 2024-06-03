import telebot

API_TOKEN = '7124611334:AAGo85HXf52joAU_1dQO-b0V79x1nTO4tuY'

bot = telebot.TeleBot(API_TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()