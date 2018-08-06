import sqlite3
import config
import time
from threading import Lock


conn = sqlite3.connect(config.database, check_same_thread=False, timeout=1)
cursor = conn.cursor()
lock = Lock()


def get_id_by_refcode(refcode):
    try:
        lock.acquire()
        sql = 'select ID from USERS where REFERAL_CODE=?'
        cursor.execute(sql, (refcode,))
        fetch = cursor.fetchone()
        if fetch is not None:
            return fetch[0]
        else:
            return None
    finally:
        lock.release()


def add_user(user_id, refcode, time_s, ref_parent=None, ref_parent_2=None, ref_parent_3=None):
    try:
        lock.acquire()
        if ref_parent is None:
            sql = 'insert into USERS (ID, REFERAL_CODE, REGISTRED_TIME) values(?, ?, ?)'
            cursor.execute(sql, (str(user_id), str(time_s), refcode))
        else:
            sql = '''
insert into USERS (ID, REFERAL_CODE, REFERAL_PARENT, REFERAL_PARENT_2, REFERAL_PARENT_3, REGISTRED_TIME)
 values(?, ?, ?, ?, ?, ?)'''
            cursor.execute(sql,
                           (str(user_id), refcode, ref_parent, ref_parent_2, ref_parent_3, str(time_s)))
        conn.commit()
    finally:
        lock.release()


def is_new_user(user_id):
    try:
        lock.acquire()
        cursor.execute('select * from USERS where ID=?', (str(user_id),))
        return cursor.fetchone() is None
    finally:
        lock.release()


def is_trained(user_id):
    try:
        lock.acquire()
        cursor.execute('select IS_TRAINED from USERS where ID=?', (str(user_id),))
        return cursor.fetchone()[0] == 1
    finally:
        lock.release()


def is_registred(user_id):
    try:
        lock.acquire()
        cursor.execute('select EMAIL from USERS where ID=?', (str(user_id),))
        return cursor.fetchone()[0] is not None
    finally:
        lock.release()


def get_state(user_id):
    try:
        lock.acquire()
        cursor.execute('select STATE from USERS where ID=?', (str(user_id),))
        return cursor.fetchone()[0]
    finally:
        lock.release()


def get_amount(user_id):
    try:
        lock.acquire()
        cursor.execute('select AMOUNT from USERS where ID=?', (str(user_id),))
        return cursor.fetchone()[0]
    finally:
        lock.release()


def set_state(user_id, state):
    try:
        lock.acquire()
        cursor.execute('update USERS set STATE = ? where ID = ?', (state, str(user_id)))
        conn.commit()
    finally:
        lock.release()


def set_name(user_id, name):
    try:
        lock.acquire()
        cursor.execute('update USERS set NAME = ? where ID = ?', (name, str(user_id)))
        conn.commit()
    finally:
        lock.release()


def set_phone(user_id, phone):
    try:
        lock.acquire()
        cursor.execute('update USERS set PHONE = ? where ID = ?', (phone, str(user_id)))
        conn.commit()
    finally:
        lock.release()


def set_email(user_id, email):
    try:
        lock.acquire()
        cursor.execute('update USERS set EMAIL = ? where ID = ?', (email, str(user_id)))
        conn.commit()
    finally:
        lock.release()


def set_paysign(user_id, code):
    try:
        lock.acquire()
        cursor.execute('update USERS set PAY_SIGN = ? where ID = ?', (code, str(user_id)))
        conn.commit()
    finally:
        lock.release()


def set_balance(user_id, balance):
    try:
        lock.acquire()
        cursor.execute('update USERS set BALANCE = ? where ID = ?', (balance, str(user_id)))
        conn.commit()
    finally:
        lock.release()


def set_salary(user_id, salary):
    try:
        cursor.execute('update USERS set MONTH_SALARY = ? where ID = ?', (salary, str(user_id)))
        conn.commit()
    finally:
        lock.release()


def set_amount(user_id, amount):
    try:
        lock.acquire()
        cursor.execute('update USERS set AMOUNT = ? where ID = ?', (amount, str(user_id)))
        conn.commit()
    finally:
        lock.release()


def set_expire(user_id, exp):
    try:
        lock.acquire()
        cursor.execute('update USERS set EXPIRATION_TIME = ? where ID = ?', (exp, str(user_id)))
        conn.commit()
    finally:
        lock.release()


