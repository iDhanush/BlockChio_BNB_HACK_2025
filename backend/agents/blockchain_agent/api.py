from auth.schemas import User
from auth.auth import get_user
from fastapi import APIRouter, Depends
from agents.blockchain_agent.blockchian import get_balance, payment, mint_nft

blockchain_router = APIRouter(prefix='/v1/test', tags=["test"])


@blockchain_router.get('/test')
async def test(url: str = None):
    return str(mint_nft(url))
