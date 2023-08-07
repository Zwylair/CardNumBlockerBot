from datetime import datetime
import sqlite3
import asyncio
import logging
import settings
import log_handler

logger = logging.getLogger(__name__)
handler = log_handler.LogHandler()
formatter = logging.Formatter('[%(asctime)s | %(levelname)s | %(name)s]: %(message)s')

handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


async def review_restricted_members():
    while True:
        sql = sqlite3.connect(settings.SQL_DB_FL)

        req = sql.execute('select * from restricted').fetchall()
        for i in req:
            i: [int, int, str, str]
            member_id, chat_id, until_date, reason = i

            if datetime.now() >= datetime.fromtimestamp(float(until_date)):
                sql.execute(f"delete from restricted where member_id={member_id} and chat_id={chat_id}")
                sql.commit()

                logger.info(f'{member_id} was deleted from restricted list of {chat_id}')

        await asyncio.sleep(30)
