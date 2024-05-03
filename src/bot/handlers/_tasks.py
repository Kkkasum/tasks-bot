import asyncio
import qrcode

from aiogram import Router, F, types
from aiogram.utils.deep_linking import create_start_link

from pytonconnect.exceptions import FetchWalletsError
from pytoniq_core import Address, AddressError

from src.common import bot, CHAT, NAME, WALLET_REWARD, CHANNEL_REWARD, NAME_REWARD, REF_REWARD
from src.services.user import user_service
from src.services.ton import Connector
from src.utils.formatters import format_tasks, format_ref, format_increase
from src.utils import messages as msg
from src.bot.keyboards import (
    MenuCallbackFactory,
    TasksCallbackFactory,
    WalletCallbackFactory,
    TaskCheckCallbackFactory,
    WalletActionCallbackFactory,
    tasks_kb,
    return_tasks_kb,
    task_check_kb,
    wallets_kb,
    wallet_try_again_kb,
    wallet_connect_kb,
    task_ref_kb,
    task_invite_ref_kb, wallet_action_kb
)


router = Router()


@router.callback_query(MenuCallbackFactory.filter(F.page == 'tasks'))
async def tasks_callback(callback: types.CallbackQuery, **_):
    ref, balance, wallet = await user_service.get_user(user_id=callback.from_user.id)

    completed_tasks = await user_service.get_completed_tasks(user_id=callback.from_user.id)

    m = format_tasks(user_id=callback.from_user.id, balance=balance + ref * REF_REWARD, ref=ref, wallet=wallet)

    await callback.message.delete()
    await callback.message.answer(text=m, reply_markup=tasks_kb(completed_tasks=completed_tasks))


@router.callback_query(TasksCallbackFactory.filter(F.page == 'wallet'))
async def tasks_wallet_callback(callback: types.CallbackQuery, **_):
    completed_tasks = await user_service.get_completed_tasks(user_id=callback.from_user.id)

    await callback.message.delete()
    await callback.message.answer(text='Выберите действие:', reply_markup=wallet_action_kb(completed_tasks))


@router.callback_query(WalletActionCallbackFactory.filter(F.action == 'connect'))
async def wallet_connect_callback(callback: types.CallbackQuery, **_):
    await callback.message.delete()

    completed_task = await user_service.get_completed_tasks(user_id=callback.from_user.id)
    if 'wallet' in completed_task:
        await callback.message.answer(text=msg.task_complete_already, reply_markup=return_tasks_kb())
        return

    connector = Connector(callback.from_user.id)

    is_connected = await connector.restore_connection()
    if is_connected:
        await callback.message.answer(text=msg.wallet_connected, reply_markup=return_tasks_kb())
        return

    try:
        wallets = [
            wallet['name']
            for wallet in connector.get_wallets()
        ]
    except FetchWalletsError:
        await connector.disconnect()
        wallets_list = await connector.connect(connector.get_wallets())
        wallets = [
            wallet['name']
            for wallet in wallets_list
        ]

    await callback.message.answer(text=msg.wallet, reply_markup=wallets_kb(wallets))


@router.callback_query(WalletCallbackFactory.filter())
async def wallet_callback(callback: types.CallbackQuery, callback_data: WalletCallbackFactory):
    await callback.message.delete()

    connector = Connector(callback.from_user.id)
    while True:
        try:
            url = await connector.connect(connector.get_wallets()[callback_data.index])
        except FetchWalletsError:
            await connector.disconnect()
        else:
            break

    qrcode.make(url).save(f'images/{callback.from_user.id}.png')

    qr = types.FSInputFile(f'images/{callback.from_user.id}.png')

    connect_msg = await callback.message.answer_photo(photo=qr, reply_markup=wallet_connect_kb(url))

    address = None
    for i in range(120):
        await asyncio.sleep(1)
        if connector.connected:
            try:
                address = Address(connector.account.address)
            except AddressError:
                break
            else:
                break

    await connect_msg.delete()

    if not address:
        await callback.message.answer(text=msg.wallet_conn_expired, reply_markup=wallet_try_again_kb())
        return

    wallet = address.to_str(is_user_friendly=True, is_bounceable=True)

    completed_tasks = await user_service.get_completed_tasks(user_id=callback.from_user.id)
    completed_tasks.append('wallet')
    await user_service.add_task(user_id=callback.from_user.id, completed_tasks=completed_tasks)

    await user_service.update_wallet(user_id=callback.from_user.id, wallet=wallet)
    await user_service.increase_balance(user_id=callback.from_user.id, k=WALLET_REWARD)

    m = format_increase(WALLET_REWARD)

    await callback.message.answer(text=m)
    await callback.message.answer(text=msg.wallet_conn_succeed, reply_markup=return_tasks_kb())


