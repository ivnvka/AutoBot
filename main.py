import asyncio
import logging
import sys
from config import BOT_TOKEN, ALLOWED_CHAT_ID, ARCHIVE_CHAT_ID

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# Bot token can be obtained via https://t.me/BotFather
TOKEN = BOT_TOKEN

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\nЯ автобот, слежу за повреждениями корпоративного транспорта.")


@dp.message()
async def reply_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the archive

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    if message.chat.id == ALLOWED_CHAT_ID:
        try:
            # Send a copy of the received message
            await message.forward(ARCHIVE_CHAT_ID)
        except TypeError:
            # But not all the types is supported to be copied so need to handle it
            await Bot.send_message(Bot, ARCHIVE_CHAT_ID, "Попытка отправить сообщение не поддерживающегося типа")
    else:
        if message.chat.id == ARCHIVE_CHAT_ID:
            return
        await message.answer("Был бы рад с тобой пообщаться, но слежу только за сообщениями в чате приема корпоративного транспорта и совсем нет времени на беседы 🙃")

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())