from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
from bs4 import BeautifulSoup as BS
import lxml
import json

TOKEN = '1552413047:AAGpkNonW31wDJOY7-DnMRCl4iI9eElxUkw'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)



def get_html():
    sp = []
    fio = []
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36"
    }
    url = "https://igis.ru/online?obj=71&page=zapdoc"
    response = requests.get(url=url, headers=HEADERS)
    soup = BS(response.text, "lxml")
    table = soup.find('table', attrs={'class': 'table-border'})
    tr = table.find_all('tr')
    i = 0
    j = 0
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
            quote_text = quote.text.strip()
            for link in quote.select('a', href=True):
                quote_href = 'https://igis.ru/online' + link['href']

            sp.append(sp[i])
            word = 'Всего номерков'
            if word in quote.text.strip():
                fio[j].append(quote_text + ' ' + quote_href)
            i += 1
    key = list(dict.fromkeys(sp))
    for i, elem in enumerate(fio):
        if not fio[i]:
            fio[i].append('Номерков нет')

    # special_slovar = dict(zip(key, fio))
    # with open('MAKE_AN_APPOINTMENT.json', 'w') as file:
    #     json.dump(special_slovar, file, indent=4, ensure_ascii=False)
    return key, fio


# кнопки вызывающие действия
@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
    await msg.answer(f'Я бот. Приятно познакомиться, {msg.from_user.first_name}')
    rez = get_html()
    for i, elem in enumerate(rez[0]):
        await msg.answer(f'{elem}\n\n' + '\n\n'.join(rez[1][i]))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
