import aiogram

bot: aiogram.Bot


async def on_new_members(message: aiogram.types.Message):
    for user in message.new_chat_members:
        if user.id != bot.id:  # Проверяем, что новый участник - это бот
            await message.reply("Привет! hjkljhklhjklЯ бот, рад познhlklhjакомиться с вами!")  # Отправляем приветственное сообщение
