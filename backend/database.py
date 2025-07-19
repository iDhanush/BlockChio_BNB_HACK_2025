import os
from pytz import timezone
from motor import motor_asyncio

from wflow.schemas import WoFl

ist = timezone("Asia/Kolkata")


class DataBase:
    def __init__(self):
        uri = os.environ.get('MONGO_URI', "mongodb://localhost:27017")
        self._client = motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client["BlockChio"]
        self.wofls = self.db['wofls']

    async def get_wflow(self, wofl_id: str):
        await self.wofls.find_one({'wofl_id': wofl_id})

    async def set_wflow(self, wofl_id: str, wofl: WoFl):
        await self.wofls.update_one({'wofl_id': wofl_id}, {'$set': wofl.model_dump()}, upsert=True)
