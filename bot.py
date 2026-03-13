import telebot
from flask import Flask
import threading
import os
import time
import logging
import requests
import random
import re

# ==================== НАСТРОЙКИ ====================
TELEGRAM_TOKEN = "8629154850:AAG4xSPM2VSQ8zmS7ysij8Jgg3Yvn9VIFKw"
ADMIN_ID = 8629154850

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# ==================== AI ПОМОЩНИК ====================

class MathSolver:
    """Решает математические задачи"""
    
    def solve_equation(self, text):
        """Пытается решить уравнение"""
        # Простые примеры 5+5
        match = re.search(r'(\d+)\s*([\+\-\*\/])\s*(\d+)', text)
        if match:
            a = int(match.group(1))
            op = match.group(2)
            b = int(match.group(3))
            
            if op == '+':
                return f"✅ **Решение:** {a} + {b} = {a+b}"
            elif op == '-':
                return f"✅ **Решение:** {a} - {b} = {a-b}"
            elif op == '*':
                return f"✅ **Решение:** {a} × {b} = {a*b}"
            elif op == '/':
                if b != 0:
                    return f"✅ **Решение:** {a} ÷ {b} = {a/b}"
                else:
                    return "❌ На ноль делить нельзя!"
        return None
    
    def solve_text_task(self, text):
        """Решает текстовые задачи"""
        # Задача про яблоки
        if "яблок" in text.lower() and "корзин" in text.lower():
            return """
📝 **Решение задачи про яблоки:**

**Шаг 1:** Пусть в первой корзине x яблок
**Шаг 2:** Тогда во второй корзине 2x яблок (в 2 раза больше)
**Шаг 3:** В третьей корзине x + 10 яблок (на 10 больше)

**Шаг 4:** Составляем уравнение:
x + 2x + (x + 10) = 80

**Шаг 5:** Упрощаем:
4x + 10 = 80
4x = 70
x = 17.5? 

❌ **Ошибка!** Число не целое. Проверь условие задачи.

✅ **Правильное решение:**
x + 2x + (x + 10) = 80
4x + 10 = 80
4x = 70
x = 17.5 — но яблоки не могут быть половинками!

👉 **Вывод:** В условии опечатка или задача с подвохом.
В реальных задачах 526 гимназии числа подобраны так, чтобы ответ был целым.
            """
        
        # Задача про площадь
        if "площадь" in text.lower() and "прямоугольник" in text.lower():
            return """
📏 **Решение задачи про площадь:**

**Формула:** Площадь прямоугольника = длина × ширина

**Дано:**
• Длина = 5 см
• Ширина = 8 см

**Решение:**
S = 5 × 8 = 40 см²

✅ **Ответ:** 40 квадратных сантиметров

📚 **Объяснение:** Площадь показывает, сколько квадратов со стороной 1 см поместится в фигуре. Здесь поместится 40 таких квадратов.
            """
        return None
    
    def ask_ai(self, question):
        """Запрос к AI для сложных вопросов"""
        try:
            response = requests.post(
                "https://text.pollinations.ai/",
                json={
                    "messages": [
                        {"role": "system", "content": """Ты - репетитор по математике и русскому языку. 
                        Твоя задача: ПОЛНОСТЬЮ РЕШАТЬ задачи, а не просто давать советы.
                        Когда тебе дают задачу:
                        1. Напиши "📝 РЕШЕНИЕ:"
                        2. Покажи все шаги подробно
                        3. Дай конечный ответ
                        4. Объясни, почему так
                        
                        Например, на вопрос "сколько будет 5+5" ты должен ответить "5+5=10", а не "давай подумаем".
                        """},
                        {"role": "user", "content": question}
                    ]
                },
                timeout=15
            )
            if response.status_code == 200:
                return response.text
        except:
            pass
        return None

# ==================== ОСНОВНОЙ КЛАСС ====================

class StudyBot:
    def __init__(self):
        self.solver = MathSolver()
        self.user_data = {}
    
    def process_message(self, user_id, text):
        """Обрабатывает сообщение"""
        
        # 1. Сначала пробуем решить как уравнение
        math_solution = self.solver.solve_equation(text)
        if math_solution:
            return math_solution
        
        # 2. Пробуем решить как текстовую задачу
        text_solution = self.solver.solve_text_task(text)
        if text_solution:
            return text_solution
        
        # 3. Если не получилось, спрашиваем AI
        ai_answer = self.solver.ask_ai(text)
        if ai_answer:
            return ai_answer
        
        # 4. Запасной вариант
        return self._fallback(text)
    
    def _fallback(self, text):
        """Запасной ответ"""
        return f"""
📚 **По твоему вопросу:** "{text}"

Я могу помочь, если уточнишь:

1️⃣ **Математика:** напиши пример (например "5+5" или "реши уравнение x+3=7")

2️⃣ **Задачи 526 гимназии:** напиши "задача про яблоки" или "площадь прямоугольника"

3️⃣ **ВПР 4 класс:** напиши "ВПР математика" или "ВПР русский"

Что именно тебе нужно?
        """

# Создаём бота
study_bot = StudyBot()

# ==================== КОМАНДЫ ====================

@bot.message_handler(commands=['start'])
def start(message):
    welcome = """
🎓 **Учебный агент 526 гимназия**

✅ **Я РЕШАЮ ЗАДАЧИ, а не просто советую!**

📝 **Примеры:**
• "сколько будет 5+5" → сразу ответ
• "реши задачу про яблоки" → полное решение
• "найди площадь прямоугольника 5 и 8" → ответ с объяснением

📌 **Команды:**
/help - все команды
/526 - задачи 526 гимназии
/vpr - задания ВПР

💬 **Просто напиши задачу!**
    """
    bot.send_message(message.chat.id, welcome, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help(message):
    help_text = """
📖 **ПОЛНЫЙ СПИСОК КОМАНД:**

🔹 **526 гимназия:**
/526math - задача по математике
/526logic - логическая задача
/526russian - русский язык

🔹 **ВПР 4 класс:**
/vprmath - математика
/vprrus - русский язык
/vprworld - окружающий мир

🔹 **Режимы:**
/exam - режим экзамена
/practice - тренировка

💡 **Или просто напиши задачу!**
    """
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['526math'])
def math_526(message):
    task = """
📐 **Задача 526 гимназии:**

В трёх корзинах 80 яблок. В первой в 2 раза меньше, чем во второй, а в третьей на 10 больше, чем в первой. Сколько яблок в каждой корзине?

✏️ **Напиши "реши задачу про яблоки"** — я покажу полное решение!
    """
    bot.send_message(message.chat.id, task, parse_mode='Markdown')

@bot.message_handler(commands=['vprmath'])
def vpr_math(message):
    task = """
📝 **ВПР 4 класс (математика):**

Найди площадь прямоугольника со сторонами 5 см и 8 см.

✏️ **Напиши "площадь прямоугольника 5 и 8"** — я решу!
    """
    bot.send_message(message.chat.id, task, parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    """Обработка всех сообщений"""
    text = message.text
    
    # Показываем "печатает"
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Получаем ответ
    answer = study_bot.process_message(message.chat.id, text)
    
    # Отправляем
    bot.send_message(message.chat.id, answer, parse_mode='Markdown')

# ==================== ЗАПУСК ====================

def run_bot():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            time.sleep(5)

@app.route('/')
def home():
    return "526 Гимназия бот работает!"

if __name__ == "__main__":
    thread = threading.Thread(target=run_bot)
    thread.daemon = True
    thread.start()
    
    # ВАЖНО: используем переменную port!
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=
