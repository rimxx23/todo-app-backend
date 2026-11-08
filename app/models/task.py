from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column

from app.models.base import Base


class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)

    description: Mapped[str | None] 

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))