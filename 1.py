import telebot
from telebot import types
import requests

bot = telebot.TeleBot('5540571238:AAEXAT_0XVt_l_wb7864JgZdSvtGq5M0tyo')  # @test324234324_bot


@bot.message_handler(commands=['start'])
def website(message):
    # создаем стандартные кнопки (resize_keyboard=True - для корректного вывода кнопок на ПК и телефоне)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button1 = types.KeyboardButton('Калькулятор')
    button2 = types.KeyboardButton('Прогноз подгоды')
    # формируем структуру
    markup.add(button1, button2)
    # для отправки сообщения прикрепляем кнопку
    bot.send_message(message.chat.id, 'Сделайте выбор', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.text == 'Калькулятор':
        calc()
        bot.send_message(message.chat.id, 'Работает функция калькулятор', reply_markup=calc())


def calc():
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
    return keyboard
bot.polling(none_stop=True)