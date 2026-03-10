import telebot
from flask import Flask
import threading
import os

TOKEN = "8629154850:AAGni8Nj2iqjNBbGfwlD72ufx7nKIJPdywQ"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Бот работает!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👌 Всё работает!")

@bot.message_handler(func=lambda m: True)
def reply(message):
    bot.reply_to(message, f"Ты написал: {message.text}")

def run_bot():
    bot.polling()

thread = threading.Thread(target=run_bot)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
