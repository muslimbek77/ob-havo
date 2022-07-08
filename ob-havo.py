from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import requests
from bs4 import BeautifulSoup as BS


viloyat ={
    'Andijan':'погода-андижан',
    'Toshkent':'погода-ташкент',
    'Namangan':'погода-наманган',
    'Farg\'ona':'погода-фергана',
    'Buxoro':'погода-бухара',
    'Jizzax':'погода-джизак',
    'Xorazm':'погода-ургенч',
    'Navoiy':'погода-навои',
    'Qashqadaryo':'погода-карши',
    'Qoraqalpog\'iston Respublikasi':'погода-нукус',
    'Samarqand':'погода-самарканд',
    'Sirdaryo':'погода-сырдарья',
    'Surxondaryo':'погода-термез'
}


def choose_city(city):
    t = requests.get(f'https://sinoptik.ua/{viloyat[city]}')
    html_t = BS(t.content, 'html.parser')
    for el in html_t.select('#content'):
        min = el.select('.temperature .min')[0].text
        max = el.select('.temperature .max')[0].text
        print(min,max)
        t_min = min[4:]
        t_max = max[5:]
    return f'{t_min}\nmax {t_max}'


def city():

    return [
        [InlineKeyboardButton("Toshkent", callback_data=f"Toshkent"),InlineKeyboardButton("Andijon", callback_data=f"Andijan")],
        [InlineKeyboardButton("Namangan", callback_data=f"Namangan"),InlineKeyboardButton("Farg\'ona", callback_data=f"Farg\'ona")],
        [InlineKeyboardButton("Buxoro", callback_data=f"Buxoro"),InlineKeyboardButton("Jizzax", callback_data=f"Jizzax")],
        [InlineKeyboardButton("Xorazm", callback_data=f"Xorazm"),InlineKeyboardButton("Navoiy", callback_data=f"Navoiy")],
        [InlineKeyboardButton("Qashqadaryo", callback_data=f"Qashqadaryo"),InlineKeyboardButton("Samarqand", callback_data=f"Samarqand")],
        [InlineKeyboardButton("Sirdaryo", callback_data=f"Sirdaryo"),InlineKeyboardButton("Surxondaryo", callback_data=f"Surxondaryo")],
        [InlineKeyboardButton("Qoraqalpog\'iston Respublikasi", callback_data=f"Qoraqalpog\'iston Respublikasi")],
    ]


def back():
    return [
        [InlineKeyboardButton("Orqaga", callback_data=f"back1")]
    ]


def inline_handlerlar(update, context):
    query = update.callback_query
    data = query.data.split("_")

    if data[0] in viloyat.keys():
        query.message.edit_text(f"Bugun {data[0]}da havo o`zgarib turadi\nmin {choose_city(data[0])}\nbo`lishi kutilmoqda ⛅",
                                reply_markup=InlineKeyboardMarkup(back()))

    elif data[0] == 'back1':
        query.message.edit_text(
            f"Bu yerdan Kerakli joy nomini tanlang 👇",
            reply_markup=InlineKeyboardMarkup(city()))


def start(update, context):
    user = update.message.from_user
    update.message.reply_text(f"""Salom {user.first_name} 🖐🏼\nBu yerdan Kerakli joy nomini tanlang 👇""",
                              reply_markup=InlineKeyboardMarkup(city()))
def help(update,context):
    update.message.reply_text("Bu bot 12 viloyat ob-havo ma'lumotini ko'rsatadi.\nAdmin:@MuslimMuslih")

def main():
    Token = "5317958815:AAG7XdqdenDvwDf4Y41XeHV2hzIwv4LvBPw"
    updater = Updater(Token)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_handler(CallbackQueryHandler(inline_handlerlar))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

# Weather bot for Co-Learning center