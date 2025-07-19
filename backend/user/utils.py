import asyncio
import datetime
from globar_vars import Var
from utils import tokenizer
from typing import Union
from auth.schemas import User

user_auth_mutex = asyncio.Lock()


def create_new_user(wallet: str) -> User:
    user_id = tokenizer.invoke_uid(prefix="usr")
    return User(
        user_id=user_id,
        wallet=wallet,
        is_active=True,
        is_superuser=False,
        is_admin=False,
        account_created=datetime.datetime.now(Var.IST),
        account_updated=datetime.datetime.now(Var.IST),
    )


# CREATE OR REGISTER USER
async def get_or_reg_user(wallet: Union[str, None] = None, ) -> User:
    async with user_auth_mutex:
        if wallet:
            user = await Var.db.get_user(wallet=wallet)
            # REGISTER AS NEW USER IF USER NOT FOUND
            if not user:
                user = create_new_user(wallet)
                await Var.db.reg_user(user)
        return user
