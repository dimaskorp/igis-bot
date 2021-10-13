import requests
from bs4 import BeautifulSoup as BS
import asyncio
import json

HEADERS = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36"
}

sp = []
spisok_fio = []
dep_slovar = dict()
budget_slovar = dict()


def f_departments():  # парсинг учреждений ижевска
    url = "https://igis.ru/online"
    response = requests.get(url, headers=HEADERS)
    soup = BS(response.text, 'lxml')
    div = soup.find_all('div', class_='row-div row-div-sm-4 row-div-md-2 row-div-bg-1')
    for quote in div:
        for link in quote.select('a', href=True):
            quote_href = url + link['href']
            text = quote.get_text(separator=' ').strip()
            dep_slovar[text] = quote_href
    # with open('1_INSTITUTIONS_OF_IZHEVSK.json', 'w') as file:
    #     json.dump(dep_slovar, file, indent=4, ensure_ascii=False)
    return dep_slovar


def budget_institutions(number):  # парсинг бюджетных
    url = list(dep_slovar.values())[number]
    response = requests.get(url, headers=HEADERS)
    soup = BS(response.text, 'lxml')
    div = soup.find('div', attrs={'class': 'headline'}).find_next('h2', text='Бюджетные учреждения')
    all_budget_institutions = div.find_all_next('h3')
    for quote in all_budget_institutions:
        itemName = quote.find_next('a').text.strip()
        quote_href = 'https://igis.ru/online' + quote.find_next('a', href=True).get('href')
        budget_slovar[itemName] = quote_href
    # with open('2_BUDGET_INSTITUTIONS.json', 'w') as file:
    #     json.dump(budget_slovar, file, indent=4, ensure_ascii=False)
    return budget_slovar


def f_specialists(number):  # парсинг номерков
    url = list(budget_slovar.values())[number] + '&page=zapdoc'
    response = requests.get(url, headers=HEADERS)
    soup = BS(response.text, 'lxml')
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
    # with open('3_MAKE_AN_APPOINTMENT.json', 'w') as file:
    #     json.dump(special_slovar, file, indent=4, ensure_ascii=False)
    return key, spisok_fio


if __name__ == '__main__':
    f_departments()
    budget_institutions(number=2)
    f_specialists(number=8)
