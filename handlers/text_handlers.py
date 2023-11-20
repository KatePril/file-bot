from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode

from os import listdir
from main import bot


router = Router()


@router.message(F.text == "/list_files")
async def list_files(message: Message):
    await message.answer("\n".join([f'`{file}`' for file in listdir("files/")]), parse_mode=ParseMode.MARKDOWN)


@router.message(F.text == "/download test.txt")
async def send_file(message: Message):
    file: str = message.text.split(" ")[-1]
    path = f"files/{file}"
    document = open(file=path)
    await bot.send_document(chat_id=message.chat.id, document=document)


async def list_commands(message):
    await message.answer("<b>Here is the list of the commands available:</b>\n"
                         "/list_files - show all files sent to the bot\n"
                         "/help - see all commands", parse_mode=ParseMode.HTML)


@router.message(F.text == "/help")
async def help(message: Message):
    await list_commands(message)


@router.message(F.text)
async def message_with_text(message: Message):
    await message.reply("*Hi here\!*\n_Talking with the bot is not currently available_\n"
                        "*_So, please make sure you have typed a command correctly or come back later_*",
                        parse_mode=ParseMode.MARKDOWN_V2)
    await list_commands(message)


@router.message(F)
async def message_with_file(message: Message):
    file_id = message.document.file_id
    file_name = message.document.file_name
    file = await bot.get_file(file_id)
    file_path = file.file_path
    try:
        await bot.download_file(file_path, f"files/{file_name}")
        await message.reply("Downloaded successfully")
    except:
        await message.reply("Failed to download")

