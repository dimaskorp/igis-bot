# -*- coding: windows-1251 -*-
import telebot
import requests
from bs4 import BeautifulSoup as Bs
from telebot import types


bot = telebot.TeleBot('1552413047:AAGpkNonW31wDJOY7-DnMRCl4iI9eElxUkw')
key_spisok = []

url = 'http://igis.ru/online?obj=24&page=zapdoc'

def slovar():
    html = requests.get(url).text
    soup = Bs(html, 'html.parser')
    table = soup.findChildren('table', attrs={'class': 'table-border'})
    my_table = table[0]
    tr = my_table.findChildren(['tr'])
    sp = []
    fio = []
    i = 0
    j = 0

    for link in my_table.select('a', href=True):
        print('https://igis.ru/online' + link['href'])


    for quote in tr:
        a = len(sp)
        if quote.attrs == {'class': ['table-border-light']}:

            if i < a:
                i += 1
                sp.append(quote.text.strip())
                fio.append([])
                j += 1
            else:
                sp.append(quote.text.strip())
                fio.append([])
        else:
            sp.append(sp[i])
            word = 'Всего номерков'
            if word in quote.text.strip():
                fio[j].append(quote.text.strip())
            i += 1

    key = list(dict.fromkeys(sp))

    for i, elem in enumerate(fio):
        if not fio[i]:
            fio[i].append('Номерков нет')
    # dictionary = dict(zip(fio, sp))
    # print(dictionary)
    # sorp = sorted(dictionary.items(), key=lambda x: x[1])
    # diction = json.dumps(dict(sorp), ensure_ascii=False, indent=4)

    return key, fio

# кнопки вызывающие действия
@bot.message_handler(commands="start")
def messay(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!')
        keyboard = types.InlineKeyboardMarkup()

        for i, elem in enumerate(slovar()[0]):
            name_key = f'key{i}'
            key_spisok.append(name_key)
            keyboard.add(types.InlineKeyboardButton(text=elem, callback_data=name_key))
        bot.send_message(message.from_user.id, 'Выбери специализацию:', reply_markup=keyboard)
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Напиши /igis')
    else:
        bot.send_message(message.from_user.id, 'Напиши /help')


# обработчик (кнопки вызывающие действия)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "keyboard":
        keyboard = types.InlineKeyboardMarkup()
        for i, elem in enumerate(slovar()[0]):
            name_key = f'key{i}'
            keyboard.add(types.InlineKeyboardButton(text=elem, callback_data=name_key))
        bot.edit_message_text('Выбери специализацию:', call.message.chat.id, call.message.message_id,
                              reply_markup=keyboard)

    for i, elem in enumerate(slovar()[0]):
        if call.data == key_spisok[i]:
            next_menu = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton(text='Назад', callback_data='keyboard')
            next_menu.add(back)
            bot.edit_message_text(
                f'Вы выбрали специализацию: {slovar()[0][i]}!\n\n' + '\n\n'.join([str(lst) for lst in slovar()[1][i]]),
                call.message.chat.id, call.message.message_id, reply_markup=next_menu)


bot.polling()


