import datetime
import json

import aiogram

from telebot_base.funcs.funcs import *
from telebot_base.funcs.settings import *

# load settings
users: dict = json.load(open(f'{SAVE_DIR}/telebot.users.base'))
settings: dict = json.load(open(f'{SAVE_DIR}/telebot.settings.base'))
log: dict = json.load(open(f'{SAVE_DIR}/telebot.log.base'))

bot = aiogram.Bot(TOKEN)
dp = aiogram.Dispatcher(bot)

start_check(settings, CHATS_CORRECT_KEYS, json.load(open(f'{SAVE_DIR}/telebot.whitelist.base')))


async def get_chat_admins(chat: aiogram.types.Chat) -> list:
    return [i.user.username for i in await bot.get_chat_administrators(chat.id)] if chat.type != 'private' else []


@dp.message_handler(commands=['chat_settings'])
async def chat_settings(message: aiogram.types.Message):
    load_message = await bot.send_message(message.chat.id, 'Секунду...')
    chat_admins = await get_chat_admins(message.chat)

    if message.from_user.username in chat_admins or message.chat.type == 'private':
        # set vars & check for args
        try:
            group, setting, state = get_args(message.text, [int, str, str])
            group = users[message.from_user.username]['admin_on'][group - 1]

            # check that the arguments are filled in correctly; if incorrect, issue an error
            if setting not in CHATS_CORRECT_KEYS or state not in ['on', 'off']:
                raise Exception
        except BaseException:
            if str(message.from_user.id) in users.keys():
                chats_settings = ''
                count = 0

                for i in users[str(message.from_user.id)]['admin_on']:
                    count += 1
                    chat = await bot.get_chat(i)
                    chats_settings += f'"{chat.title}" (№{count}):\n'
                    if str(i) in settings.keys():
                        for b in settings[str(i)].keys():
                            text = 'on' if settings[str(i)][b] else 'off'
                            chats_settings += f'   {b}: {text}\n'

                bot.edit_message_text(f'-=-=-=-=[Настройки]=-=-=-=-\n\n'
                                      f'{chats_settings}'
                                      f'\n-=-=-=-=[Помощь]=-=-=-=-=\n\n'
                                      f'\n-=-=-=-=[Пример]=-=-=-=-=\n\n'
                                      f'(Пример: "/chat_settings 1 block_card_num on" - это включит блок карт в первом чате',
                                      message.chat.id, load_message.message_id)
            else:
                bot.edit_message_text('Ты не добавил групп', message.chat.id, load_message.message_id)
        else:
            if str(message.from_user.id) in users.keys():
                state, state_text = [True, 'включена'] if state == 'on' else [False, 'выключена']

                if str(group) not in settings.keys():
                    settings[str(group)] = {}
                settings[str(group)][str(setting)] = state

                save(settings, open(f'{SAVE_DIR}/telebot.settings.base', 'w'))
                chat = await bot.get_chat(group)
                bot.edit_message_text(f'Настройка {setting} в чате "{chat.title}" успешно {state_text}!',
                                      message.chat.id, load_message.message_id)
            else:
                bot.edit_message_text('Ты не добавил групп', message.chat.id, load_message.message_id)


print('Started')

bot.skip_pending = True
aiogram.executor.start_polling(dp)
