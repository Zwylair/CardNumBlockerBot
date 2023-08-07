import aiogram
from whitelist import whitelist_add, whitelist_remove


def set_bot_to_modules(bot: aiogram.Bot):
    whitelist_add.bot = bot
    whitelist_remove.bot = bot


def setup(dp: aiogram.Dispatcher, bot: aiogram.Bot):
    set_bot_to_modules(bot)

    dp.register_message_handler(whitelist_add.whitelist_add, commands=['whitelist_add'])
    dp.register_message_handler(whitelist_remove.whitelist_remove, commands=['whitelist_remove'])
