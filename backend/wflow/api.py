from fastapi import APIRouter

from globar_vars import Var

wflow_router = APIRouter(prefix='wflow')


@wflow_router.get('/{wflow_id}')
async def get_wflow(wflow_id):
    await Var.db.get_wflow(wflow_id)

