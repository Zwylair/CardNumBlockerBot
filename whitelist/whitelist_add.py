import sqlite3
import aiogram
import settings

bot: aiogram.Bot


async def whitelist_add(message: aiogram.types.Message):
    if message.chat.type != 'private':
        return

    if message.from_user.id != settings.OWNER_ID:
        await bot.send_message(message.chat.id, 'You dont have permission to do that!')
        return

    try:
        whitelist_user_id = int(message.text.split(' ')[1])
        whitelist_chat_id = int(message.text.split(' ')[1])
    except ValueError:
        await bot.send_message(message.chat.id, 'Cant convert letters to int')
        return

    sql = sqlite3.connect(settings.SQL_DB_FL)

    member_in_db = sql.execute(f'select * from whitelist where member_id={whitelist_user_id}').fetchall()
    for i in member_in_db:
        i: [int, int]
        db_member_id, db_chat_id = i

        if whitelist_chat_id == db_chat_id:
            await bot.send_message(message.chat.id, 'This member already in whitelist of this group')
            return

    sql.execute(f'insert into "whitelist" (member_id, chat_id) values ({whitelist_user_id}, {whitelist_chat_id})')
    sql.commit()

    await bot.send_message(message.chat.id, 'The operation ended successfully')
