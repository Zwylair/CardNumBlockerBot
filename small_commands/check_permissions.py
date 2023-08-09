import aiogram

bot: aiogram.Bot


async def check_for_my_perms(message: aiogram.types.Message):
    if message.chat.type == 'private':
        await message.reply('Данная команда работает только в группе')
        return

    admins = await message.chat.get_administrators()
    admins_id = [i.user.id for i in admins]

    if message.from_user.id not in admins_id:
        await message.delete()
        return

    if bot.id not in admins_id:
        await message.reply('Бот не администратор. Назначьте бота администратором группы, выдав право блокировки участников и удаление сообщений')
        return

    me_admin = [i for i in admins if i.user.id == bot.id][0]

    can_restrict_perm_text = '✅' if me_admin.can_restrict_members else '❌'
    can_delete_messages_text = '✅' if me_admin.can_delete_messages else '❌'
    await message.reply('Бот администратор, требуемые права:\n\n'
                        f'Блокировка участников: {can_restrict_perm_text}\n'
                        f'Удаление сообщений: {can_delete_messages_text}')
