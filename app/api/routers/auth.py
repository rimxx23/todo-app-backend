from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_current_user, get_user_service
from app.schemas.user import TokenSchema, UserCreateSchema, UserSchema
from app.services.user import UserService
from app.services.user import UserAlreadyExists, InvalidCredentials


router = APIRouter(prefix="/auth")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreateSchema, user_service: UserService = Depends(get_user_service)) -> UserSchema:
    try:
        return await user_service.register(user_create=payload)
    except UserAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends(get_user_service)) -> TokenSchema:
    try:
        return await user_service.login(username=form_data.username, password=form_data.password)
    except InvalidCredentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"})

@router.get("/me")
async def me(current_user: UserSchema = Depends(get_current_user)) -> UserSchema:
    return current_user
