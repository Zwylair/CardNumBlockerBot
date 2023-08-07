import asyncio
import sqlite3
import logging
import aiogram
import settings
import checker
import log_handler
import whitelist
import on_new_member

bot = aiogram.Bot(settings.TOKEN)
dp = aiogram.Dispatcher(bot)

logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(asctime)s | %(levelname)s | %(name)s]: %(message)s')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler.LogHandler())


@dp.message_handler(commands=['test'])
async def test(message: aiogram.types.Message):
    sql = sqlite3.connect(settings.SQL_DB_FL)
    sql.execute('insert into restricted (member_id, chat_id, until_date_timestamp, reason) values (1, 1, "3289472", "yes")')
    sql.commit()

    await bot.send_message(message.chat.id, 'YES')


async def message_handler(message: aiogram.types.Message):
    # if chat is between bot and user (private)
    if message.chat.type == 'private':
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


async def main():
    asyncio.create_task(checker.review_restricted_members())

    whitelist.setup(dp, bot)
    on_new_member.setup(dp, bot)

    dp.register_message_handler(message_handler, content_types=['text'])
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
