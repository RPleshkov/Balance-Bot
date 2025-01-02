from aiogram.fsm.state import State, StatesGroup


class FSMSettings(StatesGroup):
    waiting_start_settings = State()
    balance_state = State()
    income_category = State()
    expense_category = State()


class FSMMainProcess(StatesGroup):
    main_process = State()
