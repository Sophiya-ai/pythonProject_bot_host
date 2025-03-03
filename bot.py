import telebot
import datetime
import time
import threading
import random

bot = telebot.TeleBot("your-bot-token")


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.reply_to(message, "Привет! Я чат-бот, который напомнит тебе пить")
    reminder_thread = threading.Thread(target=send_remainders, args=(message.chat.id,))
    reminder_thread.start()

@bot.message_handler(commands=["fact"])
def fact_message(message):
    list = ["**Вода составляет около 71% поверхности Земли","**Вода замерзает при 0°C и кипит при 100°C на уровне моря", "**Вода — единственное вещество, которое может существовать в трех состояниях: жидком, твердом и газообразном"]
    random_fact = random.choice(list)
    bot.reply_to(message, f"Лови факт о воде {random_fact}")

def send_remainders(chat_id):
    rem_1 = "09:00"
    rem_2 = "14:00"
    rem_3 = "18:10"
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == rem_1 or now == rem_2 or now == rem_3:
            bot.send_message(chat_id, "Напоминание - выпей воды")
            time.sleep(61)
        time.sleep(1)


bot.polling(non_stop=True)
