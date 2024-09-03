import os
import time
from random import choice

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


BASE_URL = "https://www.cardmarket.com/en/FleshAndBlood/Products/Singles"


def format_url(**kwargs):
    print(kwargs)
    if kwargs.get('alpha_print'):
        # URL in form of:
        # {set-name}{set-edition-full-name}/{card-name}{pitch_name}{OPTIONAL set_id if not alpha}{card-print-id}{OPTIONAL foiling-id}
        first_part = '-'.join([kwargs.get("set_name"), kwargs.get("card_edition_name")])
        second_part_data = [kwargs.get("card_name"), kwargs.get("set_id")]
        if kwargs.get('card_pitch'):
            second_part_data.insert(1, kwargs.get('card_pitch'))
        if kwargs.get('printing_edition') == 'U':
            second_part_data.insert(2, kwargs.get('printing_edition'))
        if kwargs.get("foiling") == 'R':
            second_part_data.append('RF')
        second_part = '-'.join(second_part_data)
        print(os.path.join(BASE_URL, first_part, second_part))
        return os.path.join(BASE_URL, first_part, second_part)
    elif kwargs.get('old_print'):
        # URL in form of:
        # {set-name}{set-edition-full-name}/{card-name}{set-edition-id}{card-print-id}{OPTIONAL foiling-id}

        first_part = '-'.join([kwargs.get("set_name"), kwargs.get("card_edition_name")])
        second_part_data = [kwargs.get("card_name"), kwargs.get("set_id")]
        if kwargs.get('printing_edition') == 'U':
            second_part_data.insert(1, kwargs.get('printing_edition'))
        if kwargs.get("foiling") == 'R':
            second_part_data.append('RF')
        second_part = '-'.join(second_part_data)
        print(os.path.join(BASE_URL, first_part, second_part))
        return os.path.join(BASE_URL, first_part, second_part)
    else:
        # URL in form of:
        # {set-name}/{card-name}{foiling-name}
        print(os.path.join(BASE_URL, kwargs.get("set_name"),
                            '-'.join([kwargs.get("card_name"), kwargs.get("foiling")])))
        return os.path.join(BASE_URL, kwargs.get("set_name"),
                            '-'.join([kwargs.get("card_name"), kwargs.get("foiling")]))


def scrap_cm(**kwargs):
    time.sleep(1)
    url = format_url(**kwargs)
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
        "Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/113.0",
        "Mozilla/5.0 (Android 12; Mobile; rv:109.0) Gecko/113.0 Firefox/113.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0",
    ]
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", choice(user_agents))
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.profile = profile
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    table_content = driver.find_element(By.CLASS_NAME, 'table-body').get_attribute('innerHTML')
    souped_html = BeautifulSoup(table_content, 'html.parser')
    driver.close()
    result_dict = {}
    for index, row_div in enumerate(souped_html.findAll('div', attrs={'class': 'row g-0 article-row'})):
        if index == 5:
            break
        price_div = row_div.find('span', attrs={
            'class': "color-primary small text-end text-nowrap fw-bold"})
        seller_div = row_div.find('span', attrs={'class': "seller-name"})
        attributes_elem = row_div.find('div', attrs={'class': "product-attributes col"})
        quantity_elem = row_div.find('span', attrs={'class': "item-count small text-end"})
        card_info_dict = {}
        if quantity_elem:
            quantity = quantity_elem.text
            card_info_dict['quantity'] = int(quantity)
        if attributes_elem:
            card_condition = attributes_elem.find('span', attrs={'class': "badge"}).text
            card_info_dict['card_condition'] = card_condition
            try:
                card_language = attributes_elem.find('span', attrs={'class': 'icon me-2'})['aria-label']
            except KeyError:
                card_language = attributes_elem.find('span', attrs={'class': 'icon me-2'})['data-original-title']
            card_info_dict['card_language'] = card_language
        if seller_div:
            seller_country = seller_div.find('span', attrs={'class': 'icon d-flex has-content-centered me-1'})
            try:
                card_info_dict['seller_country'] = seller_country['aria-label']
            except KeyError:
                card_info_dict['seller_country'] = seller_country['title']
            seller_name = seller_div.find('a')
            card_info_dict['seller_name'] = seller_name.text
            card_info_dict['seller_profile_link'] = seller_name['href']
        if price_div:
            price_text = price_div.text
            price_text = price_text.split('€')[0].strip().replace(',', '.')
            card_info_dict['card_price'] = float(price_text)
        result_dict[index] = card_info_dict
    return result_dict
