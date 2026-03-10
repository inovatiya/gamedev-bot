import telebot
from flask import Flask
import threading
import os
from openai import OpenAI

# ===== ТВОИ ДАННЫЕ =====
TELEGRAM_TOKEN = "8629154850:AAH5bI-h5NE4Mfj2MzSZWxKm4ddlJZld5Pw"
OPENROUTER_KEY = "import telebot
from flask import Flask
import threading
import os
from openai import OpenAI

# ===== ТВОИ ДАННЫЕ =====
TELEGRAM_TOKEN = "8629154850:AAH5bI-h5NE4Mfj2MzSZWxKm4ddlJZld5Pw"
OPENROUTER_KEY = "твой_ключ_openrouter"
# ========================

client = OpenAI(
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1"
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

SYSTEM_PROMPT = "Ты — опытный GameDev-агент. Помогаешь с кодом для игр, игровыми механиками, идеями. Отвечай подробно, с примерами."

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎮 **GameDev AI Agent**\n\nЯ помогаю с кодом и играми. Задавай вопросы!")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ]
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

def run_bot():
    bot.polling()

thread = threading.Thread(target=run_bot)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)"
# ========================

client = OpenAI(
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1"
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

SYSTEM_PROMPT = "Ты — опытный GameDev-агент. Помогаешь с кодом для игр, игровыми механиками, идеями. Отвечай подробно, с примерами."

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎮 **GameDev AI Agent**\n\nЯ помогаю с кодом и играми. Задавай вопросы!")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ]
        )
        bot.reply_to(message, response.choices[0].message.content)
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
