import os
from typing import Union, Optional

from pytz import timezone
from motor import motor_asyncio

from agents.blockchain_agent.schemas import ContractsData
from auth.schemas import User
from responses import StandardException
from wflow.schemas import WFlow, WFlowPayload

ist = timezone("Asia/Kolkata")


class DataBase:
    def __init__(self):
        uri = os.environ.get('MONGO_URI', "mongodb://localhost:27017")
        self._client = motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client["BlockChio"]
        self.wflows = self.db['wflows']
        self.users = self.db['users']
        self.contracts = self.db['contracts']

    async def get_wflow(self, wflow_id: str):
        wflow_data = await self.wflows.find_one({'wflow_id': wflow_id})
        if not wflow_data:
            raise StandardException(details='workflow not found', status_code=404)
        print(wflow_data)
        wflow_data = WFlow(**wflow_data)

        return wflow_data

    async def get_wflows(self):
        wflow_data = await self.wflows.find({}, {'_id': 0} ).to_list(None)
        return wflow_data

    async def set_wflow(self, wflow_id: str, wflow: WFlowPayload):
        if not wflow.wflow_name:
            del wflow.wflow_name
        await self.wflows.update_one({'wflow_id': wflow_id}, {'$set': wflow.model_dump()}, upsert=True)

    async def create_wflow(self, wflow: WFlow):
        await self.wflows.insert_one(wflow.model_dump())

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

    async def get_addresses_from_db(self, user_id) -> Optional[ContractsData]:
        try:
            document = await  self.contracts.find_one({'user_id': user_id})
            if document:
                contract_data: ContractsData = ContractsData(**document)
                return contract_data
            return None
        except Exception as e:
            return None

    async def save_addresses_to_db(self, contract_data: ContractsData):
        try:
            await self.contracts.update_one({'wallet': contract_data.wallet}, {'$set': contract_data.model_dump()},
                                            upsert=True)
        except Exception as e:
            pass
