from aiogram.fsm.state import State, StatesGroup


class SendToChatForm(StatesGroup):
    file_name = State()
