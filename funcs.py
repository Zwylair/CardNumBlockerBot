import datetime

import aiogram.types

import settings


def get_str_date(date: datetime.datetime) -> str:
    return date.strftime('%d.%m.%Y, %H:%M:%S')


def get_str_msg(message_text: str) -> str:
    msg_text = message_text.lower()
    msg_text = msg_text.replace('\n', ' ').replace('380', '0')  # card nums cant start with 0 | it prevents from counting phone num as a card num
    msg_text = ''.join([i for i in list(msg_text) if i in settings.VALID_SYMBOLS])  # removing special symbols

    return msg_text


def get_str_user(user: aiogram.types.User) -> str:
    return f'[{user.mention}](tg://user?id={user.id}) (`{user.id}`)'
