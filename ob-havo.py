from telegram import InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,MessageHandler,Filters
import requests
from bs4 import BeautifulSoup as BS


buttons = [
        ["Aloqa","Biz haqimizda"],
        
        ["Manzil"]
    ]

replys_markup = ReplyKeyboardMarkup(buttons,
                                       resize_keyboard=True)


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

def aloqa(update, context):
    text = 'Aloqa'
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=text)  

def bizxaqimizda(update:Update, context):
    text = 'Manzil'
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=text) 
def location(update, context):

    update.message.reply_location(2,2) 


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
                              reply_markup=InlineKeyboardMarkup(city()),)
def help(update,context):
    update.message.reply_text("Bu bot 12 viloyat ob-havo ma'lumotini ko'rsatadi.\nAdmin:@MuslimMuslih")

def about(update, context):
    user = update.message.from_user
    update.message.reply_text(f"""Salom {user.first_name} 🖐🏼\nBu yerda biz haqimizda ma'lumot olishingiz mumkin 👇""",
                              reply_markup=replys_markup)


def main():
    Token = "2066983997:AAH8_5X2qp2n_oYsyMCZXPF5SMz_saydKqI"
    updater = Updater(Token)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_handler(CallbackQueryHandler(inline_handlerlar))
    updater.dispatcher.add_handler(CommandHandler("about", about))
    aloqa_hendler = MessageHandler(Filters.text('Aloqa'),aloqa)
    updater.dispatcher.add_handler(aloqa_hendler)

    about_hendler = MessageHandler(Filters.text('Biz haqimizda'),bizxaqimizda)
    updater.dispatcher.add_handler(about_hendler)

    location_hendler = MessageHandler(Filters.text('Manzil'),location)
    updater.dispatcher.add_handler(location_hendler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

# Weather bot for Co-Learning center