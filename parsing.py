import requests
from bs4 import BeautifulSoup, Tag, NavigableString

import json
import work_with_files as fw

Element = Tag | NavigableString

# ROOT = /html/body/section/div[0]/div[1]/div[0]/div
# IMG = ROOT/div[0]/img
# CONTENT = ROOT/div[1]/
# LINK = CONTENT/a
# SHORT_TEXT = CONTENT/p
# DATE = CONTENT/div/time

def parse_fpt_last_news():
    URL = 'https://feopoliteh.ru/news'
    fpt_news = {}

    res = requests.get(URL)

    soup = BeautifulSoup(res.text, 'html.parser')
    
    root: Element = soup.find('section').find_all('div')[0].find_all('div')[1].find_all('div')[0].find('div')
    img: Element = root.find('div').find('img')
    content: Element = root.find_all('div', recursive=False)[1]

    link: Element = content.find('a')
    short_text: Element = content.find('p')
    date: Element = content.find('div').find('time')

    fpt_news['name'] = link.text
    fpt_news['href'] = link.get('href', '')
    fpt_news['date'] = date.text
    fpt_news['shortText'] = short_text.text
    fpt_news['imgSrc'] = img.get('data-src', '')

    return fpt_news

def save_news(obj):
    fw.file_writer('json/saves.json', json.dumps(obj, ensure_ascii=False, indent=2))

def is_current_news_and_save_equal(current_news: dict):
    return json.load(open('json/saves.json', encoding='utf-8'))['name'] == current_news['name']

print(parse_fpt_last_news())