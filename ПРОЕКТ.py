# импортируем библиотеку бота
import telebot
from telebot import types
import requests

# указываем к камому боту обращаемся, в класс TeleBot прописываем бот, с которым будем взаимодействовать
bot = telebot.TeleBot('5540571238:AAEXAT_0XVt_l_wb7864JgZdSvtGq5M0tyo')  # @test324234324_bot

# для отслеживания команд прописываем декоратор с обращением к специальному методу message_handler
@bot.message_handler(commands=['start'])
# создаем функцию для указанной команды  с указанем параметра message (может быть команда, либо текствовая запись)
def website(message):
    # создаем стандартные кнопки (resize_keyboard=True - для корректного вывода кнопок на ПК и телефоне)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button1 = types.KeyboardButton('Калькулятор')
    button2 = types.KeyboardButton('Прогноз подгоды')
    # формируем структуру
    markup.add(button1, button2)
    # приветствуем пользователя с обращение по имени
    bot.send_message(message.chat.id, f'''Привет, {message.from_user.first_name}!
Я БОТ-ОРГАНАЙЗЕР
пользуйся наздоровье :)
выбери что тебе нужно''', reply_markup=markup) #reply_markup=keyboard для присвоения кнопок

# выбираем кнопки (прогноз погоды будет тут же, еще в разработке)
@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.text == 'Калькулятор':
        calc()
        bot.send_message(message.chat.id, 'Тискай на кнопки', reply_markup=calc())

# создаем функцию калькулятора
def calc():
    global value # для доступа к переменной
    value = '' # хранит текущее значение калькулятора
    global old_value
    old_value = '' # чтобы не изменять сообщение на то же самое
    # создаем клавиатуру
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
# добавляем обработчик событий
    @bot.callback_query_handler(func=lambda call: True)
    def callback_func(query):
        global value, old_value
        data = query.data # data это то, что возвращает кнопка

        if data == '**':
            pass
        elif data == 'C':
            value = ''
        elif data == '<=':
            if value != '':
                value = value[:len(value) - 1]
        elif data == '=':
            try:
                value = str(eval(value)) # считаем значения при помощи функции eval
            except:
                value = 'Деление на 0!'
        else:
            value += data # иначе любой символ

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




# запускаем код в работу
bot.polling(none_stop=True)
