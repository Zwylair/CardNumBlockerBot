import asyncio
import logging

import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import log_handler

import whitelist
import small_commands
import on_new_member
import message_handler
import callback_handler

import settings

#

bot = aiogram.Bot(settings.TOKEN)
storage = MemoryStorage()
dp = aiogram.Dispatcher(bot, storage=storage)

logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(asctime)s | %(levelname)s | %(name)s]: %(message)s')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler.LogHandler())


# @dp.message_handler(commands=['test'])
# async def test(message: aiogram.types.Message):
#     ...


@dp.message_handler(commands=['start'])
async def start(message: aiogram.types.Message):
    my_username = await bot.get_me()
    my_username = my_username.username

    markup = aiogram.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        aiogram.types.InlineKeyboardButton('Добавить меня в группу ➕', url=f'https://t.me/{my_username}?startgroup=start'),
    )

    if message.chat.type == 'private':
        text = 'Привет! Я бот для блокировки *номеров карт*, пингов чата и прочего 🚫\n' \
               'Ты можешь добавить меня *в чат* по кнопке ниже, не забудь выдать право *блокировки пользователей* и *удаления сообщений* 👥\n\n'
        reply = await message.reply(text, parse_mode='markdown', reply_markup=markup)
    else:
        admins = await message.chat.get_administrators()
        admins_id = [i.user.id for i in admins]
        if message.from_user.id not in admins_id:
            return

        text = '*ВНИМАНИЕ: Эта команда доступна только для администраторов*\n\n' \
               '*ВНИМАНИЕ 2: В группе отключены все команды кроме этой и /check_permissions. Это сообщение будет автоудалено через 15 секунд*'
        reply = await message.reply(text, parse_mode='markdown')

    if message.chat.type != 'private':
        await asyncio.sleep(15)
        await reply.delete()


@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return  # User is not in any state, ignoring

    # Cancel state and inform user about it
    await state.finish()
    await message.reply('Отменено 🔙')


async def main():
    # asyncio.create_task(checker.review_restricted_members())

    # commands always at the top
    whitelist.setup(dp, bot)
    small_commands.setup(dp, bot)
    # not message handlers at the middle
    on_new_member.setup(dp, bot)
    callback_handler.setup(dp, bot)
    # message handler always at bottom
    message_handler.setup(dp, bot)

    await dp.skip_updates()
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
