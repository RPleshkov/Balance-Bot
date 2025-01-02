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


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start_process(message: Message, state: FSMContext, session: AsyncSession):
    await rq.upsert_user(
        session,
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.last_name,
    )
    await message.delete()
    await message.answer_photo(
        photo=LEXICON_RU["photo_1"],
        caption=LEXICON_RU["/start"],
        reply_markup=start_settings_kb(),
    )

    await state.set_state(FSMSettings.waiting_start_settings)


@router.callback_query(
    StateFilter(FSMSettings.waiting_start_settings), F.data == "start_settings"
)
async def start_settings_button_pressed(
    callback: CallbackQuery, state: FSMContext, bot: Bot
):
    await bot.edit_message_caption(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        caption=LEXICON_RU["balance_settings"],
    )
    await state.update_data(
        main_window={
            "chat_id": callback.message.chat.id,
            "message_id": callback.message.message_id,
        }
    )
    await state.set_state(FSMSettings.balance_state)


@router.message(StateFilter(FSMSettings.balance_state), BalanceFilter())
async def balance_entry_process(
    message: Message, balance: str, state: FSMContext, bot: Bot
):
    await message.delete()
    await bot.edit_message_caption(
        chat_id=(await state.get_data())["main_window"]["chat_id"],
        message_id=(await state.get_data())["main_window"]["message_id"],
        caption=f"Твой баланс: {balance}руб.\n\nЧтобы продолжить настройку - жми 'Далее'\n\n"
        "Чтобы изменить баланс, отправь в чат новую сумму.",
        reply_markup=balance_settings_kb(),
    )
    await state.update_data(balance=balance)


@router.message(StateFilter(FSMSettings.balance_state))
async def balance_other_process(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    await bot.edit_message_caption(
        chat_id=(await state.get_data())["main_window"]["chat_id"],
        message_id=(await state.get_data())["main_window"]["message_id"],
        caption=LEXICON_RU["incorrect_balance"],
    )


@router.callback_query(
    StateFilter(FSMSettings.balance_state), F.data == "balance_next_btn"
)
async def set_income_categories(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_caption(
        chat_id=(await state.get_data())["main_window"]["chat_id"],
        message_id=(await state.get_data())["main_window"]["message_id"],
        caption=LEXICON_RU["income_categories"],
        reply_markup=income_settings_kb_1(),
    )
    await state.set_state(FSMSettings.income_category)


@router.callback_query(
    StateFilter(FSMSettings.income_category), F.data == "income_back_btn"
)
async def back_income_btn_pressed(callback: CallbackQuery, state: FSMContext, bot: Bot):
    balance = (await state.get_data())["balance"]
    await bot.edit_message_caption(
        chat_id=(await state.get_data())["main_window"]["chat_id"],
        message_id=(await state.get_data())["main_window"]["message_id"],
        caption=f"Твой баланс: {balance}руб.\n\nЧтобы продолжить настройку - жми 'Далее'\n\n"
        "Чтобы изменить баланс, отправь в чат новую сумму.",
        reply_markup=balance_settings_kb(),
    )
    await state.set_state(FSMSettings.balance_state)


@router.message(StateFilter(FSMSettings.income_category))
async def set_income_category(
    message: Message, state: FSMContext, session: AsyncSession, bot: Bot
):
    await message.delete()
    await rq.set_income_category(session, message.from_user.id, message.text)
    categories = await rq.get_income_categories(session, message.from_user.id)
    await bot.edit_message_caption(
        chat_id=(await state.get_data())["main_window"]["chat_id"],
        message_id=(await state.get_data())["main_window"]["message_id"],
        caption=LEXICON_RU["categories_settings"],
        reply_markup=income_settings_kb_generator(categories),
    )


@router.callback_query(
    StateFilter(FSMSettings.income_category), F.data.split("_")[0] == "delete"
)
async def delete_income_category_process(
    callback: CallbackQuery, state: FSMContext, bot: Bot, session: AsyncSession
):
    await rq.delete_income_category(
        session, callback.from_user.id, callback.data.split("_")[1]
    )
    categories = await rq.get_income_categories(session, callback.from_user.id)
    await bot.edit_message_caption(
        chat_id=(await state.get_data())["main_window"]["chat_id"],
        message_id=(await state.get_data())["main_window"]["message_id"],
        caption=LEXICON_RU["categories_settings"],
        reply_markup=income_settings_kb_generator(categories),
    )


# @router.message()
# async def photo(message: Message):
#     print(message.model_dump_json(indent=4))
