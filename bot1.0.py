from telebot import types
from bs4 import BeautifulSoup as Bs
import telebot
import re
import requests
import json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.41 Mobile Safari/537.36'}

sp = []
spisok_fio = []
dep_slovar = dict()
budget_slovar = dict()


bot = telebot.TeleBot('1552413047:AAGpkNonW31wDJOY7-DnMRCl4iI9eElxUkw')
key_spisok_1 = []
key_spisok_2 = []
key_spisok_3 = []

data1 = []
data2 = []
data3 = []


def get_html(url):
    html = requests.get(url, headers=HEADERS)
    return html.text


def f_departments():  # парсинг учреждений ижевска
    url = 'http://igis.ru/online'
    soup = Bs(get_html(url), 'lxml')
    div = soup.find_all('div', class_='row-div row-div-sm-4 row-div-md-2 row-div-bg-1')
    # dep_slovar = dict()
    for quote in div:
        for link in quote.select('a', href=True):
            quote_href = url + link['href']
            text = quote.get_text(separator=' ').strip()
            dep_slovar[text] = quote_href
    with open('INSTITUTIONS_OF_IZHEVSK.json', 'w') as file:
        json.dump(dep_slovar, file, indent=4, ensure_ascii=False)
    return dep_slovar


def budget_institutions(number):  # парсинг бюджетных
       url = list(dep_slovar.values())[number]
    soup = Bs(get_html(url), 'html.parser')
    div = soup.find('div', attrs={'class': 'headline'}).find_next('h2', text='Бюджетные учреждения')
    all_budget_institutions = div.find_all_next('h3')
    # budget_slovar = dict()
    for quote in all_budget_institutions:
        itemName = quote.find_next('a').text.strip()
        quote_href = 'https://igis.ru/online' + quote.find_next('a', href=True).get('href')
        budget_slovar[itemName] = quote_href
    with open('BUDGET_INSTITUTIONS.json', 'w') as file:
        json.dump(budget_slovar, file, indent=4, ensure_ascii=False)
    return budget_slovar


def f_specialists(number):  # парсинг номерков
    url = list(budget_slovar.values())[number] + '&page=zapdoc'
    soup = Bs(get_html(url), 'html.parser')
    table = soup.find('table', attrs={'class': 'table-border'})
    tr = table.find_all('tr')
    # sp = []
    # spisok_fio = []
    i = 0
    j = 0
    for quote in tr:
        a = len(sp)
        if quote.attrs == {'class': ['table-border-light']}:
            if i < a:
                i += 1
                sp.append(quote.text.strip())
                spisok_fio.append([])
                j += 1
            else:
                sp.append(quote.text.strip())
                spisok_fio.append([])
        else:
            quote_text = quote.text.strip()
            for link in quote.select('a', href=True):
                quote_href = 'https://igis.ru/online' + link['href']
            sp.append(sp[i])
            word = 'Всего номерков'
            if word in quote.text.strip():
                spisok_fio[j].append(quote_text + ' ' + quote_href)
            i += 1

    key = list(dict.fromkeys(sp))
    for i, elem in enumerate(spisok_fio):
        if not spisok_fio[i]:
            spisok_fio[i].append('Номерков нет')
    special_slovar = dict(zip(key, spisok_fio))
    with open('MAKE_AN_APPOINTMENT.json', 'w') as file:
        json.dump(special_slovar, file, indent=4, ensure_ascii=False)
    return key, spisok_fio


# кнопки вызывающие действия
@bot.message_handler(commands=["start"])
def messay(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!\nВыберите раздел:', reply_markup=main_menu_keyboard())
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Напиши /igis')
    else:
        bot.send_message(message.from_user.id, 'Напиши /help')


@bot.callback_query_handler(func=lambda call: call.data == 'keyboard')
def callback_inline_1(call):
    bot.edit_message_text('Выберите раздел:', call.message.chat.id, call.message.message_id,
                          reply_markup=main_menu_keyboard())


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
            back = types.InlineKeyboardButton(text='Назад', callback_data='keyboard')
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
    back = types.InlineKeyboardButton(text='Назад', callback_data='keyboard')
    keyboard_menu.add(back)
    return keyboard_menu


def second_menu_keyboard(number):
    keyboard_menu2 = types.InlineKeyboardMarkup()
    for j, elem in enumerate(f_specialists(number)[0]):
        name_key_3 = f'key{j}'
        key_spisok_3.append(name_key_3)
        keyboard_menu2.add(types.InlineKeyboardButton(text=elem, callback_data=name_key_3))
    back = types.InlineKeyboardButton(text='Назад', callback_data='keyboard')
    keyboard_menu2.add(back)
    return keyboard_menu2


bot.polling(none_stop=True)
