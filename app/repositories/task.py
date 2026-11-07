from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import TaskORM




class TaskRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[TaskORM]:
        return (await self.db.scalars(select(TaskORM))).all()
    
    async def get_by_id(self, task_id:str) -> TaskORM | None:
        return await self.db.get(TaskORM, task_id)
    
    async def create(self, title: str, description: str | None) -> TaskORM:
        new_task = TaskORM(title=title, description=description, completed=False)
        self.db.add(new_task)
        return new_task           

    async def delete(self, task: TaskORM) -> None:
        await self.db.delete(task)

