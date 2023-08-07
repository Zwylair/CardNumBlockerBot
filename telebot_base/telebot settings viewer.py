from json import load

while 1:
    inpt = None
    while inpt not in ['users', 'chats', 'logs']:
        inpt = input('\nSelect base (users/chats/logs): ')
    
    if inpt == 'chats':
        chats_base = load(open('telebot.settings.base'))
        # chats_base: dict

        for chat_id, settings in chats_base.items():
            print(f'{chat_id}:')
            for setting, state in settings.items():
                print(f'   {setting}: {state}')

    elif inpt == 'users':
        users_base = load(open('telebot.users.base'))
        # users_base: dict
    
        for username, flags in users_base.items():
            # username: str
            # admin_on: list

            print(f'{username}:')
            for chat_id in flags['admin_on']:
                print(f'   {chat_id}')

    elif inpt == 'logs':
        logs_base = load(open('telebot.log.base'))
        # logs_base: dict = {'-zzzzzzzzzzzzz': [-zzzzzzzzzzzzz, -zzzzzzzzzzzzz...]}
        for main_chat, secondary_chat_list in logs_base.items():
            print(f'{main_chat}:')
            for i in secondary_chat_list:
                print(f'   {i}')
