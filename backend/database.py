import os
from pytz import timezone
from motor import motor_asyncio

from wflow.schemas import WFlow

ist = timezone("Asia/Kolkata")


class DataBase:
    def __init__(self):
        uri = os.environ.get('MONGO_URI', "mongodb://localhost:27017")
        self._client = motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client["BlockChio"]
        self.wflows = self.db['wflows']

    async def get_wflow(self, wflow_id: str):
        await self.wflows.find_one({'wflow_id': wflow_id})

    async def set_wflow(self, wflow_id: str, wflow: WFlow):
        await self.wflows.update_one({'wflow_id': wflow_id}, {'$set': wflow.model_dump()}, upsert=True)
