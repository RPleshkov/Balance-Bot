import logging

from sqlalchemy import select

from database.models import Category, CategoryType, User

logger = logging.getLogger(__name__)


async def set_user(session, tg_id, name):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        session.add(User(tg_id=tg_id, name=name))
        await session.commit()


async def set_income_category(session, tg_id, name):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    session.add(Category(user_id=user.id, name=name, type=CategoryType.income))
    await session.commit()
