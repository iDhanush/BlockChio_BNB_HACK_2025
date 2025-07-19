from fastapi import APIRouter
from globar_vars import Var
from wflow.schemas import WFlow, WFlowPayload
from utils.tokenizer import invoke_uid

wflow_router = APIRouter(prefix='/wflow')


@wflow_router.post('/')
async def create_wflow(wflow_payload: WFlowPayload):
    wflow_data = WFlow(**wflow_payload.model_dump(), wflow_id=invoke_uid(prefix='wfl'), user_id=invoke_uid('usr') )
    await Var.db.create_wflow(wflow_data)


@wflow_router.get('/{wflow_id}')
async def get_wflow(wflow_id):
    await Var.db.get_wflow(wflow_id)


@wflow_router.put('/{wflow_id}')
async def update_wflow(wflow_id: str, wflow_payload: WFlowPayload):
    await Var.db.set_wflow(wflow_id, wflow_payload)
