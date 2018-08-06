from config import bot2, bot
import telebot
import messages
import db
import airtabledb

state = 0


def menu(**kwargs):
    if 'id' in kwargs:
        bot2.send_message(kwargs['id'], 'Меню', reply_markup=get_menu_markup())


def get_menu_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Рассылка')
    markup.add('Изменение ссылок на 1xBET')
    markup.add('Управление ботом')
    return markup


def link_update(**kwargs):
    if 'id' in kwargs:
        bot2.send_message(kwargs['id'], messages.link_update, reply_markup=get_menu_markup())
        global state
        state = 1


def get_link_update(**kwargs):
    if 'id' in kwargs and 'text' in kwargs:
        xbet_link = kwargs['text']
        xbet_mobile_link = kwargs['text'] + '&r=mobile'
        db.update_links(xbet_link, xbet_mobile_link)
        bot2.send_message(kwargs['id'], 'Ссылки успешно изменены', reply_markup=get_menu_markup())
        menu(id=kwargs['id'])


def distribution(**kwargs):
    if 'id' in kwargs:
        bot2.send_message(kwargs['id'], 'Что вы хотите сделать?', reply_markup=get_distribution_markup())


def get_distribution_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Рассылка всем пользователям')
    markup.add('Рассылка пользователям с оплаченной подпиской')
    markup.add('Рассылка через Airtable')
    markup.add('Меню')
    return markup


def distribution_all(**kwargs):
    bot2.send_message(kwargs['id'], messages.distribution, reply_markup=get_back_markup())
    global state
    state = 2


def distribution_payed(**kwargs):
    bot2.send_message(kwargs['id'], messages.distribution_payed, reply_markup=get_back_markup())
    global state
    state = 3


def distribute_all(**kwargs):
    if 'id' in kwargs and 'text' in kwargs:
        ids = db.select_users()
        #print('Рассылка всем пользователям')
        for user_id in ids:
            #print(user_id[0])
            bot.send_message(user_id[0], kwargs['text'])
        bot2.send_message(kwargs['id'], 'Сообщение разослано')
        global state
        state = 0
        menu(id=kwargs['id'])


def distribute_payed(**kwargs):
    if 'id' in kwargs and 'text' in kwargs:
        subs = db.select_subs()
        #print('Рассылка оплатившим пользователям')
        for sub in subs:
            try:
                bot2.send_message(sub[0], kwargs['text'])
            except:
                pass
    bot2.send_message(kwargs['id'], 'Сообщение разослано')
    global state
    state = 0
    menu(id=kwargs['id'])


def distribution_airtable(**kwargs):
    if 'id' in kwargs:
        bot2.send_message(kwargs['id'], messages.airtable_dist, reply_markup=get_dist_markup())


def distribution_airtable_2(**kwargs):
    if 'id' in kwargs:
        bot2.send_message(kwargs['id'], messages.distribution, reply_markup=get_back_markup())
        global state
        state = 4


def disribute_airtable(**kwargs):
    if 'id' in kwargs and 'text' in kwargs:
        for user_id in airtabledb.get_dist_list():
            bot.send_message(user_id, kwargs['text'])
        bot2.send_message(kwargs['id'], 'Сообщение разослано')
        global state
        state = 0
        menu(id=kwargs['id'])


def get_dist_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Готово')
    markup.add('Меню')
    return markup


def get_back_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Меню')
    return markup


def bot_management(**kwargs):
    if 'id' in kwargs:
        bot2.send_message(kwargs['id'], 'Что вы хотите сделать?', reply_markup=get_bot_management_markup())


def get_bot_management_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Изменение файлов')
    markup.add('Изменение сообщений и ссылок')
    markup.add('Бесплатный доступ и блокировка')
    markup.add('Меню')
    return markup


def base_management(**kwargs):
    if 'id' in kwargs:
        bot2.send_message(kwargs['id'], messages.base_management, reply_markup=get_bm_markup())


def get_bm_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Синхронизировать базу')
    markup.add('Меню')
    return markup


def base_update(**kwargs):
    if 'id' in kwargs:
        bot2.send_message(kwargs['id'], 'Пожалуйста подождите...')
        airtabledb.update_base()
        bot2.send_message(kwargs['id'], 'База синхронизирована')
        global state
        state = 0
        menu(id=kwargs['id'])


def file_update(**kwargs):
    if 'id' in kwargs:
        bot2.send_message(kwargs['id'], messages.file_update, reply_markup=get_file_update_markup())


def get_file_update_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Обновить файлы')
    markup.add('Меню')
    return markup


def update_files(**kwargs):
    if 'id' in kwargs:
        bot2.send_message(kwargs['id'], 'Пожалуйста подождите...')
        airtabledb.update_files()
        bot2.send_message(kwargs['id'], 'Файлы обновлены')
        global state
        state = 0
        menu(id=kwargs['id'])


def message_update(**kwargs):
    if 'id' in kwargs:
        bot2.send_message(kwargs['id'], messages.message_update, reply_markup=get_msg_update_markup())


def get_msg_update_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Обновить сообщения')
    markup.add('Меню')
    return markup


def update_messages(**kwargs):
    if 'id' in kwargs:
        bot2.send_message(kwargs['id'], 'Пожалуйста подождите...')
        airtabledb.update_messages()
        bot2.send_message(kwargs['id'], 'Сообщения обновлены')
        global state
        state = 0
        menu(id=kwargs['id'])


msg_cases = {
    'Рассылка': distribution,
    'Изменение ссылок на 1xBET': link_update,
    'Рассылка всем пользователям': distribution_all,
    'Рассылка пользователям с оплаченной подпиской': distribution_payed,
    'Рассылка через Airtable': distribution_airtable,
    'Меню': menu,
    'Готово': distribution_airtable_2,
    'Управление ботом': bot_management,
    'Бесплатный доступ и блокировка': base_management,
    'Синхронизировать базу': base_update,
    'Изменение файлов': file_update,
    'Обновить файлы': update_files,
    'Изменение сообщений и ссылок': message_update,
    'Обновить сообщения': update_messages
}


state_cases = {
    0: menu,
    1: get_link_update,
    2: distribute_all,
    3: distribute_payed,
    4: disribute_airtable
}

