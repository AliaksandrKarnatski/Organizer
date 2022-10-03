# импортируем библиотеку бота

import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import telebot
from telebot import types
import requests

# указываем к камому боту обращаемся, в класс TeleBot прописываем бот, с которым будем взаимодействовать
bot = telebot.TeleBot('') # t.me/pjojekt12345678Bot


# для отслеживания команд прописываем декоратор с обращением к специальному методу message_handler
@bot.message_handler(commands=['start'])
# создаем функцию для указанной команды  с указанем параметра message (может быть команда, либо текствовая запись)
def start(message):
    # выводим пользователю сообщение (так же можно выбрать иное) с указание в какой чат отправляем.
    # так же указываем режим к котором отправляется текст (нашем случае будет html для удобства форматирования)
    # отражаем имя пользователя
    mess = f'''<b>Привет, {message.from_user.first_name}!</b>
Я умный БОТ, который владеет приятными мелочами.
Пожалуйста, выбери из списка ниже'''

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Калькулятор')
    item2 = types.KeyboardButton('Курсы валют')
    item3 = types.KeyboardButton('Прогноз погоды')
    item4 = types.KeyboardButton('Другое')

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)



@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.text == 'Калькулятор':
        value = ''
        old_value = ''

        keyboard = telebot.types.InlineKeyboardMarkup()
        # 1
        keyboard.row(telebot.types.InlineKeyboardButton('%', callback_data='%'),
                     telebot.types.InlineKeyboardButton('C', callback_data='C'),
                     telebot.types.InlineKeyboardButton('<=', callback_data='<='),
                     telebot.types.InlineKeyboardButton('/', callback_data='/'))
        # 2
        keyboard.row(telebot.types.InlineKeyboardButton('7', callback_data='7'),
                     telebot.types.InlineKeyboardButton('8', callback_data='8'),
                     telebot.types.InlineKeyboardButton('9', callback_data='9'),
                     telebot.types.InlineKeyboardButton('*', callback_data='*'))
        # 3
        keyboard.row(telebot.types.InlineKeyboardButton('4', callback_data='4'),
                     telebot.types.InlineKeyboardButton('5', callback_data='5'),
                     telebot.types.InlineKeyboardButton('6', callback_data='6'),
                     telebot.types.InlineKeyboardButton('-', callback_data='-'))
        # 4
        keyboard.row(telebot.types.InlineKeyboardButton('1', callback_data='1'),
                     telebot.types.InlineKeyboardButton('2', callback_data='2'),
                     telebot.types.InlineKeyboardButton('3', callback_data='3'),
                     telebot.types.InlineKeyboardButton('+', callback_data='+'))
        # 5
        keyboard.row(telebot.types.InlineKeyboardButton('x**', callback_data='**'),
                     telebot.types.InlineKeyboardButton('0', callback_data='0'),
                     telebot.types.InlineKeyboardButton(',', callback_data=','),
                     telebot.types.InlineKeyboardButton('=', callback_data='='))

        # @bot.message_handler(commands=['start', 'calculator'])
        def getMessage(message):
            global value
            if value == '':
                bot.send_message(message.from_user.id, '0', reply_markup=keyboard)  # !!!!!!!!! message.from_user.id
            else:
                bot.send_message(message.from_user.id, value, reply_markup=keyboard)

        # @bot.callback_query_handler(func=lambda call: True)
        def callback_func(query):
            global value, old_value
            data = query.data

            if data == 'no':
                pass
            elif data == 'C':
                value = ''
            elif data == '<=':
                if value != '':
                    value = value[:len(value) - 1]
            elif data == '=':
                try:
                    value = str(eval(value))
                except:
                    value = 'Деление на 0!'
            else:
                value += data

            if (value != old_value and value != '') or (0 != old_value and value == ''):
                if value == '':
                    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='0',
                                          reply_markup=keyboard)
                    old_value = '0'
                else:
                    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                          text=value, reply_markup=keyboard)
                    old_value = value

            old_value = value
            if value == 'Деление на 0!': value = ''

    elif message.text == 'Курсы валют':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item21 = types.KeyboardButton('USD')
        item22 = types.KeyboardButton('EU')
        item23 = types.KeyboardButton('RUB')
        item24 = types.KeyboardButton('BYN')
        back = types.KeyboardButton('Вернуться назад')
        markup.add(item21, item22, item23, item24, back)

        bot.send_message(message, 'Курсы валют', reply_markup=markup)

    elif message.text == 'Погода':
        # API погоды
        dp = Dispatcher(bot)

        @dp.message_handler(commands=["pogoda"])
        async def start_command(message: types.Message):
            await message.reply("Напиши мне название города, чтобы узнать какая там сейчас погода")

        # присваиваем изображение к данному типу погоды
        @dp.message_handler()
        async def get_weather(message: types.Message):
            code_to_smile = {
                "Clear": "Ясно \U00002600",
                "Clouds": "Облачно \U00002601",
                "Rain": "Дождь \U00002614",
                "Drizzle": "Дождь \U00002614",
                "Thunderstorm": "Гроза \U000026A1",
                "Snow": "Снег \U0001F328",
                "Mist": "Туман \U0001F32B"
            }

            try:
                r = requests.get(
                    f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
                )
                data = r.json()

                city = data["name"]
                cur_weather = data["main"]["temp"]

                weather_description = data["weather"][0]["main"]
                if weather_description in code_to_smile:
                    wd = code_to_smile[weather_description]
                else:
                    wd = "Посмотри в окно, не пойму что там за погода!"

                humidity = data["main"]["humidity"]
                pressure = data["main"]["pressure"]
                wind = data["wind"]["speed"]
                sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
                sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
                length_of_the_day = datetime.datetime.fromtimestamp(
                    data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                    data["sys"]["sunrise"])

                await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                    f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                                    f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                    f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                                    f"***Хорошего дня!***"
                                    )
            except:
                await message.reply("\U00002620 Проверьте название города \U00002620")

        if __name__ == '__main__':
            executor.start_polling(dp)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # item31 = types.KeyboardButton('Пожалуйста, укажите город')
        back = types.KeyboardButton('Вернуться назад')
        markup.add(back)

        bot.send_message(message.chat.id, 'Погода', reply_markup=markup)

    elif message.text == 'Другое':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item41 = types.KeyboardButton('Настройки')
        item42 = types.KeyboardButton('Стикер')
        back = types.KeyboardButton('Вернуться назад')

        markup.add(item41, item42, back)

        bot.send_message(message.chat.id, 'Другое', reply_markup=markup)

    elif message.text == 'Вернуться назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Калькулятор')
        item2 = types.KeyboardButton('Курсы валют')
        item3 = types.KeyboardButton('Погода')
        item4 = types.KeyboardButton('Другое')

        markup.add(item1, item2, item3, item4)

        bot.send_message(message.chat.id, 'Пожалуйста, сделайте свой выбор', reply_markup=markup)

    elif message.text == 'Стикер':
        stick = photo = open('1.PNG', 'rb')
        bot.send_photo(message.chat.id, stick)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Калькулятор')
        item2 = types.KeyboardButton('Курсы валют')
        item3 = types.KeyboardButton('Погода')
        item4 = types.KeyboardButton('Другое')

        markup.add(item1, item2, item3, item4)

        bot.send_message(message.chat.id, 'Пожалуйста, сделайте свой выбор', reply_markup=markup)



