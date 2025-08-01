import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from wflow.schemas import Node, WFlow, sample_workflow, telegram_blockchain_workflow
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
    query = message.text

    runnable = WorkflowExecutor(workflow=telegram_blockchain_workflow)
    await runnable.execute(query)

    await message.answer(f"Workflow Execution Finished!")


# Main function to run the bot
async def start_telegram_trigger():
    asyncio.create_task(dp.start_polling(bot))

# class BaseTrigger:
#     def __init__(self, node: Node, wflow: WFlow, workflow_registry):
#         self.node = node
#         self.wflow = wflow
#         self.workflow_registry = workflow_registry
#
#     async def start(self):
#         raise NotImplementedError
#
# class TelegramTrigger(BaseTrigger):
#     def __init__(self, node: Node, wflow: WFlow, workflow_registry):
#         super().__init__(node, wflow, workflow_registry)
#         self.bot_token = node.creds[0]['bot_token']
#         self.bot = Bot(token=self.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#         self.dp = Dispatcher()  # Initialize empty dispatcher
#         self.dp.include_router(self._get_router())  # ✅ Add router manually
#
#     def _get_router(self):
#         from aiogram import Router
#         router = Router()
#
#         @router.message()
#         async def handle_message(message: Message):
#             print("Received message:", message.text)
#             query = message.text
#
#             runnable = self.workflow_registry[self.wflow.wflow_id]
#             final_output = await runnable.run(self.node.node_id, query)
#
#             await message.answer(f"Workflow complete.\n\nOutput:\n{final_output}")
#
#         return router
#
#     async def start(self):
#         print('polling starteeeeeeeeeeeeeeeeeeeeeeeeeed')
#         asyncio.create_task(self.dp.start_polling(self.bot))  # ✅ Pass bot here explicitly
