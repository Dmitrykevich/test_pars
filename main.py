import json
from bs4 import BeautifulSoup
import requests

from utilities import scrap_ad_id, scrap_title, scrap_price, scrap_mileage, scrap_color, scrap_power, \
    scrap_description, scrap_ad_images

url = 'https://www.truckscout24.de/transporter/gebraucht/kuehl-iso-frischdienst/renault'
domain = 'https://www.truckscout24.de'
count = 1
json_data = {'ads': []}  # Здесь будут храниться итоговые данные для дампа в джейсон
while count <= 4:
    parsing_url = f'{url}?currentpage={count}'  # Поулчаем урл страницы

    response = requests.get(parsing_url)  # Делаем запрос на получение страницы для парсинга
    soup = BeautifulSoup(response.text, 'html.parser')
    first_ad_link = soup.find('div', class_='ls-elem ls-elem-gap').find('a', {'data-item-name': 'detail-page-link'})[
        'href']  # Находим ссылку на первое объявление на странице
    full_ad_link = f'{domain}{first_ad_link}'
    response = requests.get(full_ad_link)
    ad_page = BeautifulSoup(response.text, 'html.parser')
    scrap_ad_images(ad_page)  # Получаем картинку
    ad_data = {'id': scrap_ad_id(ad_page),  # Наполняем словарь данными
               'href': full_ad_link,
               'title': scrap_title(ad_page),
               'price': scrap_price(ad_page),
               'mileage': scrap_mileage(ad_page),
               'color': scrap_color(ad_page),
               'power': scrap_power(ad_page),
               'description': scrap_description(ad_page)
               }
    json_data['ads'].append(ad_data)  # Собираем все значения ключа в список
    with open('data/data.json', 'w') as f:  # Записываем, дампим
        json.dump(json_data, f, ensure_ascii=False)

    print(f'ad - {count} - is done')
    count += 1
