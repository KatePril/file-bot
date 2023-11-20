from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command

from os import listdir
from main import bot

from states.SendToChatForm import SendToChatForm
from states.SendViaLink import SendViaLink
from aiogram.fsm.context import FSMContext

import re
import requests
import json

router = Router()


@router.message(Command("list_files"))
async def list_files(message: Message):
    await message.answer("\n".join([f'`{file}`' for file in listdir("files/")]), parse_mode=ParseMode.MARKDOWN)


@router.message(Command("send"))
async def send_via_link(message: Message, state: FSMContext):
    await state.set_state(SendViaLink.file_name)
    await message.answer("Enter the file name:")


@router.message(SendViaLink.file_name)
async def process_file_name_via_link(message: Message, state: FSMContext):
    await state.update_data(file_name=message.text)
    await state.set_state(SendViaLink.url)
    await message.answer("Enter the link:")


async def is_valid_url(url):
    regex = re.compile(
        r'^(https?|ftp)://'
        r'([A-Za-z0-9-]+\.)+[A-Za-z]{2,}'
        r'(:\d+)?'
        r'(/[^\s]*)?$'
    )
    return bool(re.match(regex, url))


@router.message(SendViaLink.url)
async def process_url(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    data = await state.get_data()
    if await is_valid_url(data['url']):
        try:
            test_response = requests.post(data['url'], files={"form_field_name": f"{data['file_name']}"})
            if test_response.ok:
                await message.answer("File was uploaded successfully")
            else:
                await message.answer("Failed to upload the file")
        except:
            await message.answer("Failed to upload the file")
        await state.clear()
    else:
        await message.answer("Try entering link again")


@router.message(Command("download"))
async def send_file(message: Message, state: FSMContext):
    await state.set_state(SendToChatForm.file_name)
    await message.answer("Enter the file name:")


@router.message(SendToChatForm.file_name)
async def process_file_name(message: Message, state: FSMContext):
    await state.update_data(file_name=message.text)
    data = await state.get_data()
    await state.clear()

    try:
        f = open("files_id.json")
        files = json.load(f)
        f.close()
        await bot.send_document(chat_id=message.chat.id, document=files['files'][data['file_name']])
    except:
        await message.answer("Failed to send file")


async def list_commands(message):
    await message.answer("<b>Here is the list of the commands available:</b>\n"
                         "/list_files - show all files sent to the bot\n"
                         "/help - see all commands\n"
                         "/download - send one of the files you have sent to the bot\n"
                         "/send - send fil via link", parse_mode=ParseMode.HTML)


@router.message(Command("help"))
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

    f = open("files_id.json")
    data = json.load(f)
    f.close()
    data['files'][file_name] = file_id

    json_object = json.dumps(data)

    with open("files_id.json", "w") as file_json:
        file_json.write(json_object)


    try:
        await bot.download_file(file_path, f"files/{file_name}")
        await message.reply("Downloaded successfully")
    except:
        await message.reply("Failed to download")
