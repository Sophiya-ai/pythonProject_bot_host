import telebot as t
import datetime as dt
import time
import threading
import random
from telebot import types

bot = t.TeleBot("7787729459:AAG-KkVnwGVy5cw_VsNMposKkyeI-2MUjNw")
user_data = {}
res = 2 / 3


def water_count(gender, m, h):
    if gender == "Ж":
        water = m * 30
        add_water = water * 0.1 * h
    else:
        water = m * 35
        add_water = water * 0.1 * h
    return (water + add_water) / 1000


def send_remainders(chat_id):
    rem_1 = "07:00"
    rem_2 = "14:00"
    rem_3 = "18:00"
    while True:
        now = dt.datetime.now().strftime("%H:%M")
        if now == rem_1:
            bot.send_message(chat_id, f"Напоминание - выпейте теплой воды {round(res,2)} л натощак")
            time.sleep(61)
        elif now == rem_2:
            bot.send_message(chat_id, f"Напоминание - выпейте воды {round(res,2)}  л ")
            time.sleep(61)
        elif now == rem_3:
            bot.send_message(chat_id, f"Напоминание - выпейте воды {round(res,2)}  л ")
            time.sleep(61)
        time.sleep(1)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message,
                 "Привет! Я чат-бот, который напомнит тебе пить. В меню есть команда /count рассчета количество воды "
                 "для твоих параметров. Я напомню тебе выпить её 3 раза в день (по умолчанию 2 л).")
    bot.reply_to(message,
                 "Используйте /help, чтобы увидеть команды ботика")
    reminder_thread = threading.Thread(target=send_remainders, args=(message.chat.id,))
    reminder_thread.start()


@bot.message_handler(commands=["fact"])
def fact(message):
    list = [
        "**В жару лучше пить холодную воду** -- Нет, температура воды должна быть выше 30 градусов. Холодная жидкость хуже утоляет жажду.",
        "**В день нужно пить 8-10 стаканов воды (по 220 мл)** -- Суточная норма жидкости состоит не только из чистой воды."
        "Она поступает в организм вместе с едой и позволяет удовлетворить около 40-50% потребностей.",
        "**Сладкий чай, кофе и газировка удовлетворяют потребности организма в воде** -- Нет, чай и кофе завариваются кипяченой водой, "
        "которая хуже усваивается организмом. В газировках содержится большое количество сахара и глюкозы, вызывающих последующую жажду.",
        "**Бутилированная вода полезнее любой другой** -- Нет, качество жидкости зависит от производителя, ее минерализации. "
        "Вода, прошедшая обработку в бытовой системе обратного осмоса в домашних условиях, является более чистой, чем бутилированная.",
        "**Вода помогает сбросить вес** -- В некоторых случаях жидкость позволяет заменить прием пищи или уменьшить ее количество. "
        "Теплая жидкость создает чувство насыщенности, продукты быстрее усваиваются. При этом вода не способна полноценно заменить приемы пищи — это приведет к общей слабости.",
        "**Ограничив себя в воде, можно снизить отечность** -- Нет, отеки возникают из-за недостатка жидкости в организме. Снизить отечность можно, "
        "регулярно употребляя суточную норму воды и занимаясь умеренными физическими нагрузками после консультации с врачом."]
    random_fact = random.choice(list)
    bot.reply_to(message, f"Лови факт о воде {random_fact}")


@bot.message_handler(commands=["help"])
def help_message(message):
    help_info = (
        "Список команд нашего бота-напоминалки:\n\n"
        "/start - запускает нашего ботика\n"
        "/fact - выдает интересный миф о потреблении воды и развенчивает его\n"
        "/count - подсчитывает необходимое именно вам количество воды\n"
        "/help - выдает перечень всех команд ботика\n\n"
        "Чтобы узнать подробности, нажмите на команду")
    bot.send_message(message.chat.id, help_info, parse_mode="MarkDown")


@bot.message_handler(commands=["count"])
def gender_mess(message):
    # простой вариант
    # bot.reply_to(message, "Укажите ваш пол (М/Ж):")
    # bot.register_next_step_handler(message, try_gender)

    #Создаем объект клавиатуры.
    # `one_time_keyboard=True`: Указывает, что клавиатура
    # будет скрыта после выбора одного из вариантов. Это удобно, чтобы не засорять
    # интерфейс пользователя
    # `resize_keyboard=True`: Позволяет автоматически изменять размер кнопок
    # под размер экрана устройства пользователя
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    #Создаем кнопки
    item1 = types.KeyboardButton('Мужчина')
    item2 = types.KeyboardButton('Женщина')

    #Добавляем созданные кнопки `item1` и `item2` на клавиатуру
    markup.add(item1, item2)

    #Отправляеv пользователю сообщение с текстом "..." и прикрепляем к нему клавиатуру `markup`
    msg = bot.reply_to(message, "Укажите ваш пол:", reply_markup=markup)
    bot.register_next_step_handler(msg, try_gender)


def try_gender(message):
    try:
        chat_id = message.chat.id
        gender = message.text.upper()
        if gender not in ["МУЖЧИНА", "ЖЕНЩИНА"]:
            raise ValueError("Введите корректный пол")
        user_data[chat_id] = {"Gender": gender}
        bot.reply_to(message, "Введите вес в кг:")
        bot.register_next_step_handler(message, try_m)
    except Exception as e:
        bot.reply_to(message, "Ошибка ввода! Попробуйте заново, введя команду /count")


def try_m(message):
    try:
        chat_id = message.chat.id
        m = float(message.text)
        user_data[chat_id]['Weight'] = m
        bot.reply_to(message, "Введите количество часов физической активности в сутки:")
        bot.register_next_step_handler(message, try_h)
    except ValueError:
        bot.reply_to(message, "Ошибка ввода! Вес должен быть числом! Попробуйте заново, введя команду /count")


def try_h(message):
    global res
    try:
        chat_id = message.chat.id
        h = float(message.text)
        user_data[chat_id]['Time'] = h
        gender = user_data[chat_id]['Gender']
        m = user_data[chat_id]['Weight']
        h = user_data[chat_id]['Time']
        w = water_count(gender, m, h)
        res = w / 3
        bot.reply_to(message, f"Ваша норма потребления воды (л/сутки): {w}")
        return res
    except ValueError:
        bot.reply_to(message,
                     "Ошибка ввода! Количество часов должно быть числом! Попробуйте заново, введя команду /count")


bot.polling(non_stop=True)
