from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_settings_kb():
    button = InlineKeyboardButton(
        text="Приступить к настройке", callback_data="start_settings"
    )
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


def balance_settings_kb():
    button = InlineKeyboardButton(text="Далее", callback_data="balance_next_btn")
    return InlineKeyboardMarkup(inline_keyboard=[[button]])
