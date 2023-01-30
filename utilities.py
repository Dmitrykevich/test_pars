import os
import requests
import re
import shutil


def scrap_title(ad_page):
    """

    :param ad_page: Объект bs4
    :return: Возвращает название объявления
    """
    ad_title = ad_page.find('h1', class_='sc-ellipsis sc-font-xl').text
    return ad_title


def scrap_price(ad_page):
    """

    :param ad_page: Объект bs4
    :return: Если цена указана, то возвращает число, если нет - возвращает ноль
    """
    ad_price = ad_page.find('h2', class_='sc-highlighter-4 sc-highlighter-xl sc-font-bold').text
    if ad_price:
        price = re.findall(r'\d+\.\d+', ad_price)
        return int(price[0].replace('.', ''))
    else:
        return 0


def scrap_mileage(ad_page):
    """

    :param ad_page: Объект bs4
    :return: Если пробег указан, то возвращает число в Км, если нет - возвращает ноль
    """
    ad_mileage = ad_page.find_all('div', class_='itemval')[1].text
    mileage = re.findall(r'\d+\.\d+', ad_mileage)
    if mileage:
        return int(mileage[0].replace('.', ''))
    else:
        return 0


def scrap_color(ad_page):
    """

    :param ad_page: Объект bs4
    :return: Если указан цвет, то возвращает цвет, если не указан - возвращает пустую строку
    """
    ad_color = ad_page.find('div', string='Farbe')
    if ad_color:
        color = ad_color.find_next('div').text
        return color
    else:
        return ''


def scrap_power(ad_page):
    """

    :param ad_page: Объект bs4
    :return: Если указана мощность двигателя, то возвращает число в Kw, если нет - возвращает ноль
    """
    ad_power = ad_page.find('div', string='Leistung')
    if ad_power:
        power = ad_power.find_next('div').text
        return int(power.split(' ')[0])
    else:
        return 0


def scrap_description(ad_page):
    """

    :param ad_page: Объект bs4
    :return: Возвращает описание авто, если описания нет, то возвращает пустую строку
    """
    ad_description = ad_page.find('div', {'data-type': 'description'})
    description = ad_description.find_next('p').text
    if ad_description:
        return description.replace('\xa0', '')
    else:
        return ''


def scrap_ad_id(ad_page):
    """

    :param ad_page: Объект bs4
    :return: За уникальный айди возьмем TruckScoutID с сайта https://www.truckscout24.de
    """
    truck_scout_id = ad_page.find('div', string='TruckScoutID')
    scout_id = truck_scout_id.find_next('div').text
    return int(scout_id)


def scrap_ad_images(ad_page):
    """

    :param ad_page: Объект bs4
    :return: Находит первое изображение объявления, даёт ему имя из 6 последних символов, создаёт папку с уникальным
    айди объявления, если такая уже есть, то просто сохраняет в неё картинку
    """
    image_url = ad_page.find('div', class_='gallery-picture').find('img')['data-src']
    ad_id = scrap_ad_id(ad_page)
    img_name = image_url[-10:-4]
    folder_path = f'data/{ad_id}'
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    res = requests.get(image_url, stream=True)
    with open(f'{folder_path}/{img_name}.jpg', 'wb') as f:
        shutil.copyfileobj(res.raw, f)
