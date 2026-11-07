from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    completed: bool

    description: str | None


class TaskCreateSchema(BaseModel):
    title: str

    description: str | None = None


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

    description: str | None = None
