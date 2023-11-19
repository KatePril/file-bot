from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode

router = Router()

@router.message(F.text)
async def message_with_text(message: Message):
    await message.reply("*Hi here\!*\n_Talking with the bot is not currently available_\n"
                         "*_So, please make sure you have typed a command correctly or come back later_*",
                        parse_mode=ParseMode.MARKDOWN_V2)
    await message.answer("<b>Here is the list of the commands available</b>", parse_mode=ParseMode.HTML)