def trained(user_id):
    try:
        lock.acquire()
        cursor.execute('update USERS set IS_TRAINED = 1 where ID = ?', (str(user_id),))
        conn.commit()
    finally:
        lock.release()


def get_paysign(user_id):
    try:
        lock.acquire()
        cursor.execute('select PAY_SIGN from USERS where ID=?', (user_id,))
        return cursor.fetchone()[0]
    finally:
        lock.release()


def get_name_by_refcode(refcode):
    try:
        lock.acquire()
        cursor.execute('select NAME from USERS where REFERAL_CODE=?', (refcode,))
        return cursor.fetchone()[0]
    finally:
        lock.release()


def get_phone_by_refparent(refparent):
    try:
        lock.acquire()
        cursor.execute('select PHONE from USERS where REFERAL_PARENT=?', (str(refparent),))
        return cursor.fetchone()[0]
    finally:
        lock.release()


def get_registred_time(user_id):
    try:
        lock.acquire()
        cursor.execute('select REGISTRED_TIME from USERS where ID=?', (user_id,))
        return cursor.fetchone()[0]
    finally:
        lock.release()


def get_balance(user_id):
    try:
        lock.acquire()
        cursor.execute('select BALANCE from USERS where ID=?', (user_id,))
        return cursor.fetchone()[0]
    finally:
        lock.release()


def get_salary(user_id):
    try:
        lock.acquire()
        cursor.execute('select MONTH_SALARY from USERS where ID=?', (user_id,))
        return cursor.fetchone()[0]
    finally:
        lock.release()


def get_expiration_time(user_id):
    try:
        lock.acquire()
        cursor.execute('select EXPIRATION_TIME from USERS where ID=?', (user_id,))
        return cursor.fetchone()[0]
    finally:
        lock.release()


def get_refcode_by_id(user_id):
    try:
        lock.acquire()
        cursor.execute('select REFERAL_CODE from USERS where ID=?', (user_id,))
        return cursor.fetchone()[0]
    finally:
        lock.release()


def get_name_by_id(user_id):
    try:
        lock.acquire()
        cursor.execute('select NAME from USERS where ID=?', (user_id,))
        fetch = cursor.fetchone()
        if fetch is not None:
            return fetch[0]
        else:
            return None
    finally:
        lock.release()


def get_parent_by_id(user_id):
    try:
        lock.acquire()
        cursor.execute('select REFERAL_PARENT from USERS where ID=?', (user_id,))
        fetch = cursor.fetchone()
        if fetch is not None:
            return fetch[0]
        else:
            return None
    finally:
        lock.release()


def get_phone_by_id(user_id):
    try:
        lock.acquire()
        cursor.execute('select PHONE from USERS where ID=?', (user_id,))
        return cursor.fetchone()[0]
    finally:
        lock.release()


def get_parents_by_id(user_id):
    try:
        lock.acquire()
        cursor.execute('select REFERAL_PARENT, REFERAL_PARENT_2, REFERAL_PARENT_3 from USERS where ID=?', (user_id,))
        fetch = cursor.fetchone()
        if fetch is not None:
            return fetch
        else:
            return None
    finally:
        lock.release()


def get_lines_by_id(user_id):
    try:
        lock.acquire()
        cursor.execute('select ID from USERS where REFERAL_PARENT=? and EXPIRATION_TIME != -1', (user_id,))
        fetch = cursor.fetchone()
        if fetch is not None:
            line_1 = fetch
        else:
            return None, None, None
        cursor.execute('select ID from USERS where REFERAL_PARENT_2=? and EXPIRATION_TIME != -1', (user_id,))
        fetch = cursor.fetchone()
        if fetch is not None:
            line_2 = fetch
        else:
            return line_1, None, None
        cursor.execute('select ID from USERS where REFERAL_PARENT_3=? and EXPIRATION_TIME != -1', (user_id,))
        fetch = cursor.fetchone()
        if fetch is not None:
            line_3 = fetch
            return line_1, line_2, line_3
        else:
            return line_1, line_2, None
    finally:
        lock.release()


