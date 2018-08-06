# coding=utf-8

import refcode as rc
import messages as msgs
import db
from config import bot, telebot, help_url, manager_id, bot2, wallet_id, price, secret_2, secret_1
import bot_time
from yandex_money.api import ExternalPayment
import requests
import re
from hashlib import md5
import airtabledb


def help(**kwargs):
    if 'id' in kwargs:
        bot.send_message(kwargs['id'], msgs.help.format(help_url))


def registration(user_id, text):
    refcode = rc.generate_code()
    if rc.has_refcode(text) and db.get_id_by_refcode(rc.extract_refcode(text)):
        parent_id = db.get_id_by_refcode(rc.extract_refcode(text))
        parent_name = db.get_name_by_id(parent_id)
        bot.send_message(user_id, msgs.hello_ref.format(parent_name, parent_id))
        parent_id_2 = db.get_parent_by_id(parent_id)
        parent_id_3 = db.get_parent_by_id(parent_id_2)
        for line_n, parent in enumerate([parent_id, parent_id_2, parent_id_3]):
            if parent is not None:
                line_c = db.increment_line(line_n, parent)
                airtabledb.increment_line(line_n, line_c, db.get_at_id(parent))
        db.add_user(user_id, refcode, bot_time.get_time(), parent_id, parent_id_2, parent_id_3)
        intro_1_f(id=user_id)
    else:
        parent_id = 398821553  # Айгуль ID
        parent_id_2 = None
        parent_id_3 = None
        for line_n, parent in enumerate([parent_id, parent_id_2, parent_id_3]):
            if parent is not None:
                line_c = db.increment_line(line_n, parent)
                airtabledb.increment_line(line_n, line_c, db.get_at_id(parent))
        # parent_name = db.get_name_by_id(parent_id)
        # bot.send_message(user_id, msgs.hello_ref.format(parent_name, parent_id))
        db.add_user(user_id, refcode, bot_time.get_time(), ref_parent=parent_id)
        intro_1_f(id=user_id)


def ask_name_f(**kwargs):
    if 'id' in kwargs and 'state' in kwargs:
        if kwargs['state'] < menu:
            markup = get_base_markup()
            bot.send_message(kwargs['id'], msgs.ask_name.format(kwargs['id']), reply_markup=markup)
            db.set_state(kwargs['id'], get_name_ask_phone)


def get_name_ask_phone_f(**kwargs):
    if 'id' in kwargs and 'text' in kwargs:
        db.set_name(kwargs['id'], kwargs['text'])
        phone_markup = get_phone_markup()
        bot.send_message(kwargs['id'], msgs.ask_phone, reply_markup=phone_markup)
        db.set_state(kwargs['id'], get_phone_ask_email)


def get_phone_ask_email_f(**kwargs):
    if 'id' in kwargs and 'text' in kwargs:
        if not isinstance(kwargs['text'], str):
            if kwargs['text'].contact.phone_number.startswith('+'):
                db.set_phone(kwargs['id'], kwargs['text'].contact.phone_number)
            else:
                db.set_phone(kwargs['id'], '+' + kwargs['text'].contact.phone_number)
            markup = get_base_markup()
            bot.send_message(kwargs['id'], msgs.ask_email, reply_markup=markup)
            db.set_state(kwargs['id'], get_email)
        else:
            db.set_phone(kwargs['id'], kwargs['text'])
            markup = get_base_markup()
            bot.send_message(kwargs['id'], msgs.ask_email, reply_markup=markup)
            db.set_state(kwargs['id'], get_email)


def get_phone_markup():
    phone_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_phone = telebot.types.KeyboardButton(text="Нажмите чтобы отправить телефон", request_contact=True)
    phone_markup.add(button_phone)
    phone_markup.add('⬅ Назад', '❓Помощь')
    return phone_markup


def get_email_f(**kwargs):
    if 'id' in kwargs and 'text' in kwargs:
        email_regexp = r"^[-a-z0-9!#$%&'*+/=?^_`{|}~]+(?:\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@(?:[a-z0-9]([-a-z0-9]{0," \
                       r"61}[a-z0-9])?\.)*(?:aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum" \
                       r"|name|net|org|pro|tel|travel|[a-z][a-z])$"
        if re.match(email_regexp, kwargs['text'].lower()):
            db.set_email(kwargs['id'], kwargs['text'])
            db.set_at_id(kwargs['id'], airtabledb.new_user(
                name=db.get_name_by_id(kwargs['id']),
                email=kwargs['text'],
                phone=db.get_phone_by_id(kwargs['id']),
                user_id=kwargs['id'],
                parent=db.get_at_id(db.get_parent_by_id(kwargs['id']))
            ))
            notify_about_ref(id=kwargs['id'])
            terms_of_use_f(id=kwargs['id'])
        else:
            bot.send_message(kwargs['id'], msgs.incorrect_email)