@router.callback_query(WalletActionCallbackFactory.filter(F.action == 'disconnect'))
async def wallet_disconnect_callback(callback: types.CallbackQuery, **_):
    connector = Connector(callback.from_user.id)
    await connector.restore_connection()
    await connector.disconnect()

    await user_service.update_wallet(user_id=callback.from_user.id, wallet=None)

    completed_tasks = await user_service.get_completed_tasks(user_id=callback.from_user.id)
    completed_tasks = [task for task in completed_tasks if task != 'wallet']
    await user_service.add_task(user_id=callback.from_user.id, completed_tasks=completed_tasks)
    await user_service.decrease_balance(user_id=callback.from_user.id, k=WALLET_REWARD)

    await callback.message.delete()
    await callback.message.answer(text=msg.wallet_disconnect)
    await callback.message.answer(text=msg.task_incomplete_wallet, reply_markup=return_tasks_kb())


@router.callback_query(TasksCallbackFactory.filter(F.page == 'channel'))
async def task_channel_callback(callback: types.CallbackQuery, **_):
    await callback.message.delete()

    completed_task = await user_service.get_completed_tasks(user_id=callback.from_user.id)
    if 'channel' in completed_task:
        await callback.message.answer(text=msg.task_complete_already, reply_markup=return_tasks_kb())
        return

    await callback.message.answer(text=msg.task_channel, reply_markup=task_check_kb(task='channel'))


@router.callback_query(TasksCallbackFactory.filter(F.page == 'name'))
async def task_name_callback(callback: types.CallbackQuery, **_):
    await callback.message.delete()

    completed_task = await user_service.get_completed_tasks(user_id=callback.from_user.id)
    if 'name' in completed_task:
        await callback.message.answer(text=msg.task_complete_already, reply_markup=return_tasks_kb())
        return

    await callback.message.answer(text=msg.task_name, reply_markup=task_check_kb(task='name'))


@router.inline_query()
async def task_ref_inline(inline: types.InlineQuery):
    ref_link = await create_start_link(bot, f'ref_{inline.from_user.id}')

    results = [
        types.InlineQueryResultArticle(
            id='1',
            title='Отправить приглашение',
            input_message_content=types.InputTextMessageContent(
                message_text=format_ref(inline.from_user.first_name)
            ),
            reply_markup=task_ref_kb(url=ref_link)
        )
    ]

    await bot.answer_inline_query(inline.id, results=results, cache_time=0)


@router.callback_query(TasksCallbackFactory.filter(F.page == 'ref'))
async def task_ref_callback(callback: types.CallbackQuery, **_):
    m = format_ref(callback.from_user.first_name)

    await callback.message.delete()
    await callback.message.answer(text=m, reply_markup=task_invite_ref_kb(user_id=callback.from_user.id))


@router.callback_query(TaskCheckCallbackFactory.filter(F.task == 'channel'))
async def task_check_channel_callback(callback: types.CallbackQuery, **_):
    res = await bot.get_chat_member(chat_id=CHAT, user_id=callback.from_user.id)
    if res.status == 'left':
        await callback.answer(text=msg.task_incomplete)
        return

    completed_tasks = await user_service.get_completed_tasks(user_id=callback.from_user.id)
    completed_tasks.append('channel')
    await user_service.add_task(user_id=callback.from_user.id, completed_tasks=completed_tasks)

    await user_service.increase_balance(user_id=callback.from_user.id, k=CHANNEL_REWARD)

    m = format_increase(CHANNEL_REWARD)

    await callback.message.delete()
    await callback.message.answer(text=m)
    await callback.message.answer(text=msg.task_complete, reply_markup=return_tasks_kb())


@router.callback_query(TaskCheckCallbackFactory.filter(F.task == 'name'))
async def task_check_name_callback(callback: types.CallbackQuery, **_):
    first_name, last_name = callback.from_user.first_name or '', callback.from_user.last_name or ''
    if NAME not in first_name and NAME not in last_name:
        await callback.answer(text=msg.task_incomplete)
        return

    completed_tasks = await user_service.get_completed_tasks(user_id=callback.from_user.id)
    completed_tasks.append('name')
    await user_service.add_task(user_id=callback.from_user.id, completed_tasks=completed_tasks)

    await user_service.increase_balance(user_id=callback.from_user.id, k=NAME_REWARD)

    m = format_increase(NAME_REWARD)

    await callback.message.delete()
    await callback.message.answer(text=m)
    await callback.message.answer(text=msg.task_complete, reply_markup=return_tasks_kb())
