from src.repos.user import UserRepo


class UserService:
    def __init__(self):
        self.repo = UserRepo()

    async def add_user(self, user_id: int, ref_id: int | None = None) -> int | None:
        return await self.repo.add_user(user_id=user_id, ref_id=ref_id)

    async def get_user(self, user_id: int) -> [int, int, str | None]:
        return await self.repo.get_user(user_id=user_id)

    async def get_ref(self, user_id: int) -> int:
        return await self.repo.get_ref(user_id=user_id)

    async def get_balance(self, user_id: int) -> int:
        return await self.repo.get_balance(user_id=user_id)

    async def get_wallet(self, user_id: int) -> str | None:
        return await self.repo.get_wallet(user_id=user_id)

    async def get_completed_tasks(self, user_id: int) -> list[str]:
        return await self.repo.get_completed_tasks(user_id=user_id)

    async def update_wallet(self, user_id: int, wallet: str) -> None:
        await self.repo.update_wallet(user_id=user_id, wallet=wallet)

    async def add_task(self, user_id: int, completed_tasks: list[str]) -> None:
        await self.repo.add_task(user_id=user_id, completed_tasks=completed_tasks)

    async def increase_balance(self, user_id: int, k: int) -> None:
        await self.repo.increase_balance(user_id=user_id, k=k)

    async def decrease_balance(self, user_id: int, k: int) -> None:
        await self.repo.decrease_balance(user_id=user_id, k=k)


user_service = UserService()
