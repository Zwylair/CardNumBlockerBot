import aiogram
import callback_handler.whitelist


async def cb_handler(callback: aiogram.types.CallbackQuery):
    funcs = [callback_handler.whitelist.whitelist_callback_handler]
    for func in funcs:
        await func(callback)


def setup(dp: aiogram.Dispatcher, bot: aiogram.Bot):
    callback_handler.whitelist.bot = bot

    dp.register_callback_query_handler(cb_handler)
