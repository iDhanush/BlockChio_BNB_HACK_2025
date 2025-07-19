import os
from typing import Union

from pytz import timezone
from motor import motor_asyncio
from auth.schemas import User
from wflow.schemas import WFlow, WFlowPayload

ist = timezone("Asia/Kolkata")


class DataBase:
    def __init__(self):
        uri = os.environ.get('MONGO_URI', "mongodb://localhost:27017")
        self._client = motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client["BlockChio"]
        self.wflows = self.db['wflows']
        self.users = self.db['users']
        self.contrs = self.db['deployed_contracts']

    async def get_wflow(self, wflow_id: str):
        await self.wflows.find_one({'wflow_id': wflow_id})

    async def set_wflow(self, wflow_id: str, wflow: WFlowPayload):
        await self.wflows.update_one({'wflow_id': wflow_id}, {'$set': wflow.model_dump()}, upsert=True)

    async def create_wflow(self, wflow: WFlow):
        await self.wflows.insert_one({'$set': wflow.model_dump()})

    ##############################################################################################
    # USER FUNCTIONS #############################################################################
    ##############################################################################################

    # GET USER BY EMAIL OR USERID
    async def get_user(self, user_id=None, wallet=None) -> Union[User, None]:
        user_data = None
        if user_id:
            user_data = await self.users.find_one({'user_id': user_id})
        if wallet:
            user_data = await self.users.find_one({'wallet': wallet})
        return User(**user_data) if user_data else None

    # REGISTER NEW USER
    async def reg_user(self, user: User) -> User:
        await self.users.insert_one(user.model_dump())
        return user
