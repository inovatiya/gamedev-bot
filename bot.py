import telebot
import os

TOKEN = "8629154850:AAGni8Nj2iqjNBbGfwlD72ufx7nKIJPdywQ"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ Бот работает на Render!")

@bot.message_handler(func=lambda m: True)
def reply(message):
    bot.reply_to(message, f"Ты написал: {message.text}")

bot.polling()
