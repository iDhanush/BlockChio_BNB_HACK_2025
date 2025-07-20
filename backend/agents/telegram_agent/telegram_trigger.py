from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
import asyncio
import logging

from wflow.schemas import sample_workflow2
from wflow.wflow import WorkflowExecutor

# Enable logging
logging.basicConfig(level=logging.INFO)

# Replace with your actual bot token
BOT_TOKEN = "1765542474:AAHpERwNgs7o9_qkxmkaDqwOhN5T9efmSSs"

# Initialize bot and dispatcher
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(bot=bot)

# Echo handler
@dp.message()
async def echo(message: Message):
    work_flow = WorkflowExecutor(workflow=sample_workflow2)
    await work_flow.execute(message.text)
# Main function to run the bot
async def start_telegram_trigger():
    asyncio.create_task(dp.start_polling(bot))
