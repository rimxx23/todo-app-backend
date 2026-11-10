from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserSchema
from app.services.task import TaskService
from app.services.user import InvalidCredentials
from app.db.session import get_db
from app.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_task_service(db: AsyncSession = Depends(get_db)):
    return TaskService(db)

def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
) -> UserSchema:
    try:
        return await user_service.get_user_by_token(token=token)
    except InvalidCredentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"})