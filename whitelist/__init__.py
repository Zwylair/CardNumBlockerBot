import aiogram
import whitelist.whitelist as wh


def setup(dp: aiogram.Dispatcher, bot: aiogram.Bot):
    wh.bot = bot

    dp.register_message_handler(wh.whitelist_command, commands=['whitelist'])

    dp.register_message_handler(callback=wh.process_user_add, state=wh.AnswersForm.user_state_add)
    dp.register_message_handler(callback=wh.process_user_remove, state=wh.AnswersForm.user_state_remove)
    dp.register_message_handler(callback=wh.process_chat_add, state=wh.AnswersForm.chat_state_add)
    dp.register_message_handler(callback=wh.process_chat_remove, state=wh.AnswersForm.chat_state_remove)
