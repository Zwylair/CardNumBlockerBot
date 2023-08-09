import aiogram
import small_commands.check_permissions


def setup(dp: aiogram.Dispatcher, bot: aiogram.Bot):
    small_commands.check_permissions.bot = bot

    dp.register_message_handler(small_commands.check_permissions.check_for_my_perms, commands=['check_permissions'])
