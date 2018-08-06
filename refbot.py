from config import bot
import db
import core
import time


@bot.message_handler(content_types=['text'])
def process(message):
    user_id = message.chat.id
    text = message.text
    if db.is_new_user(user_id):
        core.registration(user_id, text)
    elif db.is_blocked(user_id):
        return None
    elif text in core.msg_cases:
            core.msg_cases[text](id=user_id, state=db.get_state(user_id))
    else:
        core.state_cases[db.get_state(user_id)](id=user_id, text=text)


@bot.message_handler(content_types=['contact'])
def process_contact(message):
    user_id = message.chat.id
    if db.is_blocked(user_id):
        return None
    text = message
    if db.is_new_user(user_id):
        core.registration(user_id, text)
    else:
        if text in core.msg_cases:
            core.msg_cases[text](id=user_id, state=db.get_state(user_id))
        else:
            core.state_cases[db.get_state(user_id)](id=user_id, text=text)


@bot.callback_query_handler(func=lambda c: c.data)
def process_callback(callback):
    ref_cdatas = ['line_1', 'line_2', 'line_3', 'total']
    chat_id = callback.message.chat.id
    msg_id = callback.message.message_id
    user_id = callback.from_user.id
    if db.is_blocked(user_id):
        return None
    cdata = callback.data
    if cdata not in ref_cdatas:
        core.edit_msg(chat_id, msg_id, cdata)
    else:
        if cdata == 'line_1':
            core.show_line(user_id, chat_id, msg_id, db.get_line_1_by_id(user_id), 1, 2000)
        elif cdata == 'line_2':
            core.show_line(user_id, chat_id, msg_id, db.get_line_2_by_id(user_id), 2, 1000)
        elif cdata == 'line_3':
            core.show_line(user_id, chat_id, msg_id, db.get_line_3_by_id(user_id), 3, 500)
        else:
            core.show_total(user_id, msg_id, chat_id)


def referal_bot_loop():
    while True:
        try:
            bot.polling(none_stop=True, interval=2)
            break
        except Exception as ex:
            print(ex)
            bot.stop_polling()
            time.sleep(15)

