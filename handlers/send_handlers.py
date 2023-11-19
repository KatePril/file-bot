from aiogram import Router, F
from aiogram.types import Message
from os import listdir
from aiogram.enums import ParseMode


router = Router()

@router.message(F.text == "/list_files")
async def list_files(message: Message):
    await message.answer("\n".join([f'`{file}`' for file in listdir("files/")]), parse_mode=ParseMode.MARKDOWN)