import telebot
from flask import Flask
import threading
import os
import g4f

# ===== ТВОИ ДАННЫЕ =====
TELEGRAM_TOKEN = "8629154850:AAG4xSPM2VSQ8zmS7ysij8Jgg3Yvn9VIFKw"
# ========================

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "GameDev Agent with g4f работает!"

def ask_ai(question):
    try:
        # Используем провайдера напрямую
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,  # правильный формат
            messages=[
                {"role": "system", "content": "Ты — дружелюбный GameDev-агент. Помогаешь с кодом, играми, идеями."},
                {"role": "user", "content": question}
            ],
            provider=g4f.Provider.Bing,  # можно заменить на другой
        )
        
        # Проверяем, что пришло
        if response:
            return str(response)
        else:
            return "❌ Пустой ответ от AI"
            
    except Exception as e:
        return f"❌ Ошибка AI: {str(e)}"

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
    while True:
        try:
            bot.polling()
        except:
            pass

thread = threading.Thread(target=run_bot)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0")
