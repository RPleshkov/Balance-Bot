from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
import database.requests as rq


router = Router()


@router.message(CommandStart())
async def command_start_process(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(text="Привет!")
