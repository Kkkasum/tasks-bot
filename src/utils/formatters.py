def format_start(username: str) -> str:
    start_msg = f'Привет, @{username}!\n\n'\
                f'Выполняй задания, чтобы увеличить баланс'

    return start_msg


def format_tasks(user_id: int, balance: int, ref: int, wallet: str | None) -> str:
    tasks_msg = f'Ваш ID: <code>{user_id}</code>\n'\
                f'Ваш баланс: {balance}\n'\
                f'Количество рефералов: {ref}\n'
    if wallet:
        tasks_msg += f'Ваш кошелек: <code>{wallet}</code>'

    return tasks_msg


def format_ref(name: str) -> str:
    ref_msg = f'<b>{name}</b> приглашает вас в бота'

    return ref_msg


def format_increase(k: int) -> str:
    increase_msg = f'Вы получили +{k} очков'

    return increase_msg
