import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.config import load_config, Config
from handlers import user_handlers
from database.models import async_main


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def main():

    await async_main()

    logger.info("Start Bot")
    config: Config = load_config()

    bot = Bot(config.tg_bot.token)
    dp = Dispatcher()

    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stop Bot")
