import sqlite3

import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import funcs
import settings

bot: aiogram.Bot

whitelist_menu_markup = aiogram.types.InlineKeyboardMarkup(row_width=2)
whitelist_menu_markup.add(
    aiogram.types.InlineKeyboardButton('Добавить в БС ➕', callback_data='wl_add'),
    aiogram.types.InlineKeyboardButton('Удалить из БС 🗑️', callback_data='wl_remove')
)


class AnswersForm(StatesGroup):
    user_state_add = State()
    chat_state_add = State()
    user_state_remove = State()
    chat_state_remove = State()
    user_obj: aiogram.types.User | None = None


async def process_user_add(message: aiogram.types.Message, state: FSMContext):
    if message.forward_from is None and not message.text.isdigit():
        await message.reply('Это невалидное пересланное сообщение / айди пользователя ❌')
        return

    if message.text.isdigit():
        try:
            user = await funcs.get_user_from_id(bot, message.text)
        except aiogram.exceptions.ChatNotFound:
            await message.reply('Это невалидное айди пользователя ❌')
            return
    else:
        user = message.forward_from

    if user.is_bot:
        await message.reply('Этот пользователь - бот 🤖\n'
                            'Невозможно добавить бота в белый список ❌')
        return  # the author of the forwarded message is a bot, and messages from bots are not counted in the checks

    await state.finish()
    await AnswersForm.chat_state_add.set()
    await message.reply(f'Отлично, теперь отправь мне айди чата (-111222333444...) либо его отметку (@chat) 📨\n\n'
                        ''
                        'Для отмены /cancel')

    AnswersForm.user_obj = user


async def process_user_remove(message: aiogram.types.Message, state: FSMContext):
    if message.forward_from is None and not message.text.isdigit():
        await message.reply('Это невалидное пересланное сообщение / айди пользователя ❌')
        return

    if message.text.isdigit():
        try:
            user = await funcs.get_user_from_id(bot, message.text)
        except aiogram.exceptions.ChatNotFound:
            await message.reply('Это невалидное айди пользователя ❌')
            return
    else:
        user = message.forward_from

    if user.is_bot:
        await message.reply('Этот пользователь - бот 🤖\n'
                            'Невозможно добавить бота в белый список ❌')
        return  # the author of the forwarded message is a bot, and messages from bots are not counted in the checks

    await state.finish()
    await AnswersForm.chat_state_remove.set()
    await message.reply(f'Отлично, теперь отправь мне айди чата (-111222333444...) либо его отметку (@chat) 📨\n\n'
                        ''
                        'Для отмены /cancel')


async def process_chat_add(message: aiogram.types.Message, state: FSMContext):
    try:
        chat = await bot.get_chat(message.text)
    except aiogram.exceptions.ChatNotFound:
        try:
            chat = await bot.get_chat(f'@{message.text.split("/")[-1]}')
        except aiogram.exceptions.ChatNotFound:
            await message.reply('Это невалидный чат ❌')
            return

    await state.finish()
    user = AnswersForm.user_obj
    AnswersForm.user_obj = None

    sql = sqlite3.connect(settings.SQL_DB_FL)
    req = sql.execute(f'SELECT * FROM whitelist WHERE member_id={user.id} AND chat_id={chat.id}').fetchone()

    if req is not None:
        await message.reply('Данный пользователь уже добавлен в белый список в этот чат! ✋')
        return

    sql.execute(f'INSERT INTO whitelist (member_id, chat_id) VALUES ({user.id}, {chat.id})')
    sql.commit()

    await message.reply(f'Отлично! {funcs.get_str_user(user)} из чата {funcs.get_str_chat(chat)} был добавлен в белый список ✅', parse_mode='markdown')
    return


async def process_chat_remove(message: aiogram.types.Message, state: FSMContext):
    try:
        chat = await bot.get_chat(message.text)
    except aiogram.exceptions.ChatNotFound:
        try:
            chat = await bot.get_chat(f'@{message.text.split("/")[-1]}')
        except aiogram.exceptions.ChatNotFound:
            await message.reply('Это невалидный чат ❌')
            return

    await state.finish()
    user = AnswersForm.user_obj
    AnswersForm.user_obj = None

    sql = sqlite3.connect(settings.SQL_DB_FL)
    req = sql.execute(f'SELECT * FROM whitelist WHERE member_id={user.id} AND chat_id={chat.id}').fetchone()

    if req is not None:
        await message.reply('Данный пользователь уже добавлен в белый список в этот чат! ✋')
        return

    sql.execute(f'DELETE FROM whitelist WHERE member_id={user.id} AND chat_id={chat.id}')
    sql.commit()

    await message.reply(f'Отлично! {funcs.get_str_user(user)} из чата {funcs.get_str_chat(chat)} был убран из белого списка ✅', parse_mode='markdown')
    return


async def whitelist_command(message: aiogram.types.Message):
    if message.chat.type != 'private':
        return

    await message.reply('При добавлении пользователя в белый список он становится невосприимчив к любым проверкам (проверки на бан-ворды, номера карт и прочее) ✳️',
                        reply_markup=whitelist_menu_markup)
