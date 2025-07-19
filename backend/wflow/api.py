from fastapi import APIRouter

from globar_vars import Var

wflow_router = APIRouter(prefix='wflow')


@wflow_router.get('/{wofl_id}')
async def get_wflow(wofl_id):
    await Var.db.get_wflow(wofl_id)
