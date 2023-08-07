from json import dump as save
from datetime import datetime
from datetime import timedelta
from typing import Union

import aiogram

from telebot_base.funcs.settings import SAVE_DIR


def get_args(message: str, args_type: list):
    input_args: Union[list] = message.split(' ')[1:]
    try:
        cnt = -1
        for arg_type in args_type:
            cnt += 1
            if arg_type == str:
                input_args[cnt] = str(input_args[cnt])
            elif arg_type == int:
                input_args[cnt] = int(input_args[cnt])
            elif arg_type == float:
                input_args[cnt] = float(input_args[cnt])
            elif arg_type == bool:
                if arg_type == 'True':
                    input_args[cnt] = True
                elif arg_type == 'False':
                    input_args[cnt] = False
    except:
        return None
    else:
        return input_args


def check_chat_items(settings: dict, settings_correct_keys: list):
    incorrect_keys = {}

    # add missing settings / save unnecessary settings
    for chat_id, chatSettings in settings.items():
        # chat_id: str = '-zzzzzzzzzzzzz'
        # chatSettings: dict = {'setting1': True, 'setting2': False}

        # Add the missing element if there is none
        for setting_correct in settings_correct_keys:
            # settings_correct: str = 'setting1'

            # if CORRECT setting name missing from chat settings list
            if setting_correct not in chatSettings.keys():
                settings[chat_id][setting_correct] = True

        # Remove unnecessary element if it exists
        for chat_setting in chatSettings.keys():
            # chat_setting: str = 'setting3'  # from chat, NOT correct settings list

            if chat_setting not in settings_correct_keys:
                if chat_id in incorrect_keys:
                    incorrect_keys[chat_id].append(chat_setting)
                else:
                    incorrect_keys[chat_id] = [chat_setting]

    # remove unnecessary settings
    for chat_id, incorrect_key_list in incorrect_keys.items():
        for key in incorrect_key_list:
            settings[chat_id].pop(key)
    
    save(settings, open(f'{SAVE_DIR}/telebot.settings.base', 'w'))


def check_exceptions(exceptions: dict):
    now = datetime.now()
    for user_id in list(exceptions):
        exception_time = exceptions[user_id]
        if now >= str2datetime(exception_time):
            exceptions.pop(user_id)
    
    save(exceptions, open(f'{SAVE_DIR}/telebot.whitelist.base', 'w'))


async def action(bot: aiogram.Bot, message: aiogram.types.Message, mode: int, log: dict, part: Union[str, None], type_of_exc: str):
    # log part
    user = message.from_user.first_name if str(message.from_user.username) == 'None' else f'@{message.from_user.username}'

    if log != {}:
        for chat_main, chat_log_list in log.items():
            if str(message.chat.id) in chat_log_list:
                await bot.forward_message(int(chat_main), message.chat.id, message.message_id)
                await bot.send_message(int(chat_main), f'({str(datetime.now())})'
                                                 f'   Sender: "{user}" ({message.from_user.id})\n'
                                                 f'   Trigger:\n'
                                                 f'      Type: "{type_of_exc}"\n'
                                                 f'      Part: "{part}"\n'
                                                 f'   Chat:\n'
                                                 f'      ID: "{message.chat.id}"\n'
                                                 f'      Name: "{message.chat.title}"')
    
    await bot.delete_message(message.chat.id, message.message_id)
    
    if mode in [1, 2]:
        if mode == 1:
            await  bot.restrict_chat_member(message.chat.id, message.from_user.id, aiogram.types.ChatPermissions(), until_date=datetime.now() + timedelta(days=1))
            
            date_now = str(datetime.now() + timedelta(days=1)).split(' ')[0].split('-')
            date_now = f'{date_now[2]}/{date_now[1]}/{date_now[0]}'
            time_now = f' {str(datetime.now()).split(" ")[1][:-10]}'
            do = 'заткнул'
        else:
            await bot.ban_chat_member(message.chat.id, message.from_user.id)
            
            date_now = 'истечения 9e+21 лет'
            time_now = ''
            do = 'забанил'
        
        await bot.send_message(message.chat.id,
                         f'[{user}](tg://user?id={message.from_user.id}) (`{message.from_user.id}`) отправляет спам\n'
                         f'*Что я сделал?:* {do} до {date_now}{time_now}.',
                         parse_mode='markdown')


def str2datetime(text: str):
    date = text.split(' ')[0]
    time = text.split(' ')[1]
    
    y, m, d = [int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2])]
    h, mi, s, ms = [int(time.split(':')[0]), int(time.split(':')[1]), int(time.split(':')[2].split('.')[0]),
                    int(time.split('.')[1])]
    
    return datetime(y, m, d, h, mi, s, ms)


def str2timedelta(message: str):
    time_ = message
    for i in list('smhdw'):
        time_ = time_.replace(i, '')
    
    if time_.isdigit():
        if message[-1] == 's':
            return timedelta(seconds=int(message.replace('s', '')))
        elif message[-1] == 'm':
            return timedelta(minutes=int(message.replace('m', '')))
        elif message[-1] == 'h':
            return timedelta(hours=int(message.replace('h', '')))
        elif message[-1] == 'd':
            return timedelta(days=int(message.replace('d', '')))
        elif message[-1] == 'w':
            return timedelta(weeks=int(message.replace('w', '')))
    else:
        return None


def start_check(settings: dict, settings_correct_keys: list, exceptions: dict):
    check_chat_items(settings, settings_correct_keys)
    check_exceptions(exceptions)
