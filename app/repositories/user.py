from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserORM

class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, user_id: str) -> UserORM | None:
        return await self.db.get(UserORM, user_id)

    async def create(self, username: str, hashed_password: str) -> UserORM:
        new_user = UserORM(username=username, hashed_password=hashed_password)
        self.db.add(new_user)
        return new_user

    async def get_by_username(self, username: str) -> UserORM | None:
        return await self.db.scalar(select(UserORM).where(UserORM.username == username))