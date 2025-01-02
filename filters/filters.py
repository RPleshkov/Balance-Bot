from aiogram.filters import BaseFilter
import re

from aiogram.types import Message


class BalanceFilter(BaseFilter):

    async def __call__(self, message: Message) -> bool | dict:
        text = message.text.replace(" ", "").replace(",", ".")
        pattern = r"\d+(\.?\d+)?"
        if re.fullmatch(pattern, text):
            if "." not in text:
                text = text + ".00"
            integer, fract = text.split(".")
            return {"balance": f"{integer}.{int(fract[:2]):0<2d}"}
        else:
            return False
