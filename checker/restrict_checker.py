from datetime import datetime, timedelta
import logging
import aiogram
import settings
import log_handler
import funcs

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s | %(levelname)s | %(name)s]: %(message)s')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler.LogHandler())


async def check_for_ban_words(message: aiogram.types.Message, bot: aiogram.Bot):
    msg_text = funcs.get_str_msg(message.text)

    for ban_word in settings.BAN_WORDS:
        if ban_word in msg_text:
            try:
                await bot.ban_chat_member(message.chat.id, message.from_user.id)  # maybe revoke_messages=True ??
                await message.delete()
                await bot.send_message(message.chat.id, f'{funcs.get_str_user(message.from_user)} был забанен из-за бан-ворда', parse_mode='markdown')

                logger.info(f'{funcs.get_str_user(message.from_user)} was banned using ban-word')
            except aiogram.exceptions.CantRestrictChatOwner:
                await bot.send_message(message.chat.id, "Я не могу банить овнера!")
                logger.info(f"{funcs.get_str_user(message.from_user)} cannot be banned (chat owner)")
            except aiogram.exceptions.UserIsAnAdministratorOfTheChat:
                await bot.send_message(message.chat.id, "Я не могу мьютить администратора!")
                logger.info(f"{funcs.get_str_user(message.from_user)} cannot be banned (chat admin)")
            return True  # return True to stop checking the message
    else:
        return False  # return False to continue checking the message


async def check_for_chat_mention(message: aiogram.types.Message, bot: aiogram.Bot) -> bool:
    if '@' not in message.text:
        return False  # return False to continue checking the message

    msg_text = message.text.lower().replace('\n', ' ')

    for word in msg_text.split(' '):
        if word.startswith('@'):
            try:
                await bot.get_chat(word)

                until_date = datetime.now() + timedelta(days=1)

                await bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=until_date)
                await message.delete()
                await bot.send_message(message.chat.id, f'{funcs.get_str_user(message.from_user)} был замьючен до {funcs.get_str_date(until_date)} из-за ссылки на чат', parse_mode='markdown')

                logger.info(f'{funcs.get_str_user(message.from_user)} was muted until {funcs.get_str_date(until_date)} using chat mention')
                return True  # return True to stop checking the message
            except aiogram.exceptions.CantRestrictChatOwner:
                await bot.send_message(message.chat.id, "Я не могу мьютить владельца!")
                logger.info(f"{funcs.get_str_user(message.from_user)} cannot be restricted (chat owner)")
                return True  # return True to stop checking the message
            except aiogram.exceptions.UserIsAnAdministratorOfTheChat:
                await bot.send_message(message.chat.id, "Я не могу мьютить администраторов!")
                logger.info(f"{funcs.get_str_user(message.from_user)} cannot be restricted (chat admin)")
                return True  # return True to stop checking the message
            except aiogram.exceptions.ChatNotFound:
                pass
    else:
        return False  # return False to continue checking the message


async def check_for_mute_words(message: aiogram.types.Message, bot: aiogram.Bot) -> bool:
    msg_text = funcs.get_str_msg(message.text)

    for mute_word in settings.MUTE_WORDS:
        if mute_word in msg_text:
            try:
                until_date = datetime.now() + timedelta(days=1)

                await bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=until_date)
                await message.delete()
                await bot.send_message(message.chat.id, f'{funcs.get_str_user(message.from_user)} был замьючен до {funcs.get_str_date(until_date)} из-за мут-слова', parse_mode='markdown')

                logger.info(f'{funcs.get_str_user(message.from_user)} was muted using mute-word')
            except aiogram.exceptions.CantRestrictChatOwner:
                await bot.send_message(message.chat.id, "Я не могу мьютить владельца!")
                logger.info(f"{funcs.get_str_user(message.from_user)} cannot be restricted (chat owner)")
            except aiogram.exceptions.UserIsAnAdministratorOfTheChat:
                await bot.send_message(message.chat.id, "Я не могу мьютить администраторов!")
                logger.info(f"{funcs.get_str_user(message.from_user)} cannot be restricted (chat admin)")
            return True  # return True to stop checking the message
    else:
        return False  # return False to continue checking the message


async def card_num_check(message: aiogram.types.Message, bot: aiogram.Bot):
    msg_text = funcs.get_str_msg(message.text)
    user = message.from_user

    offset = 0
    for i in range(len(msg_text) - 15):
        offset_text = msg_text[offset:16 + offset]  # len is always 16 ## (1234-5678-1234-5678 = 16 digits)
        offset += 1

        if offset_text.isdigit():
            if not offset_text.startswith('0'):
                try:
                    until_date = datetime.now() + timedelta(days=1)

                    await message.chat.restrict(user.id, until_date=until_date)
                    await bot.send_message(message.chat.id, f'{funcs.get_str_user(message.from_user)} был замьючен до {funcs.get_str_date(until_date)} из-за номера карты', parse_mode='markdown')
                    await message.delete()

                    logger.info(f'{funcs.get_str_user(message.from_user)} was muted (card number) until {funcs.get_str_date(until_date)}')
                except aiogram.exceptions.MethodIsNotAvailable:
                    await bot.send_message(message.chat.id, "Я не могу мьютить не в супергруппе!")
                    logger.info(f"{funcs.get_str_user(message.from_user)} cannot be restricted (chat isn't a supergroup)")
                except aiogram.exceptions.CantRestrictChatOwner:
                    await bot.send_message(message.chat.id, "Я не могу мьютить владельца!")
                    logger.info(f"{funcs.get_str_user(message.from_user)} cannot be restricted (chat owner)")
                return True  # return True to stop checking the message
    else:
        return False  # return False to continue checking the message


async def check_for_delete_words(message: aiogram.types.Message) -> bool:
    msg_text = funcs.get_str_msg(message.text)

    for delete_word in settings.DELETE_WORDS:
        if delete_word in msg_text:
            await message.delete()

            logger.info(f"{funcs.get_str_user(message.from_user)}'s message was deleted")
            return True  # return True to stop checking the message
    else:
        return False  # return False to continue checking the message