def notify_about_ref(**kwargs):
    if 'id' in kwargs:
        name = db.get_name_by_id(kwargs['id'])
        phone = db.get_phone_by_id(kwargs['id'])
        parent_id = db.get_parent_by_id(kwargs['id'])
        if parent_id:
            bot.send_message(parent_id, msgs.new_ref.format(name, phone))


def get_base_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('⬅ Назад', '❓Помощь')
    return markup


def intro_1_f(**kwargs):
    intro_1_markup = get_intro_1_markup()
    if 'id' in kwargs:
            db.set_state(kwargs['id'], intro_1)
            bot.send_message(kwargs['id'], db.get_video(), reply_markup=intro_1_markup)
            # bot.send_video(kwargs['id'], open('белый.wmv', 'rb'))


def get_intro_1_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('✅ Я посмотрел(а) видео')
    markup.add('❓Помощь')
    return markup


def intro_2_f(**kwargs):
    if 'id' in kwargs and 'state' in kwargs:
        if kwargs['state'] < menu:
            # print(bot.send_document(kwargs['id'], open('Презентация.pdf', 'rb')), 'Презентация.pdf')
            for file_id, caption in db.get_presentation_files():
                bot.send_document(chat_id=kwargs['id'], data=file_id, caption=caption, reply_markup=get_intro_2_markup())
            #bot.send_document(kwargs['id'], 'BQADAgADFQIAAn8ZCEpzWvPIxfNrGgI')
            db.set_state(kwargs['id'], intro_2)
            # bot.send_message(kwargs['id'], msgs.intro_2, reply_markup=get_intro_2_markup())


def get_intro_2_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('✅ Ознакомился(ась) с файлом')
    markup.add('❓Помощь')
    return markup


def intro_3_f(**kwargs):
    if 'id' in kwargs and 'state' in kwargs:
        if kwargs['state'] < menu:
            db.set_state(kwargs['id'], intro_2)
            bot.send_message(kwargs['id'], msgs.intro_3, reply_markup=get_intro_3_markup())


def get_intro_3_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Регистрация')
    markup.add('❓ Остались вопросы', '❓Помощь')
    return markup


def quests_left_f(**kwargs):
    if 'id' in kwargs and 'state' in kwargs:
        if kwargs['state'] < menu:
            db.set_state(kwargs['id'], quests_left)
            parent_id = db.get_parent_by_id(kwargs['id'])
            if parent_id is not None and parent_id != 398821553:
                parent_name = db.get_name_by_id(parent_id)
                parent_phone = db.get_phone_by_id(parent_id)
                faq = db.get_faq() + msgs.faq.format(parent_name, parent_phone, parent_id)
                bot.send_message(kwargs['id'], faq)
            else:
                faq = db.get_faq() + msgs.faq_no_par
                bot.send_message(kwargs['id'], faq)


def terms_of_use_f(**kwargs):
    markup = get_terms_of_use_markup()
    if 'id' in kwargs:
        db.set_state(kwargs['id'], terms_of_use)
        for file_id, caption in db.get_termsofuse_files():
            bot.send_document(chat_id=kwargs['id'], data=file_id, caption=caption, reply_markup=markup)
        #bot.send_document(kwargs['id'], 'BQADAgADnwEAAt_pCUp3fnumaw4FDAI')
        #bot.send_message(kwargs['id'], msgs.terms_of_use, reply_markup=markup)


def get_terms_of_use_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('✅ Принять')
    markup.add('⬅ Назад', '❓Помощь')
    return markup


def menu_f(**kwargs):
    if 'id' in kwargs:
        db.set_state(kwargs['id'], menu)
        bot.send_message(kwargs['id'], msgs.menu, reply_markup=get_menu_markup())


def get_menu_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('⚡ Пригласить', '🏪 Кабинет')
    markup.add('📚 Обучение', '📈 Каналы')
    markup.add('💳 Кошелек', '❓Помощь')
    return markup


