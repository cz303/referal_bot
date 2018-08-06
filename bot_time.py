import time
import datetime

year = 31536000
month = 2592000
week = 604800
day = 86400
hour = 3600
current_month = 7


def parse_time(time_s):
    items = [
        (31536000, '{} г. '),
        (2592000, '{} мес. '),
        (604800, '{} нед. '),
        (86400, '{} д. '),
        (3600, '{} ч.'),
    ]

    if time_s == 0:
        return None

    if time_s < 3600:
        return 'меньше часа'

    result = ''

    for value, fmt in items:
        if time_s >= value:
            result += fmt.format(int(time_s / value))
            time_s %= value

    return result


def is_day_gone():
    global current
    if time.time() - current >= day:
        current = time.time()
        return True
    return False


def is_month_gone():
    global current
    if time.time() - current >= month:
        current = time.time()
        return True
    return False


def time_left(exp_time):
    if is_expired(exp_time):
        return 0
    return float(exp_time) - time.time()


def less_than_3_days_left(time_left):
    return float(time_left) <= day * 3


def is_expired(exp_time):
    return float(exp_time) < time.time()


def get_time():
    return time.time()


def get_exp_date(exp):
    if not is_expired(exp):
        return datetime.datetime.fromtimestamp(float(exp)).strftime('%d.%m.%Y %H:%M')
    else:
        return None


def get_reg_date(reg):
    return datetime.datetime.fromtimestamp(float(reg)).strftime('%d.%m.%Y %H:%M')


def get_cur_month():
    return datetime.datetime.now().month


def get_isoformat_date():
    return datetime.datetime.now().isoformat()
