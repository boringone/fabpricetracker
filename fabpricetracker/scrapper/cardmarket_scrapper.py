import os
import time
from selenium.webdriver import ActionChains
from selenium_stealth import stealth
from random import choice

from bs4 import BeautifulSoup
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


BASE_URL = "https://www.cardmarket.com/en/FleshAndBlood/Products/Singles"


def format_url(**kwargs):
    print(kwargs)
    # TODO pitch should be included for scrapping lower rarity cards
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

def gen_driver():
    try:
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        ]
        options = webdriver.ChromeOptions()
        user_agent = choice(user_agents)
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("start-maximized")
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        return driver
    except Exception as e:
        print("Error in Driver: ", e)


def _init_driver(driver):
    try:
        driver.execute_cdp_cmd('Page.enable', {})
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': """
                Element.prototype._as = Element.prototype.attachShadow;
                Element.prototype.attachShadow = function (params) {
                    return this._as({mode: "open"})
                };
            """
        })
    except Exception as e:
        print('error init driver')


def get_shadowed_iframe(driver, css_selector: str):
    try:
        shadow_element = driver.execute_script("""
        return document.querySelector(arguments[0]).shadowRoot.firstChild;
        """, css_selector)
        return shadow_element
    except:
        print('no shadow iframe')
        pass


def scrap_cm(**kwargs):
    url = format_url(**kwargs)
    driver = gen_driver()
    _init_driver(driver)
    driver.get(url)
    try:
        table_content = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-body')))
    except TimeoutException:
        input_checkbox = get_shadowed_iframe(driver, "div:not(:has(div))")
        if not input_checkbox:
            return {}
        driver.switch_to.frame(input_checkbox)
        iframe_body = driver.find_element(By.CSS_SELECTOR, "body")
        if iframe_body:
            iframe_body.click()
            actions = ActionChains(driver)
            actions.move_to_element_with_offset(iframe_body, 10, 10)
            actions.click(iframe_body)
            actions.perform()
            driver.switch_to.default_content()
            table_content = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-body')))
        else:
            print('cloudfare error')
            return {}
    result_dict = {}
    table_inner_html = table_content.get_attribute('innerHTML')
    if not table_inner_html:
        return result_dict
    souped_html = BeautifulSoup(table_inner_html, 'html.parser')
    driver.quit()
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