def get_line_1_by_id(user_id):
    try:
        lock.acquire()
        cursor.execute('select ID from USERS where REFERAL_PARENT=? and EXPIRATION_TIME != -1', (user_id,))
        fetch = cursor.fetchall()
        if fetch is not None:
            return fetch
        else:
            return None
    finally:
        lock.release()


def get_line_2_by_id(user_id):
        cursor.execute('select ID from USERS where REFERAL_PARENT_2=? and EXPIRATION_TIME != -1', (user_id,))
        fetch = cursor.fetchall()
        if fetch is not None:
            return fetch
        else:
            return None


def get_line_3_by_id(user_id):
    try:
        lock.acquire()
        cursor.execute('select ID from USERS where REFERAL_PARENT_3=? and EXPIRATION_TIME != -1', (user_id,))
        fetch = cursor.fetchall()
        if fetch is not None:
            return fetch
        else:
            return None
    finally:
        lock.release()


def select_subs():
    try:
        lock.acquire()
        cursor.execute('select ID from USERS where EXPIRATION_TIME > ? OR FREE_ACCESS=1', (time.time(),))
        fetch = cursor.fetchall()
        if fetch is not None:
            return fetch
        else:
            return None
    finally:
        lock.release()


def get_lines_len_by_id(user_id):
    try:
        lock.acquire()
        cursor.execute('select ID from USERS where REFERAL_PARENT=? and EXPIRATION_TIME != -1', (user_id,))
        fetch = cursor.fetchall()
        line_1_len = len(fetch)
        cursor.execute('select ID from USERS where REFERAL_PARENT_2=? and EXPIRATION_TIME != -1', (user_id,))
        fetch = cursor.fetchall()
        line_2_len = len(fetch)
        cursor.execute('select ID from USERS where REFERAL_PARENT_3=? and EXPIRATION_TIME != -1', (user_id,))
        fetch = cursor.fetchall()
        line_3_len = len(fetch)
        return line_1_len, line_2_len, line_3_len
    finally:
        lock.release()


def get_api_code_by_id(user_id):
    try:
        lock.acquire()
        cursor.execute('select PAY_WALLET from USERS where ID=?', (user_id,))
        wallet = cursor.fetchone()[0]
        # print(wallet)
        cursor.execute('select CODE from MONEY where WALLET=?', (wallet,))
        code = cursor.fetchone()[0]
        # print(code)
        return code
    finally:
        lock.release()


def new_month():
    try:
        lock.acquire()
        cursor.execute('update USERS set MONTH_SALARY = 0')
        conn.commit()
    finally:
        lock.release()


def update_links(xbet_link, xbet_mobile_link):
    try:
        lock.acquire()
        cursor.execute('update UTILS set XBET_LINK = ?, XBET_MOBILE_LINK = ?', (xbet_link, xbet_mobile_link))
        conn.commit()
    finally:
        lock.release()


def get_links():
    try:
        lock.acquire()
        cursor.execute('select XBET_LINK, XBET_MOBILE_LINK from UTILS')
        return cursor.fetchone()
    finally:
        lock.release()


def select_users():
    try:
        lock.acquire()
        cursor.execute('select ID from USERS')
        return cursor.fetchall()
    finally:
        lock.release()


def set_at_id(user_id, at_id):
    try:
        lock.acquire()
        cursor.execute('update USERS set AT_ID = ? where ID = ?', (str(at_id), user_id))
        conn.commit()
    finally:
        lock.release()


def get_at_id(user_id):
    try:
        lock.acquire()
        cursor.execute('select AT_ID from USERS where ID=?', (user_id,))
        return cursor.fetchone()[0]
    finally:
        lock.release()


def increment_line(line_n, user_id):
    try:
        lock.acquire()
        requests_1 = {
            0: 'select LINE_1 from USERS where ID=?',
            1: 'select LINE_2 from USERS where ID=?',
            2: 'select LINE_3 from USERS where ID=?'
        }
        requests_2 = {
            0: 'update USERS set LINE_1 = ? where ID = ?',
            1: 'update USERS set LINE_2 = ? where ID = ?',
            2: 'update USERS set LINE_3 = ? where ID = ?'
        }
        cursor.execute(requests_1[line_n], (user_id,))
        line_c = int(cursor.fetchone()[0]) + 1
        cursor.execute(requests_2[line_n], (line_c, user_id))
        conn.commit()
        return line_c
    finally:
        lock.release()


