# -*- coding: cp1251 -*-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from parsing import f_departments, budget_institutions, f_specialists

spisok_key_1 = []  # Список кнопок первого меню
spisok_key_2 = []
spisok_key_3 = []


def keyboard_1():
    KEYBORD_1 = InlineKeyboardMarkup()
    for i, elem in enumerate(f_departments()):
        NAME_KEY_1 = f'key{i}'
        spisok_key_1.append(NAME_KEY_1)
        KEYBORD_1.row(InlineKeyboardButton(text=elem, callback_data=NAME_KEY_1))
    return KEYBORD_1


def keyboard_2(number):
    KEYBORD_2 = InlineKeyboardMarkup()
    for j, elem in enumerate(budget_institutions(number)):
        NAME_KEY_2 = f'key{j}'
        spisok_key_2.append(NAME_KEY_2)
        KEYBORD_2.add(InlineKeyboardButton(text=elem, callback_data=NAME_KEY_2))
    BACK = InlineKeyboardButton(text='Назад', callback_data='keyboard')
    KEYBORD_2.add(BACK)
    return KEYBORD_2


def keyboard_3(number):
    KEYBORD_3 = InlineKeyboardMarkup()
    for j, elem in enumerate(f_specialists(number)[0]):
        NAME_KEY_3 = f'key{j}'
        spisok_key_3.append(NAME_KEY_3)
        KEYBORD_3.add(InlineKeyboardButton(text=elem, callback_data=NAME_KEY_3))
    BACK = InlineKeyboardButton(text='Назад', callback_data='keyboard')
    KEYBORD_3.add(BACK)
    return KEYBORD_3
