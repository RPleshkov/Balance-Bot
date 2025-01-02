from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def inc_exp_kb():
    incom_button = InlineKeyboardButton(text="Доход", callback_data="incom_button")
    expense_button = InlineKeyboardButton(text="Расход", callback_data="expense_button")
    return InlineKeyboardMarkup(inline_keyboard=[[incom_button, expense_button]])
