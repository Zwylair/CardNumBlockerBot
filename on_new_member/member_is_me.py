import aiogram

bot: aiogram.Bot


async def on_new_members(message: aiogram.types.Message):
    perm_granted = '✅'
    perm_not_provided = '❌'

    bot_user = await bot.me
    message.new_chat_members.append(bot_user)
    for user in message.new_chat_members:
        message.new_chat_members.remove(bot_user)
        if user.id != bot.id:
            return

        init_message = await message.reply('Инициализация')

        admins = await message.chat.get_administrators()
        admins_id = [i.user.id for i in admins]

        if bot.id not in admins_id:
            await init_message.edit_text('Бот не администратор в этой группе! Поставьте бота администратором для его корректной работы!')
            return

        me_admin = [i for i in admins if i.user.id == bot.id][0]

        if not me_admin.can_restrict_members or not me_admin.can_delete_messages:
            visualize_delete_messages_perm = perm_granted if me_admin.can_delete_messages else perm_not_provided
            visualize_restrict_perm = perm_granted if me_admin.can_restrict_members else perm_not_provided

            await init_message.edit_text('Бот администратор, но не предоставлены требуемые права:\n\n'
                                         f'\tУдаление сообщений: {visualize_delete_messages_perm}\n'
                                         f'\tБлокировка участников: {visualize_restrict_perm}\n\n'
                                         ''
                                         'Выдайте требуемые права боту для корректной его работы!')
            return

        await init_message.edit_text('Бот успешно инициализирован, требуемые права присутствуют. Для проверки можете использовать следующий текст: `5555-5555-5555-5555` (тыкните для копирования)', parse_mode='markdown')
