from telebot import types
import telebot
from parsing import f_departments, budget_institutions, f_specialists, dep_slovar, budget_slovar, sp, spisok_fio
import re

bot = telebot.TeleBot('1552413047:AAGpkNonW31wDJOY7-DnMRCl4iI9eElxUkw')
key_spisok_1 = []
key_spisok_2 = []
key_spisok_3 = []

data1 = []
data2 = []
data3 = []


# кнопки вызывающие действия
@bot.message_handler(commands=["start"])
def messay(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!')
        bot.send_message(message.from_user.id, 'Выберите раздел:', reply_markup=main_menu_keyboard())
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Напиши /igis')
    else:
        bot.send_message(message.from_user.id, 'Напиши /help')


@bot.callback_query_handler(func=lambda call: call.data == 'keyboard')
def callback_inline_1(call):
    bot.edit_message_text('Выберите раздел:', call.message.chat.id, call.message.message_id,
                          reply_markup=main_menu_keyboard())


# # обработчик (кнопки вызывающие действия)
# @bot.callback_query_handler(func=lambda call: call.data == 'keyboard')
# def name_key_2(call):
#     number = int("".join(re.findall("\d+", data1[0])))
#     first_menu_keyboard(number)
#     callback_inline_2(call)


# # обработчик (кнопки вызывающие действия)
# @bot.callback_query_handler(func=lambda call: call.data == 'keyboard')
# def name_key_2(call):
#     number = int("".join(re.findall("\d+", data2[0])))
#     second_menu_keyboard(number)
#     callback_inline_3(call)


@bot.callback_query_handler(func=lambda call: call.data in key_spisok_1)
def callback_inline_2(call):
    data1.append(call.data)
    for i, elem in enumerate(dep_slovar):
        if call.data == key_spisok_1[i]:
            number = int("".join(re.findall("\d+", call.data)))
            keys = list(dep_slovar.keys())[i]
            bot.edit_message_text(f'{keys}\n\nВыберите учреждение:', call.message.chat.id, call.message.message_id,
                                  reply_markup=first_menu_keyboard(number))
    key_spisok_1.clear()


@bot.callback_query_handler(func=lambda call: call.data in key_spisok_2)
def callback_inline_3(call):
    for i, elem in enumerate(budget_slovar):
        if call.data == key_spisok_2[i]:
            number = int("".join(re.findall("\d+", call.data)))
            keys = list(budget_slovar.keys())[i]
            bot.edit_message_text(f'{keys}\n\nВыберите специализацию:', call.message.chat.id, call.message.message_id,
                                  reply_markup=second_menu_keyboard(number))
    data2.append(call.data)
    key_spisok_2.clear()


@bot.callback_query_handler(func=lambda call: call.data in key_spisok_3)
def callback_inline_4(call):
    data3.append(call.data)
    for i, elem in enumerate(key_spisok_3):
        if call.data == key_spisok_3[i]:
            next_menu = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton(text='🚗 Назад', callback_data='keyboard')
            next_menu.add(back)
            key_ = list(dict.fromkeys(sp))
            bot.edit_message_text(f'{key_[i]}!\n\n' + '\n\n'.join(spisok_fio[i]), call.message.chat.id,
                                  call.message.message_id, reply_markup=next_menu)
    key_spisok_3.clear()


############################ Keyboards #########################################


def main_menu_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    for i, elem in enumerate(f_departments()):
        name_key = f'key{i}'
        key_spisok_1.append(name_key)
        keyboard.add(types.InlineKeyboardButton(text=elem, callback_data=name_key))
    return keyboard


def first_menu_keyboard(number):
    keyboard_menu = types.InlineKeyboardMarkup()
    for j, elem in enumerate(budget_institutions(number)):
        name_key_2 = f'key{j}'
        key_spisok_2.append(name_key_2)
        keyboard_menu.add(types.InlineKeyboardButton(text=elem, callback_data=name_key_2))
    back = types.InlineKeyboardButton(text='🚗 Назад', callback_data='keyboard')
    keyboard_menu.add(back)
    return keyboard_menu


def second_menu_keyboard(number):
    keyboard_menu2 = types.InlineKeyboardMarkup()
    for j, elem in enumerate(f_specialists(number)[0]):
        name_key_3 = f'key{j}'
        key_spisok_3.append(name_key_3)
        keyboard_menu2.add(types.InlineKeyboardButton(text=elem, callback_data=name_key_3))
    back = types.InlineKeyboardButton(text='🚗 Назад', callback_data='keyboard')
    keyboard_menu2.add(back)
    return keyboard_menu2


bot.polling(none_stop=True)
