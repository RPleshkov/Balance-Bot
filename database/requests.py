import logging

from sqlalchemy import select

from database.models import Category, CategoryType, User, async_session

logger = logging.getLogger(__name__)


async def set_user(tg_id, name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        logger.info(user)
        if not user:
            session.add(User(tg_id=tg_id, name=name))
            await session.commit()


async def set_income_category(tg_id, name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        session.add(Category(user_id=user.id, name=name, type=CategoryType.income))
        await session.commit()
