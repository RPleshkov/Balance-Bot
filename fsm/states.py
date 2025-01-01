from aiogram.fsm.state import State, StatesGroup


class FSMChoiceCategory(StatesGroup):
    wait_category_name = State()
