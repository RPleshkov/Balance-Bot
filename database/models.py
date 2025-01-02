from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import BigInteger


class Base(DeclarativeBase):
    pass


class CategoryType(Enum):
    income = "income"
    expense = "expense"


class User(Base):
    __tablename__ = "users"

    tg_id = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    name: Mapped[str] = mapped_column()
    type: Mapped[CategoryType]
