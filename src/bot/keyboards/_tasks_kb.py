from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from ._menu_kb import MenuCallbackFactory


class TasksCallbackFactory(CallbackData, prefix='tasks'):
    page: str


class TaskCheckCallbackFactory(CallbackData, prefix='check'):
    task: str


class WalletCallbackFactory(CallbackData, prefix='wallet'):
    index: int


class WalletActionCallbackFactory(CallbackData, prefix='wallet_action'):
    action: str


def tasks_kb(completed_tasks: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if 'wallet' in completed_tasks:
        builder.button(text='✅ Кошелек', callback_data=TasksCallbackFactory(page='wallet'))
    else:
        builder.button(text='💰 Кошелек', callback_data=TasksCallbackFactory(page='wallet'))

    if 'channel' in completed_tasks:
        builder.button(text='✅ Подписаться на канал', callback_data=TasksCallbackFactory(page='channel'))
    else:
        builder.button(text='Подписаться на канал', callback_data=TasksCallbackFactory(page='channel'))

    if 'name' in completed_tasks:
        builder.button(text='✅ Поменять ник', callback_data=TasksCallbackFactory(page='name'))
    else:
        builder.button(text='👤 Поменять ник', callback_data=TasksCallbackFactory(page='name'))

    builder.button(text='👥 Пригласить друга', callback_data=TasksCallbackFactory(page='ref'))
    builder.button(text='☰ Главное меню', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(1)

    return builder.as_markup()


def wallets_kb(wallets: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    [
        builder.button(text=wallet, callback_data=WalletCallbackFactory(index=index))
        for index, wallet in enumerate(wallets)
    ]
    builder.button(text='☰ Задания', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(1)

    return builder.as_markup()


def wallet_try_again_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Попробовать подключить еще раз', callback_data=MenuCallbackFactory(page='wallet'))
    builder.button(text='☰ Задания', callback_data=MenuCallbackFactory(page='menu'))

    builder.adjust(1)

    return builder.as_markup()


def wallet_action_kb(completed_tasks: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if 'wallet' in completed_tasks:
        builder.button(text='Отключить кошелек', callback_data=WalletActionCallbackFactory(action='disconnect'))
    else:
        builder.button(text='Подключить кошелек', callback_data=WalletActionCallbackFactory(action='connect'))

    return builder.as_markup()


def wallet_connect_kb(url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Подключить кошелек', url=url)

    return builder.as_markup()


def task_invite_ref_kb(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Пригласить', switch_inline_query=f'{user_id}')

    return builder.as_markup()


def task_ref_kb(url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Перейти в бота', url=url)

    builder.adjust(1)

    return builder.as_markup()


def task_check_kb(task: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='✅ Выполнено', callback_data=TaskCheckCallbackFactory(task=task))
    builder.button(text='☰ Задания', callback_data=MenuCallbackFactory(page='tasks'))

    builder.adjust(1)

    return builder.as_markup()


def return_tasks_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='☰ Задания', callback_data=MenuCallbackFactory(page='tasks'))

    return builder.as_markup()
