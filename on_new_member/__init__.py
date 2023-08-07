import aiogram
import on_new_member.member_is_me
import on_new_member.sdfkilug


def set_bot_to_modules(bot: aiogram.Bot):
    member_is_me.bot = bot
    sdfkilug.bot = bot


def setup(dp: aiogram.Dispatcher, bot: aiogram.Bot):
    set_bot_to_modules(bot)

    dp.register_message_handler(member_is_me.on_new_members, content_types=aiogram.types.ContentType.NEW_CHAT_MEMBERS)
    dp.register_message_handler(sdfkilug.on_new_members, content_types=aiogram.types.ContentType.NEW_CHAT_MEMBERS)
