import re

from aiogram import Router, F, types
from aiogram.filters import CommandStart, CommandObject

from src.common import bot, CHAT, CHANNEL_REWARD, NAME_REWARD, REF_REWARD
from src.services.user import user_service
from src.bot.keyboards import menu_kb, MenuCallbackFactory
from src.utils.formatters import format_start
from src.utils import messages as msg


router = Router()


@router.message(CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r'ref_(\d+)'))))
async def menu(message: types.Message, command: CommandObject):
    ref_id = int(command.args.split('_')[1])

    if ref_id != message.from_user.id:
        if not await user_service.add_user(user_id=message.from_user.id, ref_id=ref_id):
            balance = await user_service.get_balance(user_id=ref_id)
            ref = await user_service.get_ref(user_id=ref_id)
            await bot.send_message(
                chat_id=ref_id,
                text=f'Вы пригласили нового реферала!\nВаш баланс: {balance + ref * REF_REWARD}'
            )

    m = format_start(username=message.from_user.username)

    await message.answer(text=m, reply_markup=menu_kb())


@router.message(CommandStart())
async def menu(message: types.Message):
    await user_service.add_user(user_id=message.from_user.id)

    m = format_start(username=message.from_user.username)

    await message.answer(text=m, reply_markup=menu_kb())

    completed_tasks = await user_service.get_completed_tasks(user_id=message.from_user.id)
    if 'channel' in completed_tasks:
        res = await bot.get_chat_member(chat_id=CHAT, user_id=message.from_user.id)
        if res.status == 'left':
            completed_tasks = [task for task in completed_tasks if task != 'channel']
            await user_service.add_task(user_id=message.from_user.id, completed_tasks=completed_tasks)
            await user_service.decrease_balance(user_id=message.from_user.id, k=CHANNEL_REWARD)

            await message.answer(text=msg.task_incomplete_channel)
    if 'name' in completed_tasks:
        first_name, last_name = message.from_user.first_name or '', message.from_user.last_name or ''
        if 'asd' not in first_name and 'asd' not in last_name:
            completed_tasks = [task for task in completed_tasks if task != 'name']
            await user_service.add_task(user_id=message.from_user.id, completed_tasks=completed_tasks)
            await user_service.decrease_balance(user_id=message.from_user.id, k=NAME_REWARD)

            await message.answer(text=msg.task_incomplete_name)


@router.callback_query(MenuCallbackFactory.filter(F.page == 'menu'))
async def menu_callback(callback: types.CallbackQuery, **_):
    m = format_start(username=callback.from_user.username)

    await callback.message.delete()
    await callback.message.answer(text=m, reply_markup=menu_kb())
