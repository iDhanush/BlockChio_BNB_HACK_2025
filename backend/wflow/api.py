from fastapi import APIRouter

from auth.auth import get_user
from auth.schemas import User
from globar_vars import Var
from wflow.schemas import WFlow, WFlowPayload
from utils.tokenizer import invoke_uid
from fastapi import Depends

wflow_router = APIRouter(prefix='/wflow')


@wflow_router.post('/')
async def create_wflow(wflow_payload: WFlowPayload, user: User = Depends(get_user), ):
    wflow_data = WFlow(**wflow_payload.model_dump(), wflow_id=invoke_uid(prefix='wfl'), user_id=user.user_id)
    await Var.db.create_wflow(wflow_data)
    return wflow_data

@wflow_router.get('/{wflow_id}')
async def get_wflow(wflow_id):
    res = await Var.db.get_wflow(wflow_id)
    return res

@wflow_router.put('/{wflow_id}')
async def update_wflow(wflow_id: str, wflow_payload: WFlowPayload):
    await Var.db.set_wflow(wflow_id, wflow_payload)


@wflow_router.put('/{wflow_id}')
async def update_wflow(wflow_id: str, wflow_payload: WFlowPayload):
    await Var.db.set_wflow(wflow_id, wflow_payload)