def get_email(user_id):
    try:
        lock.acquire()
        cursor.execute('select EMAIL from USERS where ID=?', (user_id,))
        return cursor.fetchone()[0]
    finally:
        lock.release()


def get_user_by_pay_sign(pay_sign):
    try:
        lock.acquire()
        cursor.execute('select ID from USERS where PAY_SIGN=?', (pay_sign,))
        fetch = cursor.fetchone()
        if fetch is not None:
            return fetch[0]
        else:
            return None
    finally:
        lock.release()


def is_first_pay(user_id):
    try:
        lock.acquire()
        cursor.execute('select EXPIRATION_TIME from USERS where ID=?', (user_id,))
        return cursor.fetchone()[0] == -1
    finally:
        lock.release()


def is_blocked(user_id):
    try:
        lock.acquire()
        cursor.execute('select BLOCKED from USERS where ID=?', (user_id,))
        return cursor.fetchone()[0] == 1
    finally:
        lock.release()


def is_have_free_access(user_id):
    try:
        lock.acquire()
        cursor.execute('select FREE_ACCESS from USERS where ID=?', (user_id,))
        return cursor.fetchone()[0] == 1
    finally:
        lock.release()


def invert_block(user_id):
    try:
        lock.acquire()
        cursor.execute('update users set BLOCKED=BLOCKED*-1 where ID=?', (user_id,))
        conn.commit()
    finally:
        lock.release()


def invert_access(user_id):
    try:
        lock.acquire()
        cursor.execute('update users set FREE_ACCESS=FREE_ACCESS*-1 where ID=?', (user_id,))
        conn.commit()
    finally:
        lock.release()


def update_msgs(xbet_link, xbet_mobile_link, video, faq, channels):
    try:
        lock.acquire()
        cursor.execute('update utils set XBET_LINK = ?, XBET_MOBILE_LINK = ?, VIDEO = ?, FAQ = ?, CHANNELS = ?',
                       (xbet_link, xbet_mobile_link, video, faq, channels))
        conn.commit()
    finally:
        lock.release()


def get_video():
    try:
        lock.acquire()
        cursor.execute('select VIDEO from UTILS')
        return cursor.fetchone()[0]
    finally:
        lock.release()


def get_faq():
    try:
        lock.acquire()
        cursor.execute('select FAQ from UTILS')
        return cursor.fetchone()[0]
    finally:
        lock.release()


def get_channels():
    try:
        lock.acquire()
        cursor.execute('select CHANNELS from UTILS')
        return cursor.fetchone()[0]
    finally:
        lock.release()


def file_in(at_id):
    try:
        lock.acquire()
        cursor.execute('select PLACE from FILES where AT_ID=?', (at_id,))
        return cursor.fetchone() is not None
    finally:
        lock.release()


def update_file(file_id, caption, place, at_id):
    try:
        lock.acquire()
        cursor.execute('update FILES set ID=?, CAPTION=?, PLACE=? where AT_ID=?', (file_id, caption, place, at_id))
        conn.commit()
    finally:
        lock.release()


def add_file(file_id, caption, place, at_id):
    try:
        lock.acquire()
        sql = 'insert into FILES (ID, CAPTION, PLACE, AT_ID) values(?, ?, ?, ?)'
        cursor.execute(sql, (str(file_id), str(caption), str(place), str(at_id)))
        conn.commit()
    finally:
        lock.release()


def get_franchise_files():
    cursor.execute("select ID, CAPTION from FILES where PLACE='Обучение по франшизе'")
    for file_id, caption in cursor.fetchall():
        yield (file_id, caption)


def get_signal_files():
    cursor.execute("select ID, CAPTION from FILES where PLACE='Обучение по сигналам'")
    for file_id, caption in cursor.fetchall():
        yield (file_id, caption)


def get_presentation_files():
    cursor.execute("select ID, CAPTION from FILES where PLACE='Презентация'")
    for file_id, caption in cursor.fetchall():
        yield (file_id, caption)


def get_termsofuse_files():
    cursor.execute("select ID, CAPTION from FILES where PLACE='Условия использования'")
    for file_id, caption in cursor.fetchall():
        yield (file_id, caption)
