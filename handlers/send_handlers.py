from aiogram import Router, F
from aiogram.types import Message
from os import listdir
from aiogram.enums import ParseMode
from main import bot

router = Router()

@router.message(F.text == "/list_files")
async def list_files(message: Message):
    await message.answer("\n".join([f'`{file}`' for file in listdir("files/")]), parse_mode=ParseMode.MARKDOWN)

@router.message(F.text == "/download test.txt")
async def send_file(message: Message):
    file = message.text.split(" ")[-1]
    document = open(path=f"files/{file}")
    await bot.send_document(document=document)