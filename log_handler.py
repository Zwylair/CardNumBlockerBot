import asyncio
import logging
import aiogram
import settings


class LogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.bot = aiogram.Bot(settings.TOKEN)

    def emit(self, record):
        log_entry = self.format(record)
        asyncio.create_task(self.send_message_to_log_chat(log_entry))

    async def send_message_to_log_chat(self, log_record: str):
        await self.bot.send_message(settings.LOG_CHAT_ID, log_record, parse_mode='markdown')