def account_f(**kwargs):
    if 'id' in kwargs:
        check_new_month()
        db.set_state(kwargs['id'], account)
        reg_date = bot_time.get_reg_date(db.get_registred_time(kwargs['id']))
        balance = db.get_balance(kwargs['id'])
        parent_id = db.get_parent_by_id(kwargs['id'])
        if db.is_have_free_access(kwargs['id']):
            exp_date = 'бесплатная'
        else:
            exp_date = bot_time.get_exp_date(db.get_expiration_time(kwargs['id']))
            if exp_date is not None:
                exp_date = 'истекает ' + exp_date
            else:
                exp_date = 'не оплачена'
        if parent_id is not None and parent_id != 398821553:
            parent_name = db.get_name_by_id(parent_id)
            parent_phone = db.get_phone_by_id(parent_id)
            msg = msgs.account.format(parent_name, parent_phone, parent_id, exp_date, balance)
        else:
            msg = msgs.account_no_par.format(exp_date, balance)
        bot.send_message(kwargs['id'], msg, reply_markup=get_menu_markup())
        referal_f(id=kwargs['id'])


def referal_f(**kwargs):
    if 'state' in kwargs and kwargs['state'] < menu:
        return
    if 'id' in kwargs:
        line_1_len, line_2_len, line_3_len = db.get_lines_len_by_id(kwargs['id'])
        bot.send_message(kwargs['id'], msgs.referals.format(
            line_1_len, line_2_len, line_3_len
        ), reply_markup=get_referal_markup(line_1_len, line_2_len, line_3_len))


def get_referal_markup(line_1_len, line_2_len, line_3_len):
    markup = telebot.types.InlineKeyboardMarkup()
    if line_1_len > 0:
        markup.add(telebot.types.InlineKeyboardButton(text='Показать 1 линию', callback_data='line_1'))
    if line_2_len > 0:
        markup.add(telebot.types.InlineKeyboardButton(text='Показать 2 линию', callback_data='line_2'))
    if line_3_len > 0:
        markup.add(telebot.types.InlineKeyboardButton(text='Показать 3 линию', callback_data='line_3'))
    markup.add(telebot.types.InlineKeyboardButton(text='Итого', callback_data='total'))
    return markup


def show_line(user_id, chat_id, msg_id, line, line_n, rub):
    lens = db.get_lines_len_by_id(user_id)
    msg = msgs.rline.format(line_n, rub) + '\n'
    if line:
        for user_id in line:
            user_id = user_id[0]
            msg += msgs.referal.format(db.get_name_by_id(user_id),
                                       db.get_phone_by_id(user_id),
                                       bot_time.get_reg_date(db.get_registred_time(user_id))) + '\n'
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=msg,
            reply_markup=get_referal_markup(lens[0], lens[1], lens[2])
        )


def show_total(user_id, msg_id, chat_id):
    lens = db.get_lines_len_by_id(user_id)
    nmonth_salary = lens[0]*2000 + lens[1]*1000 + lens[2]*500
    month_salary = db.get_salary(user_id)
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg_id,
        text=msgs.total.format(month_salary, nmonth_salary),
        reply_markup=get_referal_markup(lens[0], lens[1], lens[2])
    )


def back(**kwargs):
    if 'id' in kwargs and 'state' in kwargs:
        if kwargs['state'] < menu or kwargs['state'] == pay:
            if kwargs['state'] == intro_2:
                intro_1_f(id=kwargs['id'])
            else:
                intro_2_f(id=kwargs['id'], state=kwargs['state'])
        else:
            db.set_state(kwargs['id'], account)
            menu_f(id=kwargs['id'])


def invite_user_f(**kwargs):
    if 'state' in kwargs and kwargs['state'] < menu:
        return
    if 'id' in kwargs:
        db.set_state(kwargs['id'], invite_user)
        bot.send_message(kwargs['id'],
                         msgs.reflink.format(rc.generate_reflink(db.get_refcode_by_id(kwargs['id']))),
                         reply_markup=get_menu_markup())


def get_pay_markup(payment_link):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='💳 Оплатить 7000', url=payment_link))
    return markup


def check_new_month():
    if bot_time.current_month != bot_time.get_cur_month():
        bot_time.current_month = bot_time.get_cur_month()
        db.new_month()


def remove_keyboard():
    return telebot.types.ReplyKeyboardRemove()


def get_payment_link(code, email):
    sign = md5('{}:{}:{}:{}'.format(
        wallet_id, price, secret_1, code
    ).encode('utf-8')).hexdigest()
    return 'http://www.free-kassa.ru/merchant/cash.php?m={}&oa={}&o={}&s={}&lang=ru&i=&em={}'.format(
        wallet_id, price, code, sign, email
    )


