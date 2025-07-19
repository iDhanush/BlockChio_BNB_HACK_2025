import datetime
from typing import Union, Optional
from pydantic import BaseModel, EmailStr, constr


class User(BaseModel):
    user_id: str
    wallet: Union[str, None]

    is_active: bool
    is_superuser: bool
    is_admin: bool

    account_created: Union[datetime.datetime, None]
    account_updated: Union[datetime.datetime, None]


class Token(BaseModel):
    access_token: str
    refresh_token: str
    profile: dict


class RToken(BaseModel):
    user_id: str
    access_token: str
    profile: dict


class TokenPayload(BaseModel):
    user_id: str = None


class WalletAuthPayload(BaseModel):
    wallet: str
