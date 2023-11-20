from aiogram.fsm.state import State, StatesGroup


class SendViaLink(StatesGroup):
    file_name = State()
    url = State()
