import asyncio
from aiogram import Bot, Dispatcher
from settings import settings
from handlers import text_handlers

bot = Bot(token=settings.BOT_TOKEN.get_secret_value())

async def main():
    dp = Dispatcher()

    dp.include_router(text_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())