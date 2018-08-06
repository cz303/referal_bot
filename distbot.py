from config import bot2
import distcore
import time

admins = [128109574, 453743812, 187335736, 361538703]

@bot2.message_handler(func=lambda m: m.chat.id in admins)
def process(message):
    user_id = message.chat.id
    text = message.text
    if text in distcore.msg_cases:
        distcore.msg_cases[text](id=user_id)
    else:
        distcore.state_cases[distcore.state](id=user_id, text=text)


def distribution_bot_loop():
    while True:
        try:
            bot2.polling(none_stop=True, interval=2)
            break
        except Exception as ex:
            print(ex)
            bot2.stop_polling()
            time.sleep(15)

