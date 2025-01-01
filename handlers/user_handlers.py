from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon import LEXICON_RU
import database.requests as rq
from keyboards.settings_keyboard import inc_exp_kb
from fsm.states import FSMChoiceCategory
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def command_start_process(message: Message):
    await rq.set_user(message.from_user.id, message.from_user.first_name)
    await message.answer(
        text=f'{message.from_user.first_name}, добро пожаловать в Balance Bot!\n\n{LEXICON_RU["/start"]}'
    )


@router.message(Command(commands="settings"), StateFilter(default_state))
async def command_settings_process(message: Message):
    await message.answer(
        text="Куда вы хотите добавить категорию?", reply_markup=inc_exp_kb
    )


@router.callback_query(F.data == "incom_category", StateFilter(default_state))
async def income_category(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите название категории")
    await state.set_state(FSMChoiceCategory.wait_category_name)


@router.message(StateFilter(FSMChoiceCategory.wait_category_name))
async def category_name_process(message: Message, state: FSMContext):
    await rq.set_income_category(message.from_user.id, message.text)
    await message.answer(text=f"Категория {message.text} добавлена!")