def please_wait_f(**kwargs):
    if 'id' in kwargs and 'state' in kwargs:
        if kwargs['state'] < menu:
            bot.send_message(kwargs['id'], msgs.wait, reply_markup=remove_keyboard())
            pay_f(id=kwargs['id'])


def channels_f(**kwargs):
    if 'id' in kwargs:
        db.set_state(kwargs['id'], channels)
        bot.send_message(kwargs['id'], db.get_channels(), reply_markup=get_menu_markup())


def learning_f(**kwargs):
    if 'id' in kwargs:
        db.set_state(kwargs['id'], learning)
        #bot.send_message(kwargs['id'], msgs.learning, reply_markup=get_learning_markup())
        for file_id, caption in db.get_signal_files():
            bot.send_document(chat_id=kwargs['id'], data=file_id, caption=caption, reply_markup=get_learning_markup())
        bot.send_message(kwargs['id'],
            '''Как делать ставку в приложении 1xBet
            https://youtu.be/a6QEXixoj9o
            ''')
        bot.send_message(kwargs['id'], 
            '''Как установить приложение 1xbet на IOS
            https://youtu.be/OFGabxNqTqc
            ''')
        bot.send_message(kwargs['id'],
            '''Как установить приложение 1xbet на ANDROID
            https://youtu.be/gU-l1yFRpUQ
            ''')
        # print(bot.send_document(kwargs['id'], open('VSB обучение по сигналам.pdf', 'rb')), 'VSB обучение по сигналам.pdf')
        # bot.send_document(kwargs['id'], 'BQADAgADqgEAAt_pCUqwCsH4yRpi-wI')


def wallet_f(**kwargs):
    if 'id' in kwargs:
        db.set_state(kwargs['id'], wallet)
        bot.send_message(kwargs['id'], msgs.choose, reply_markup=get_wallet_markup())


def get_wallet_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('💳 Заказать выплату', '💳 Оплатить подписку')
    markup.add('⬅ Назад')
    return markup


def pay_f(**kwargs):
    if 'id' in kwargs:
        code = rc.generate_code()
        sign = md5('{}:{}:{}:{}'.format(
            wallet_id, price, secret_2, code
        ).encode('utf-8')).hexdigest()
        markup = get_pay_markup(get_payment_link(code, db.get_email(kwargs['id'])))
        bot.send_message(kwargs['id'], msgs.pay1, reply_markup=markup)
        db.set_paysign(kwargs['id'], sign)


def ask_amount_f(**kwargs):
    if 'id' in kwargs:
        bot.send_message(kwargs['id'], msgs.howmuch, reply_markup=get_base_markup())
        db.set_state(kwargs['id'], get_amount_ask_creds)


def get_amount_ask_creds_f(**kwargs):
    if 'id' in kwargs and 'text' in kwargs:
        try:
            amount = float(kwargs['text'].replace(',', '.'))
            db.set_amount(kwargs['id'], amount)
            bot.send_message(kwargs['id'], msgs.getcreds)
            db.set_state(kwargs['id'], get_creds)
        except ValueError:
            ask_amount_f(id=kwargs['id'], text=kwargs['text'])


def get_creds_f(**kwargs):
    if 'id' in kwargs and 'text' in kwargs:
        amount = float(db.get_amount(kwargs['id']))
        balance = float(db.get_balance(kwargs['id']))
        if amount > balance:
            bot.send_message(kwargs['id'], msgs.nomoney)
            menu_f(id=kwargs['id'])
        else:
            db.set_balance(kwargs['id'], balance-amount)
            bot.send_message(manager_id, msgs.exchange.format(
                amount, db.get_name_by_id(kwargs['id']), kwargs['text']))
            bot.send_message(kwargs['id'], msgs.managered)
            menu_f(id=kwargs['id'])


def distribution(text):
    subs = db.select_subs()
    for sub in subs:
        # print(sub[0])
        bot2.send_message(sub[0], text)


def learning_2_f(**kwargs):
    if 'id' in kwargs:
        for file_id, caption in db.get_franchise_files():
            bot.send_document(chat_id=kwargs['id'], data=file_id, caption=caption)
        #bot.send_message(kwargs['id'], msgs.learning2, reply_markup=get_learning_markup())
        #bot.send_message(kwargs['id'], '🔹 C чего начать?')
        #bot.send_document(kwargs['id'], 'BQADAgADFgIAAn8ZCEr8OHwQ62-YFgI')
        #bot.send_message(kwargs['id'], '🔹 Выйти на новый уровень')
        #bot.send_document(kwargs['id'], 'BQADAgADqwEAAt_pCUoN2S6FK3RHygI')
        #bot.send_message(kwargs['id'], '🔹 Откуда брать людей?')
        #bot.send_document(kwargs['id'], 'BQADAgADrAEAAt_pCUqSY9BPudkcqwI')
        #bot.send_message(kwargs['id'], '🔹 План минимум')
        #bot.send_document(kwargs['id'], 'BQADAgADrQEAAt_pCUqdQ-GlTyyJSQI')
        #bot.send_message(kwargs['id'], '🔹 Как проводить живые презентации?')
        #bot.send_document(kwargs['id'], 'BQADAgADrgEAAt_pCUq5ucTdoto_TAI')


