from random import randint

from aiogram import Router, F
from aiogram.types import Message
from main import bot

router = Router()


@router.message(F)
async def message_with_file(message: Message):
    file_id = message.document.file_id
    file_name = message.document.file_name
    file = await bot.get_file(file_id)
    file_path = file.file_path
    try:
        downloaded = await bot.download_file(file_path, f"files/{file_name}")
        await message.reply("Downloaded successfully")
    except:
        await message.reply("Failed to download")

