import telebot
from flask import Flask
import threading
import os
from openai import OpenAI

# ===== ТВОИ ДАННЫЕ =====
TELEGRAM_TOKEN = "8629154850:AAGni8Nj2iqjNBbGfwlD72ufx7nKIJPdywQ"
DEEPSEEK_KEY = "sk-7be62ec2122d4984b94f51aac9057b50"
# ========================

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")

app = Flask(__name__)

@app.route('/')
def home():
    return "GameDev Agent with AI работает!"

# Системный промпт — как бот должен себя вести
SYSTEM_PROMPT = """
Ты — опытный GameDev-агент. Помогаешь с:
- написанием кода для игр (Python, C#, C++, GDScript)
- игровыми механиками, физикой, AI
- идеями для игр
- движками Unity, Unreal, Godot, Pygame
Отвечай подробно, с примерами. Будь дружелюбным.
"""

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎮 **GameDev AI Agent**\n\nЯ помогаю с кодом и играми. Задавай вопросы!")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Отправляем запрос в DeepSeek
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ]
        )
        
        answer = response.choices[0].message.content
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
