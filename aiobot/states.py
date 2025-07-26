from aiogram.fsm.state import StatesGroup, State

class AdForm(StatesGroup):
    title = State()
    price = State()
    size = State()
    condition = State()
    photos = State()
    confirm = State() 