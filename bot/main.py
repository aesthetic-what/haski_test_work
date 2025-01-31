from aiogram import Dispatcher, Bot
from bot.handlers import router
from dotenv import load_dotenv
from data.database import Base, engine
import asyncio

import os


load_dotenv('.env')
config = os.environ

TOKEN = config['TELEGRAM_TOKEN']

async def main():
    Base.metadata.create_all(bind=engine)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:

        print('bot started')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('bot deactivated')