import telebot
from telebot import types
import requests
import main_weather_tg_bot
# import datetime
# from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
# from aiogram.utils import executor

bot = telebot.TeleBot('5540571238:AAEXAT_0XVt_l_wb7864JgZdSvtGq5M0tyo')  # @test324234324_bot
# bot = Bot(token=tg_bot_token)
# dp = telebot.TeleBot('5540571238:AAEXAT_0XVt_l_wb7864JgZdSvtGq5M0tyo')

@bot.message_handler(commands=['start'])
def website(message):
    # создаем стандартные кнопки (resize_keyboard=True - для корректного вывода кнопок на ПК и телефоне)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button1 = types.KeyboardButton('Калькулятор')
    button2 = types.KeyboardButton('Прогноз погоды')

    # формируем структуру
    markup.add(button1, button2)
    # для отправки сообщения прикрепляем кнопку
    bot.send_message(message.chat.id, 'Сделайте выбор', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.text == 'Калькулятор':
        calc()
        bot.send_message(message.chat.id, 'Работает функция калькулятор', reply_markup=calc())
    elif message.text == 'Прогноз погоды':
        pogoda()
        bot.send_message(message.chat.id, 'Работает функция прогноз погоды',reply_markup=pogoda())
    elif message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Калькулятор')
        button2 = types.KeyboardButton('Прогноз погоды')
        button3 = types.KeyboardButton('Назад')
        markup.add(button1,button2,button3)
        bot.send_message(message.chat.id, 'Пожалуйста, сделайте свой выбор', reply_markup=markup)


def calc():
    global value
    value = ''
    global old_value
    old_value = ''

    keyboard = telebot.types.InlineKeyboardMarkup()

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
    keyboard.row(telebot.types.InlineKeyboardButton('x**', callback_data='*'),
                 telebot.types.InlineKeyboardButton('0', callback_data='0'),
                 telebot.types.InlineKeyboardButton(',', callback_data=','),
                 telebot.types.InlineKeyboardButton('=', callback_data='='))

    @bot.message_handler(content_types=['text'])
    def bot_message(message):
        global value
        if value == '':
            bot.send_message(message.chat.id, '0', reply_markup=keyboard)  # !!!!!!!!! message.from_user.id
        else:
            bot.send_message(message.chat.id, value, reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_func(query):
        global value, old_value
        data = query.data

        if data == '**':
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
                bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value,
                                      reply_markup=keyboard)
                old_value = value

        old_value = value
        if value == 'Деление на 0!': value = ''

    return keyboard

def pogoda():

    return main_weather_tg_bot

bot.polling(none_stop=True)
