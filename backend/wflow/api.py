from random import sample

from fastapi import APIRouter
from auth.auth import get_user
from auth.schemas import User
from globar_vars import Var
from wflow.schemas import WFlow, WFlowPayload, sample_workflow
from utils.tokenizer import invoke_uid
from fastapi import Depends
from wflow.wflow import WorkflowExecutor

wflow_router = APIRouter(prefix='/wflow')


@wflow_router.post('/')
async def create_wflow(wflow_payload: WFlowPayload, user: User = Depends(get_user), ):
    wflow_data = WFlow(**wflow_payload.model_dump(), wflow_id=invoke_uid(prefix='wfl'), user_id=user.user_id)
    await Var.db.create_wflow(wflow_data)
    return wflow_data


@wflow_router.get('/{wflow_id}')
async def get_wflow(wflow_id, _user: User = Depends(get_user)):
    res = await Var.db.get_wflow(wflow_id)
    return res


@wflow_router.put('/{wflow_id}')
async def update_wflow(wflow_id: str, wflow_payload: WFlowPayload, _user: User = Depends(get_user)):
    await Var.db.set_wflow(wflow_id, wflow_payload)


@wflow_router.put('/{wflow_id}')
async def update_wflow(wflow_id: str, wflow_payload: WFlowPayload, _user: User = Depends(get_user)):
    await Var.db.set_wflow(wflow_id, wflow_payload)


@wflow_router.post('/{wflow_id}/execute')
async def execute_wflow(wflow_id: str, wflow_payload: WFlowPayload, _user: User = Depends(get_user)):
    await Var.db.set_wflow(wflow_id, wflow_payload)
    wflow_data = await Var.db.get_wflow(wflow_id)
    executor = WorkflowExecutor(workflow=wflow_data)
    await executor.execute("create a cute cat")

@wflow_router.get('/workflows')
async def list_workflows(user:User= Depends(get_user)):
    wflow_list = await Var.db.get_wflows(user.user_id)
    return {'wflow_list': wflow_list}