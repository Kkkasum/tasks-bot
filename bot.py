import asyncio

from src.common import bot, dp
from src.bot import include_routers


async def main():
    include_routers(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
