import logging

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Category, CategoryType, User

logger = logging.getLogger(__name__)


async def upsert_user(
    session: AsyncSession,
    tg_id: int,
    first_name: str,
    last_name: str | None = None,
):
    """
    Добавление или обновление пользователя
    в таблице users
    :param session: сессия СУБД
    :param telegram_id: айди пользователя
    :param first_name: имя пользователя
    :param last_name: фамилия пользователя
    """
    stmt = upsert(User).values(
        {
            "tg_id": tg_id,
            "first_name": first_name,
            "last_name": last_name,
        }
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=["tg_id"],
        set_=dict(
            first_name=first_name,
            last_name=last_name,
        ),
    )
    await session.execute(stmt)
    await session.commit()


async def set_income_category(session, tg_id, name):
    session.add(Category(user_id=tg_id, name=name, type=CategoryType.income))
    await session.commit()


async def set_expensive_category(session, tg_id, name):
    session.add(Category(user_id=tg_id, name=name, type=CategoryType.expense))
    await session.commit()