def learning_0_f(**kwargs):
    if 'id' in kwargs:
        bot.send_message(kwargs['id'], 'Обучение', reply_markup=get_learning_markup())


def get_learning_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('📚 Обучение по сигналам', '📚 Обучение по франшизе')
    markup.add('🏈 Ссылки на 1xBET')
    markup.add('⬅ Назад')
    return markup


def get_learning_3_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    links = db.get_links()
    #print(links)
    markup.add(telebot.types.InlineKeyboardButton(text='Сайт', url=links[0]))
    markup.add(telebot.types.InlineKeyboardButton(text='Мобильное приложение', url=links[1]))
    return markup


def learning_3_f(**kwargs):
    if 'id' in kwargs:
        bot.send_message(kwargs['id'], 'Ссылки на 1xBET', reply_markup=get_learning_3_markup())


def write_to_bot_2_f(**kwargs):
    if 'id' in kwargs:
        db.set_state(kwargs['id'], write_to_bot_2)
        bot.send_message(kwargs['id'], msgs.write_msg_to_bot_2, reply_markup=get_write_msg_to_bot_2_markup())


def get_write_msg_to_bot_2_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('✍ Написал(а)')
    return markup


def pay_success(user_id, is_first_pay):
    if is_first_pay:
        bot.send_message(user_id, msgs.firstpay)
    else:
        bot.send_message(user_id, 'Вы успешно оплатили подписку на месяц')


def free_access(user_id):
    bot.send_message(user_id, 'Вы получили бесплатную подписку! 🎁')
    menu_f(id=user_id)


def no_free_access(user_id):
    bot.send_message(user_id
        , '''У вас закончилась бесплатная подписка, чтобы продолжить работу сервиса, вам необходимо произвести оплату.
Если у вас остались вопросы, обратитесь в службу поддержки @vsb_support''')
    menu_f(id=user_id)


def get_file_id(filename):
    return bot.send_document(128109574, open(filename, 'rb')).document.file_id


msg_cases = {
    'Регистрация': ask_name_f,
    '⬅ Назад': back,
    '❓Помощь': help,
    '⚡ Пригласить': invite_user_f,
    'Оплатить подписку': pay_f,
    '✅ Я посмотрел(а) видео': intro_2_f,
    '❓ Остались вопросы': quests_left_f,
    '✅ Принять': please_wait_f,
    '🏪 Кабинет': account_f,
    '📈 Каналы': channels_f,
    '📚 Обучение': learning_0_f,
    '📚 Обучение по сигналам': learning_f,
    '📚 Обучение по франшизе': learning_2_f,
    '💳 Кошелек': wallet_f,
    '💳 Оплатить подписку': pay_f,
    '💳 Заказать выплату': ask_amount_f,
    '✅ Ознакомился(ась) с файлом': intro_3_f,
    '🏈 Ссылки на 1xBET': learning_3_f,
    '✍ Написал(а)': menu_f
}


quests_left = 0
intro_1 = 1
intro_2 = 2
intro_3 = 3
get_name_ask_phone = 4
get_phone_ask_email = 5
get_email = 6
registred = 7
terms_of_use = 8
pay = 9
write_to_bot_2 = 10
menu = 11
account = 12
invite_user = 13
channels = 14
learning = 15
wallet = 16
ask_amount = 17
get_amount_ask_creds = 18
get_creds = 19

state_cases = {
    quests_left: quests_left_f,
    intro_1: intro_1_f,
    intro_2: intro_2_f,
    terms_of_use: terms_of_use_f,
    get_name_ask_phone: get_name_ask_phone_f,
    get_phone_ask_email: get_phone_ask_email_f,
    get_email: get_email_f,
    menu: menu_f,
    account: account_f,
    invite_user: invite_user_f,
    channels: channels_f,
    get_amount_ask_creds: get_amount_ask_creds_f,
    get_creds: get_creds_f,
    wallet: wallet_f,
    write_to_bot_2: write_to_bot_2_f
}
