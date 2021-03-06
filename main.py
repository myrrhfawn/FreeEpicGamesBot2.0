import parse
import os
import telebot
from telebot import types
from flask import Flask, request
from datetime import datetime, timedelta
import locale


TOKEN = "2118961153:AAFISocvOir_rVhDEXMGHUL4NCJaaMzg4ng"
APP_URL = 'https://freeepicgamesbot.herokuapp.com/'+TOKEN
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['free'])
def free(message):
    chat_id = message.chat.id
    games = parse.parse()
    for element in games:
        if element['promotions'] and element['promotions']['promotionalOffers'] and not element['promotions']['upcomingPromotionalOffers']:
            date = element['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate']
            d = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.000Z") + timedelta(hours=2)
            endData = f"Безплатно до {d.strftime('%H:%M %d %b.')}"

            title = f" *{element['title']}*\n\n{element['description']}\n*{endData}*"
            id = element['productSlug']
            url = f'https://www.epicgames.com/store/ru/p/{id}'
            photo = element['keyImages'][1]['url']
            print(f"Title: {title}\nURL: {url}\nImage: {photo}")
            markup = types.InlineKeyboardMarkup(row_width=1)
            item = types.InlineKeyboardButton('Перейти', url=url)
            markup.add(item)
            bot.send_photo(chat_id=chat_id,
                    parse_mode='Markdown',
                    photo=photo,
                    caption=title,
                    reply_markup=markup
                    )


@bot.message_handler(commands=['next'])
def free(message):
    chat_id = message.chat.id
    games = parse.parse()
    for element in games:
        if element['promotions'] and element['promotions']['upcomingPromotionalOffers']:
            edate = element['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0]['endDate']
            ed = datetime.strptime(edate, "%Y-%m-%dT%H:%M:%S.000Z") + timedelta(hours=2)
            sdate = element['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0]['startDate']
            sd = datetime.strptime(sdate, "%Y-%m-%dT%H:%M:%S.000Z") + timedelta(hours=2)
            data = f"Безплатно з {sd.strftime('%d %b')} до {ed.strftime('%d %b.')}"

            title = f" *{element['title']}*\n\n{element['description']}\n*{data}*"
            id = element['productSlug']
            url = f'https://www.epicgames.com/store/ru/p/{id}'
            photo = element['keyImages'][1]['url']
            print(f"Title: {title}\nURL: {url}\nImage: {photo}")
            markup = types.InlineKeyboardMarkup(row_width=1)
            item = types.InlineKeyboardButton('Перейти', url=url)
            markup.add(item)
            bot.send_photo(chat_id=chat_id,
                    parse_mode='Markdown',
                    photo=photo,
                    caption=title,
                    reply_markup=markup
                    )


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200

if __name__ == '__main__':
    print("start")
    locale.setlocale(locale.LC_TIME, 'ru_UA.utf8')
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
