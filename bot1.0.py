from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from parsing import dep_slovar, budget_slovar, sp, spisok_fio
import keyboards as kb
import re

TOKEN = '1552413047:AAGpkNonW31wDJOY7-DnMRCl4iI9eElxUkw'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
data_1 = []
data_2 = []
data_3 = []


# кнопки вызывающие действия
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    kb.spisok_key_1.clear()
    kb.spisok_key_2.clear()
    kb.spisok_key_3.clear()
    await bot.send_message(msg.from_user.id, 'Привет {0.first_name}!\nВыберите раздел:'.format(msg.from_user), reply_markup=kb.keyboard_1())


@dp.callback_query_handler(lambda call: call.data == 'keyboard')
async def callback_inline_1(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer("Выберите раздел:", reply_markup=kb.keyboard_1())


@dp.callback_query_handler(lambda call: call.data in kb.spisok_key_1)
async def callback_inline_2(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    data_1.append(call.data)
    for i, elem in enumerate(dep_slovar):
        if call.data == kb.spisok_key_1[i]:
            number = int("".join(re.findall("\d+", call.data)))
            keys = list(dep_slovar.keys())[i]
            await call.message.answer(f'{keys}\n\nВыберите учреждение:', reply_markup=kb.keyboard_2(number))
    kb.spisok_key_1.clear()


@dp.callback_query_handler(lambda call: call.data in kb.spisok_key_2)
async def callback_inline_3(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    data_2.append(call.data)
    for i, elem in enumerate(budget_slovar):
        if call.data == kb.spisok_key_2[i]:
            number = int("".join(re.findall("\d+", call.data)))
            keys = list(budget_slovar.keys())[i]
            await call.message.answer(f'{keys}\n\nВыберите специализацию:', reply_markup=kb.keyboard_3(number))
    kb.spisok_key_2.clear()


@dp.callback_query_handler(lambda call: call.data in kb.spisok_key_3)
async def callback_inline_4(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    data_3.append(call.data)
    for i, elem in enumerate(kb.spisok_key_3):
        if call.data == kb.spisok_key_3[i]:
            next_menu = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton(text='Назад', callback_data='keyboard')
            next_menu.add(back)
            key_ = list(dict.fromkeys(sp))
            await call.message.answer(f'{key_[i]}!\n\n' + '\n\n'.join(spisok_fio[i]), reply_markup=next_menu)
    kb.spisok_key_3.clear()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
