import telebot
from flask import Flask
import threading
import os
import requests
import json

# ===== ТВОИ ДАННЫЕ =====
TELEGRAM_TOKEN = "8629154850:AAH5bI-h5NE4Mfj2MzSZWxKm4ddlJZld5Pw"
OPENROUTER_KEY = "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"
# ========================

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)
@app.route('/')
def home():
    return "GameDev Agent работает!"

def ask_ai(question):
    try:
        print(f"🤖 Запрос: {question}")
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Ты — дружелюбный GameDev-агент. Помогаешь с кодом, играми, идеями. Отвечай просто и понятно."},
                    {"role": "user", "content": question}
                ]
            })
        )
        
        print(f"📦 Статус ответа: {response.status_code}")
        result = response.json()
        print(f"📦 Ответ OpenRouter: {result}")
        
        # Проверяем, есть ли ошибка
        if "error" in result:
            return f"❌ Ошибка OpenRouter: {result['error']['message']}"
        
        # Проверяем, есть ли choices
        if "choices" not in result:
            return f"❌ Странный ответ от AI: {result}"
        
        return result['choices'][0]['message']['content']
        
    except Exception as e:
        return f"❌ Ошибка при запросе: {str(e)}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎮 **GameDev AI Agent**\n\nПривет! Я помогаю с кодом и играми. Просто напиши мне что хочешь 🤖")

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
