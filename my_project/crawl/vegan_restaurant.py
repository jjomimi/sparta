from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient
import urllib.parse
from selenium import webdriver
import time

client = MongoClient('localhost', 27017)
db = client.vegan

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

driver = webdriver.Chrome('C:/Users/love8/OneDrive/바탕 화면/sparta/chromedriver_win32/chromedriver.exe', options=options)
url = 'https://map.kakao.com/?map_type=TYPE_MAP&q=%EB%B9%84%EA%B1%B4+%EB%A0%88%EC%8A%A4%ED%86%A0%EB%9E%91&urlLevel=10&urlX=621710&urlY=1098130'
driver.get(url)

driver.find_element_by_id('search-input').send_keys('비건 식당')
driver.find_element_by_css_selector('#search\.keyword\.submit').click()

page_bar = driver.find_element_by_css_selector("#info\.search\.page\.no2")
page_bar[0].click()

soup = BeautifulSoup(driver.page_source, 'html.parser')

items = list(soup.select('#info\.search\.place\.list > li'))

for item in items:
    validate_tag = item.select_one('div.head_item.clickArea > strong > a.link_name')
    if validate_tag is not None:
        name = item.select_one('div.head_item.clickArea > strong > a.link_name').text
        star = item.select_one('div.rating.clickArea > span.score > em').text
        address = item.select_one('div.info_item > div.addr').text
        openhour = item.select_one('div.info_item > div.openhour').text
        phone = item.select_one('div.contact.clickArea > span.phone').text.strip()
        print(name, star, address, openhour, phone)

        doc = {
            'name': name,
            'star': star,
            'address': address,
            'openhour': openhour,
            'phone': phone

        }
        db.vegan.insert_one(doc)

