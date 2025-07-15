from aiogram.fsm.state import StatesGroup, State

class AdminStates(StatesGroup):
    add_admin = State()
    get_admin = State()
    delete_admin = State()
