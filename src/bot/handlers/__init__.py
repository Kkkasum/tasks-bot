from aiogram import Dispatcher

from ._menu import router as menu_router
from ._tasks import router as tasks_router


def include_routers(dp: Dispatcher):
    dp.include_routers(
        menu_router,
        tasks_router,
    )
