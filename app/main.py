from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings

from app.api.routers.task import router as task_router
from app.api.routers.auth import router as auth_router

settings = get_settings()


app = FastAPI()
app.include_router(router=task_router)
app.include_router(router=auth_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGIN,
    allow_methods=["*"],
)