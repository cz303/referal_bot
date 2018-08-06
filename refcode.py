from random import choice
from string import ascii_letters as letters, digits
from config import bot_url


def has_refcode(text):
    return len(text.split()) > 1


def extract_refcode(text):
    return text.split()[1]


def generate_code():
    return ''.join(choice(letters + digits) for _ in range(16))


def generate_reflink(refcode):
    return 'https://t.me/{}?start={}'.format(bot_url, refcode)
