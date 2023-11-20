import re
from aiogram.enums import ParseMode

async def is_valid_url(url):
    regex = re.compile(
        r'^(https?|ftp)://'
        r'([A-Za-z0-9-]+\.)+[A-Za-z]{2,}'
        r'(:\d+)?'
        r'(/[^\s]*)?$'
    )
    return bool(re.match(regex, url))


async def list_commands(message):
    await message.answer("<b>Here is the list of the commands available:</b>\n"
                         "/list_files - show all files sent to the bot\n"
                         "/help - see all commands\n"
                         "/download - send one of the files you have sent to the bot\n"
                         "/send - send file via link", parse_mode=ParseMode.HTML)