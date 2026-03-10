import telebot
from flask import Flask
import threading
import os
import google.generativeai as genai

# ===== ТВОИ ДАННЫЕ =====
TELEGRAM_TOKEN = "8629154850:AAH5bI-h5NE4Mfj2MzSZWxKm4ddlJZld5Pw"
GEMINI_KEY = "AIzaSyD1XxU76eOijI7Rr80W2Qj_pU6nwVLd5cQ"  # мой тестовый ключ
# ========================

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "GameDev Agent with Gemini работает!"

SYSTEM_PROMPT = """
Ты — опытный GameDev-агент. Помогаешь с:
- кодом для игр (Python, C#, C++, GDScript)
- игровыми механиками (физика, AI, анимации)
- идеями для игр и геймдизайном
- движками Unity, Unreal, Godot, Pygame

Отвечай подробно, с примерами кода. Будь дружелюбным.
"""

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎮 **GameDev AI Agent (Gemini)**\n\nЯ помогаю с кодом и играми. Задавай вопросы!")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = model.generate_content(SYSTEM_PROMPT + "\n\n" + message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

def run_bot():
    bot.polling()

thread = threading.Thread(target=run_bot)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
