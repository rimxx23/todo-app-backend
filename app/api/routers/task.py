from fastapi import APIRouter, status, Depends, HTTPException

from app.api.dependencies import get_current_user, get_task_service
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from app.schemas.user import UserSchema
from app.services.task import TaskService, TaskNotFound


router = APIRouter(prefix="/tasks")

@router.get("")
async def read_tasks(current_user: UserSchema = Depends(get_current_user), task_service: TaskService = Depends(get_task_service)) -> list[TaskSchema]:
    return await task_service.list_tasks(user_id=current_user.id)



@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreateSchema, 
    current_user: UserSchema = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
) -> TaskSchema:
    return await task_service.create_task(user_id=current_user.id, task_create=payload)


@router.patch("/{task_id}")
async def update_task(
    task_id: str, 
    payload: TaskUpdateSchema,
    current_user: UserSchema = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
) -> TaskSchema:
    try:
        return await task_service.update_task(task_id=task_id, user_id=current_user.id, task_update=payload)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) 


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, current_user: UserSchema = Depends(get_current_user), task_service: TaskService = Depends(get_task_service)) -> None:
    try:
        return await task_service.delete_task(task_id=task_id, user_id=current_user.id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) 