# # отслеживание текста введенного пользователем (на текст пользователя будет ответ)
# @bot.message_handler(content_types=['text'])
# def get_user_text(message):
#     if message.text == "hello":
#         bot.send_message(message.chat.id, 'И тебе привет!', parse_mode='html')
#     elif message.text == "id":
#         bot.send_message(message.chat.id, f'Твой ID: {message.from_user.id}', parse_mode='html')
#     elif message.text == 'photo':
#         photo = open('1.PNG', 'rb')
#         bot.send_photo(message.chat.id, photo)
#     else:
#         bot.send_message(message.chat.id, 'Я тебя не понимаю', parse_mode='html')
#
#
#
# # отслеживание файлов отправленных пользователем
# @bot.message_handler(content_types=['photo'])
# def get_user_text(message):
#     bot.send_message(message.chat.id, 'Вау, крутое фото!')
#
#
# # создаем кнопки (служит объект types, который нужно импортировать из библиотеки)
# @bot.message_handler(commands=['website'])
# def website(message):
#     # создаем стандартные кнопки
#     markup = types.InlineKeyboardMarkup()
#     # формируем структуру
#     markup.add(types.InlineKeyboardButton('Посетить веб сайт', url='https://ru.wikipedia.org/wiki/%D0%9C%D0%B5%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D1%86%D0%B8%D0%BA%D0%BB'))
#     # для отправки сообщения прикрепляем кнопку
#     bot.send_message(message.chat.id, 'Перейдите на сайт', reply_markup=markup)
#


# # создаем ЕЩЁ кнопки (служит объект types, который нужно импортировать из библиотеки)
# @bot.message_handler(commands=['help'])
# def website(message):
#     # создаем стандартные кнопки (resize_keyboard=True - для корректного вывода кнопок на ПК и телефоне)
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     website = types.KeyboardButton('Веб сайт')
#     start = types.KeyboardButton('Start')
#     # формируем структуру
#     markup.add(website,start)
#     # для отправки сообщения прикрепляем кнопку
#     bot.send_message(message.chat.id, 'Перейдите на сайт', reply_markup=markup)
#
#
# # запускаем бот на постоянное выполнение (метод polling)
bot.polling(none_stop=True)

