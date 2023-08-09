import asyncio
import sqlite3
import aiogram
import checker
import settings

bot: aiogram.Bot


async def group_restrict(message: aiogram.types.Message):
    if message.from_user.is_bot:
        return

    # if chat is between bot and user (private)
    if message.chat.type == 'private':
        return

    if not await checker.check_for_my_perms(message, bot):
        msg = await message.reply('Недостаточно прав для модерации группы! Выдайте боту права ограничивать участников, удалять сообщения (автоудаление через 15 секунд)')

        await asyncio.sleep(15)
        await msg.delete()

        return

    # whitelist system
    sql = sqlite3.connect(settings.SQL_DB_FL)
    whitelist_db = sql.execute('select * from whitelist').fetchall()
    for i in whitelist_db:
        i: [int, int]
        user_id, chat_id = i

        if message.chat.id == chat_id and message.from_user.id == user_id:
            return

    # there are restrict funcs below. their order - priority in execution
    await checker.check_for_ban_words(message, bot)
    await checker.check_for_chat_mention(message, bot)
    await checker.check_for_mute_words(message, bot)
    await checker.card_num_check(message, bot)
    await checker.check_for_delete_words(message)
