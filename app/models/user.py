from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class UserORM(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]