from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.task import TaskService
from app.db.session import get_db



def get_task_service(db: AsyncSession = Depends(get_db)):
    return TaskService(db)