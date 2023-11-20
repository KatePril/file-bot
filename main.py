import asyncio
from aiogram import Bot, Dispatcher
from settings import settings
from handlers import handlers

bot = Bot(token=settings.BOT_TOKEN.get_secret_value())


async def main():
    dp = Dispatcher()

    dp.include_router(handlers.send_router)
    dp.include_router(handlers.text_router)
    dp.include_router(handlers.download_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
