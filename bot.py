import telebot as tg

# import json
import time

from parsing import *
from utils import *

bot = tg.TeleBot(get_config('token'))

GLOBAL = {
    'is_bot_must_work': False
}

def is_not_have_admin_right(m):
    if not is_user_in_white_list(get_username(m)):
        info(m, bot, 'Вы не обладаете правами администратора!')
        return True
    
    return False

def get_checking_interval(m):
    try:
        interval_time = abs(int(m.text))
        edit_config({
            'checkingIntervalTime': interval_time
        })
        info(m, bot, f'Значение изменено на {interval_time}')
        restart(m)
    except:
        info(m,bot, 'Введено неверное значение. Попробуйте еще раз! /edit_interval')
            
def check_password_right(m):
    if m.text == get_config('password'):
        add_new_admin(m)
    else:
        info(m, bot, 'Пароль неверен! Попробуйте еще раз! /password')

def add_new_admin(m):
    info(m, bot, 'Вы стали администратором! Поздравляю!')
    edit_config({
        'adminsID': get_username(m)
    })

def post_news(news: dict):

    text = f'''
    *{news['name']}*

    {news['shortText']}

    [Читать далее...]({news['href']})
    '''
    with open('newsPhoto.png', 'rb') as img:
        bot.send_photo(get_config('groupID'), img, text, 'Markdown')

def is_user_in_white_list(user: str):
    for admin in get_config('adminsID'):
        if admin == user: return True
    
    return False

def get_username(message):
    try:
        return message.from_user.username
    except:
        return message.from_user.id


@bot.message_handler(['start'])
def start(m):
    print(m.text)
    if GLOBAL['is_bot_must_work']:
        info(m, bot, 'Бот уже запущен')
        return

    if is_not_have_admin_right(m):
        return
    
    GLOBAL['is_bot_must_work'] = True

    info(m, bot, 'Бот начал работу!')

    try:
        while GLOBAL['is_bot_must_work']:
            news = parse_fpt_last_news()
            if not is_current_news_and_save_equal(news): 
                save_news(news)
                fw.file_writer('newsPhoto.png', news['imgSrc'], 'b')

                post_news(news)
                info(m, bot, 'Выложен пост')
            else:
                print('Новых новостей не было обнаружено')

            time.sleep(get_config('checkingIntervalTime'))
    except Exception as e:
        info(m, bot , f'Ошибка: {e}')
        restart(m)

@bot.message_handler(['stop'])
def stop(m):
    if not is_not_have_admin_right(m):
        info(m, bot, 'Бот остановлен!')
        GLOBAL['is_bot_must_work'] = False

@bot.message_handler(commands=['restart'])
def restart(m):
    stop(m)
    start(m)

@bot.message_handler(commands=['password'])
def password(m):
    if is_user_in_white_list(get_username(m)):
        info(m, bot, "Вы уже являетесь администратором. Нет необходимости вводить пароль!")
        return
    
    info(m, bot, "Введите пароль!")
    bot.register_next_step_handler(m, check_password_right)

@bot.message_handler(commands=['edit_interval'])
def edit_interval(m):
    if not is_not_have_admin_right(m):
        info(m, bot, "Укажите интервал времени(в секундах), когда будет проверяться новые новости с сайта.")
        bot.register_next_step_handler(m, get_checking_interval)

print('Bot is starting!')
bot.polling(skip_pending=True)