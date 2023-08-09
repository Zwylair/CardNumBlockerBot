import aiogram
import settings
import whitelist.whitelist

bot: aiogram.Bot


async def whitelist_callback_handler(callback: aiogram.types.CallbackQuery):
    message = callback.message
    user = callback.message.chat

    match callback.data:
        case 'wl_add':
            if message.chat.type != 'private':
                return

            if user.id != settings.OWNER_ID:
                await bot.send_message(message.chat.id, 'У тебя нет прав для совершения этого действия!')
                return

            # Set state
            await whitelist.whitelist.AnswersForm.user_state_add.set()
            await message.reply('Отправьте мне айди пользователя, или перешлите его сообщение (для отмены /cancel)')
        case 'wl_remove':
            if message.chat.type != 'private':
                return

            if user.id != settings.OWNER_ID:
                await bot.send_message(message.chat.id, 'У тебя нет прав для совершения этого действия!')
                return

            # Set state
            await whitelist.whitelist.AnswersForm.user_state_remove.set()
            await message.reply('Отправьте айди или перешлите сообщение пользователя, которого вы хотите удалить из белого списка')
