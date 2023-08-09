import aiogram
import on_new_member.member_is_me
# import on_new_member.other_module


funcs = [member_is_me.on_new_members]  # other_module.on_new_members


async def on_new_members(message: aiogram.types.Message):
    for func in funcs:
        await func(message)


def setup(dp: aiogram.Dispatcher, bot_arg: aiogram.Bot):
    on_new_member.member_is_me.bot = bot_arg
    # other_module.bot = bot_arg

    dp.register_message_handler(on_new_members, content_types=aiogram.types.ContentType.NEW_CHAT_MEMBERS)
