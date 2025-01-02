from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_settings_kb():
    button = InlineKeyboardButton(
        text="Приступить к настройке", callback_data="start_settings"
    )
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


def balance_settings_kb():
    button = InlineKeyboardButton(text="Далее", callback_data="balance_next_btn")
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


def income_settings_kb_1():
    button = InlineKeyboardButton(text="Назад", callback_data="income_back_btn")
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


def income_settings_kb_generator(category_names):
    builder = InlineKeyboardBuilder()
    for name, id in category_names:
        builder.row(
            InlineKeyboardButton(text=f"❌ {name}", callback_data=f"delete_{id}_btn")
        )
    builder.row(
        InlineKeyboardButton(text="Назад", callback_data="category_back_btn"),
        InlineKeyboardButton(text="Далее", callback_data="category_next_btn"),
        width=2,
    )
    return builder.as_markup()
