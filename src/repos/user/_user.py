from sqlalchemy import insert, select, update

from src.database import Database, User


class UserRepo(Database):
    def __init__(self):
        super().__init__()

    async def add_user(self, user_id: int, ref_id: int | None) -> None:
        async with self.session_maker() as session:
            query = select(User.id)\
                .where(User.id == user_id)
            res = (await session.execute(query)).scalar()
            if res:
                return 1

            stmt = insert(User)\
                .values(id=user_id, ref_id=ref_id)
            await session.execute(stmt)
            await session.commit()

    async def get_user(self, user_id: int) -> [int, int, str | None]:
        async with self.session_maker() as session:
            query = select(User.id)\
                .where(User.ref_id == user_id)
            ref = len((await session.execute(query)).fetchall())

            query = select(User.balance, User.wallet)\
                .where(User.id == user_id)
            res = (await session.execute(query)).first()

            return ref, res[0], res[1]

    async def get_ref(self, user_id: int) -> int:
        async with self.session_maker() as session:
            query = select(User.id)\
                .where(User.ref_id == user_id)
            res = len((await session.execute(query)).fetchall())

            return res

    async def get_balance(self, user_id: int) -> int:
        async with self.session_maker() as session:
            query = select(User.balance)\
                .where(User.id == user_id)
            res = (await session.execute(query)).scalar()

            return res

    async def get_wallet(self, user_id: int) -> str | None:
        async with self.session_maker() as session:
            query = select(User.wallet)\
                .where(User.id == user_id)
            res = (await session.execute(query)).first()

            return res[0]

    async def get_completed_tasks(self, user_id: int) -> list[str]:
        async with self.session_maker() as session:
            query = select(User.tasks)\
                .where(User.id == user_id)
            res = (await session.execute(query)).first()

            return res[0]

    async def update_wallet(self, user_id: int, wallet: str) -> None:
        async with self.session_maker() as session:
            stmt = update(User) \
                .where(User.id == user_id) \
                .values(wallet=wallet)
            await session.execute(stmt)
            await session.commit()

    async def add_task(self, user_id: int, completed_tasks: list[str]) -> None:
        async with self.session_maker() as session:
            stmt = update(User) \
                .where(User.id == user_id) \
                .values(tasks=completed_tasks)
            await session.execute(stmt)
            await session.commit()

    async def increase_balance(self, user_id: int, k: int) -> None:
        async with self.session_maker() as session:
            query = select(User.balance)\
                .where(User.id == user_id)
            balance = (await session.execute(query)).scalar()

            stmt = update(User)\
                .where(User.id == user_id)\
                .values(balance=balance + k)
            await session.execute(stmt)
            await session.commit()

    async def decrease_balance(self, user_id: int, k: int) -> None:
        async with self.session_maker() as session:
            query = select(User.balance)\
                .where(User.id == user_id)
            balance = (await session.execute(query)).scalar()

            stmt = update(User)\
                .where(User.id == user_id)\
                .values(balance=balance - k)
            await session.execute(stmt)
            await session.commit()
