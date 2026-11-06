import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.handlers import router
from config import settings

logging.basicConfig(
    level=logging.INFO,
    filename="py_log.log",
    format=(
        "%(levelname)s (%(asctime)s): %(message)s"
        "(Line: %(lineno)d) [%(filename)s]"
    ),
    datefmt="%d/%m/%Y %H:%M:%S",
    encoding="utf-8",
    filemode="w",
    force=True,
)
logging.getLogger("aiogram").setLevel(logging.WARNING)


async def main() -> None:
    bot = Bot(settings.bot_token)
    dp = Dispatcher()

    dp.include_router(router)

    print("Бот запущен")
    logging.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
        logging.info("Бот выключен")
