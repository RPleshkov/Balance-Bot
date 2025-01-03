from email.mime import message
from aiogram import F, Bot, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

import database.requests as rq
from fsm.states import FSMSettings
from keyboards.settings_keyboard import *
from lexicon.lexicon import LEXICON_RU
from filters.filters import BalanceFilter


router = Router()
