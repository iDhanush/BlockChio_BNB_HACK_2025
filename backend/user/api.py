from auth.schemas import User
from auth.auth import get_user
from fastapi import APIRouter, Depends

user_router = APIRouter(prefix='/v1/user', tags=["user"])


@user_router.get('/profile')
async def user_profile(user: User = Depends(get_user)):
    return {'wallet': user}
