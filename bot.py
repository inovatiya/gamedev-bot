import telebot
from flask import Flask
import threading
import os
import g4f

# ===== ТВОИ ДАННЫЕ =====
TELEGRAM_TOKEN = "8629154850:AAH5bI-h5NE4Mfj2MzSZWxKm4ddlJZld5Pw"
# ========================

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "GameDev Agent with g4f работает!"

def ask_ai(question):
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — дружелюбный GameDev-агент. Помогаешь с кодом, играми, идеями."},
                {"role": "user", "content": question}
            ],
        )
        return response
    except Exception as e:
        return f"❌ Ошибка AI: {e}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎮 **GameDev AI Agent**\n\nПривет! Я помогаю с кодом и играми. Просто напиши мне!")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        answer = ask_ai(message.text)
        bot.reply_to(message, answer)
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
