import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password, decode_access_token
from app.repositories.user import UserRepository
from app.schemas.user import TokenSchema, UserCreateSchema, UserSchema

class UserAlreadyExists(Exception):
    """Пользователь с таким именем уже занят"""

class InvalidCredentials(Exception):
    """Неверный логин или пароль"""

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db)

    async def register(self, user_create: UserCreateSchema) -> UserSchema:
        if await self.user_repository.get_by_username(username=user_create.username):
            raise UserAlreadyExists("Пользователь с таким именем уже занят")
        hashed_password = hash_password(user_create.password)
        user_orm = await self.user_repository.create(username=user_create.username, hashed_password=hashed_password)
        await self.db.commit()
        return UserSchema.model_validate(user_orm)

    async def login(self, username: str, password: str) -> TokenSchema:
        user = await self.user_repository.get_by_username(username=username)
        if not user:
            raise InvalidCredentials("Неверный логин или пароль")
        if not verify_password(password=password, hashed_password=user.hashed_password):
            raise InvalidCredentials("Неверный логин или пароль")
        access_token = create_access_token(user.id)
        return TokenSchema(access_token=access_token)

    async def get_user_by_token(self, token: str) -> UserSchema:
        try:
            user_id = decode_access_token(token=token)
        except jwt.InvalidTokenError:
            raise InvalidCredentials("Неверный логин или пароль")
        user = await self.user_repository.get_by_id(user_id=user_id)
        if not user:
            raise InvalidCredentials("Неверный логин или пароль")
        return UserSchema.model_validate(user)
