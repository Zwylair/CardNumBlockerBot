import aiogram
import message_handler.group_restrict
# import message_handler.other_module


funcs = [group_restrict.group_restrict]  # other_module.___


async def msg_handler(message: aiogram.types.Message):
    for func in funcs:
        await func(message)


def setup(dp: aiogram.Dispatcher, bot_arg: aiogram.Bot):
    group_restrict.bot = bot_arg
    # other_module.bot = bot_arg

    dp.register_message_handler(msg_handler, content_types=['text'])
