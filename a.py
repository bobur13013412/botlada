import time
from bs4 import BeautifulSoup
import telebot
import json
import requests

API_TOKEN = '1943057560:AAGWP8EnUSHd42fRZot-MG7PR7ZQ3p1qfX8'

bot = telebot.TeleBot(API_TOKEN, threaded=False)

jonatilgan = []
try:
    jonatilgan = json.loads(open("./jonatilgan.json", "r").read())
except:
    pass


def ret(f, *args, **kwargs):
    i = 0
    while (True):
        try:
            res = f(*args, **kwargs)
            i=0
            return res
        except Exception as ex:
            i+=1
            if(i>20):
                return
            print(ex)
            time.sleep(60*30)


while (True):
    all_links = []
    for i in range(1, 5):
        page = ret(requests.get, 'https://kun.uz/uz/news/news/search?q=bojxona&page=' + str(i))
        bSoup = BeautifulSoup(page.content, 'html.parser')
        links = bSoup.find_all('a', class_="news__title")
        all_links = all_links + links

    for link in all_links:
        if 'href' in link.attrs:
            a = "https://kun.uz" + str(link.attrs['href'])
            if (not a in jonatilgan):
                print(a + "\n")
                jonatilgan.append(a)
                open("./jonatilgan.json", "w").write(json.dumps(jonatilgan))
                ret(bot.send_message, "@sanlaodam", "[Batafsil bilish uchun shu yerga bosing](" + a + ")\n#uz", parse_mode="markdown")
                time.sleep(60*20)