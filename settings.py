import os
import string

TOKEN = os.getenv('block_card_num_moderator_bot_tg')
SQL_DB_FL = 'sql.db'
LOG_CHAT_ID = 880708503
OWNER_ID = 880708503
VALID_SYMBOLS = string.ascii_letters + string.digits + 'йцукенгшщзхъфывапролджэячсмитьбюёіїєґ' + '@'
BAN_WORDS = ['🇷🇺', 'хохол', 'усраин', 'славароссии']
MUTE_WORDS = ['мужчин', 'чоловік', 'мужик', 'военные', '🎫', 'збираємокошти', 'закордон', 'за кордон', 'covid', 'сертиф', 'ковид']
DELETE_WORDS = ['финанс', 'карт', 'фінанс']
