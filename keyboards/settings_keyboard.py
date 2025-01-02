from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def inc_exp_kb():
    incom_category_button = InlineKeyboardButton(
        text="Доходы", callback_data="incom_category"
    )
    expensive_category_button = InlineKeyboardButton(
        text="Расходы", callback_data="expensive_category"
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[[incom_category_button, expensive_category_button]]
    )
