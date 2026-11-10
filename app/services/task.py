from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task import TaskRepository
from app.schemas.task import TaskSchema, TaskCreateSchema, TaskUpdateSchema


class TaskNotFound(Exception):
    """Задача не найдена в БД"""


class TaskService:
    def __init__(self,db: AsyncSession) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)

    async def list_tasks(self, user_id: str) -> list[TaskSchema]:
        tasks_orm = await self.task_repository.get_all(user_id=user_id)
        return [TaskSchema.model_validate(task) for task in tasks_orm]

    async def create_task(self, user_id: str, task_create: TaskCreateSchema) -> TaskSchema:
        task_orm = await self.task_repository.create(title=task_create.title, description=task_create.description, user_id=user_id)
        await self.db.commit()
        return TaskSchema.model_validate(task_orm)

    async def update_task(self, task_id: str, user_id: str, task_update: TaskUpdateSchema) -> TaskSchema:
        task_for_update = await self.task_repository.get_by_id(task_id=task_id)
        if not task_for_update or task_for_update.user_id != user_id:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")
        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed
        if task_update.description is not None:
            task_for_update.description = task_update.description
    
        await self.db.commit()
        return TaskSchema.model_validate(task_for_update)
    
    async def delete_task(self, task_id: str, user_id: str) -> None:
        task_for_delete = await self.task_repository.get_by_id(task_id=task_id)
        if not task_for_delete or task_for_delete.user_id != user_id:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")
        await self.task_repository.delete(task_for_delete)
        await self.db.commit()
        