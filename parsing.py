import requests
from bs4 import BeautifulSoup

import json
import work_with_files as fw

def parse_fpt_last_news():
    URL = 'https://feopoliteh.ru/news'
    fpt_news = {}

    res = requests.get(URL)

    soup = BeautifulSoup(res.text, 'html.parser')
    news_item = soup.find('main').find('section').find('div').find('div').find('div').find('div').find('div')

    fpt_news['name'] = news_item.find('div').find('div', {'class': 'col-xs-7'}).find('div').find('div').find('a').text
    fpt_news['href'] = 'https://feopoliteh.ru' + news_item.find('div').find('div', {'class': 'col-xs-7'}).find('div').find('div').find('a').get('href', '')
    fpt_news['date'] = news_item.find('div').find('div', {'class': 'col-xs-7'}).find('div').find('div', {'class': 'news-date'}).text
    fpt_news['shortText'] = news_item.find('div').find('div', {'class': 'col-xs-7'}).find('div').find('div', {'class': 'news-text'}).text.strip()
    fpt_news['imgSrc'] = 'https://feopoliteh.ru' + news_item.find('div').find('div', {'class': 'col-xs-5'}).find('div').find('div').find('img').get('src', '')

    return fpt_news

def save_news(obj):
    fw.file_writer('json/saves.json', json.dumps(obj, ensure_ascii=False, indent=2))

def is_current_news_and_save_equal(current_news: dict):
    return json.load(open('json/saves.json', encoding='utf-8'))['name'] == current_news['name']