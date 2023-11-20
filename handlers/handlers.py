from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command

from os import listdir
from main import bot

from states.SendToChatForm import SendToChatForm
from states.SendViaLink import SendViaLink
from aiogram.fsm.context import FSMContext

import requests
import json

from constants import BASE_URL, JSON_FILE
from utils import *

send_router = Router()
text_router = Router()
download_router = Router()


@send_router.message(Command("list_files"))
async def list_files(message: Message):
    await message.answer("\n".join([f'`{file}`' for file in listdir(BASE_URL)]), parse_mode=ParseMode.MARKDOWN)


@send_router.message(Command("send"))
async def send_via_link(message: Message, state: FSMContext):
    await state.set_state(SendViaLink.file_name)
    await message.answer("Enter the file name:")


@send_router.message(SendViaLink.file_name)
async def process_file_name_via_link(message: Message, state: FSMContext):
    await state.update_data(file_name=message.text)
    await state.set_state(SendViaLink.url)
    await message.answer("Enter the link:")


@send_router.message(SendViaLink.url)
async def process_url(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    data = await state.get_data()
    if await is_valid_url(data['url']):
        try:
            test_response = requests.post(data['url'], files={"form_field_name": f"{data['file_name']}"})
            if test_response.ok:
                await message.answer("File was uploaded successfully")
            else:
                await message.answer("Failed to upload the file\n"
                                     "*_Make sure name of your file is present in the list of the files_*", parse_mode=ParseMode.MARKDOWN_V2)
        except:
            await message.answer("Failed to upload the file\n"
                                 "*_Make sure name of your file is present in the list of the files_*", parse_mode=ParseMode.MARKDOWN_V2)
        await state.clear()
    else:
        await message.answer("Try entering link again")


@send_router.message(Command("download"))
async def send_file(message: Message, state: FSMContext):
    await state.set_state(SendToChatForm.file_name)
    await message.answer("Enter the file name:")


@send_router.message(SendToChatForm.file_name)
async def process_file_name(message: Message, state: FSMContext):
    await state.update_data(file_name=message.text)
    data = await state.get_data()
    await state.clear()

    try:
        f = open(JSON_FILE)
        files = json.load(f)
        f.close()
        await bot.send_document(chat_id=message.chat.id, document=files['files'][data['file_name']])
    except:
        await message.answer("Failed to send file\n"
                             "*_Make sure name of your file is present in the list of the files_*", parse_mode=ParseMode.MARKDOWN_V2)


@text_router.message(Command("help"))
async def help(message: Message):
    await list_commands(message)


@text_router.message(F.text)
async def message_with_text(message: Message):
    await message.reply("*Hi here\!*\n_Talking with the bot is not currently available_\n"
                        "*_So, please make sure you have typed a command correctly or come back later_*",
                        parse_mode=ParseMode.MARKDOWN_V2)
    await list_commands(message)


@download_router.message(F)
async def message_with_file(message: Message):
    file_id = message.document.file_id
    file_name = message.document.file_name
    file = await bot.get_file(file_id)
    file_path = file.file_path

    f = open(JSON_FILE)
    data = json.load(f)
    f.close()
    data['files'][file_name] = file_id

    json_object = json.dumps(data)

    with open(JSON_FILE, "w") as file_json:
        file_json.write(json_object)

    try:
        download_path = BASE_URL + file_name
        await bot.download_file(file_path, download_path)
        await message.reply("Downloaded successfully")
    except:
        await message.reply("Failed to download")
