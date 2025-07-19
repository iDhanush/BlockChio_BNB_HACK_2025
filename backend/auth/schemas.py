import datetime
from typing import Union, Optional
from pydantic import BaseModel, EmailStr, constr


class User(BaseModel):
    user_id: str
    username: constr(pattern=r'^[a-zA-Z0-9_]+$')
    phone: Union[str, None] = None

    email: Union[EmailStr, None] = None
    name: Union[str, None] = None

    avatar: Union[str, None] = None

    is_active: bool
    is_superuser: bool
    is_admin: bool
    temp_user: bool = False
    account_created: Union[datetime.datetime, None]
    account_updated: Union[datetime.datetime, None]
    origin: str = 'web'
    profile_complete: bool
    kyc_completed: bool


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


class OtpRequest(BaseModel):
    email: str
    otp: str
    ip: str
    otp_token: str
    requested_at: datetime.datetime


class OtpAttempt(BaseModel):
    email: str
    otp: str
    ip: str
    attempted_at: datetime.datetime


class EmailAuthPayload(BaseModel):
    email: EmailStr
    otp: Union[str, None] = None
    temp_user_token: Optional[str] = None


class PhoneAuthPayload(BaseModel):
    phone: str
    otp: Union[str, None] = None
    verification_id: Union[str, None] = None
    temp_user_token: Optional[str] = None


class GoogleAuthPayload(BaseModel):
    code: str
    uri: str = 'https://productgpt.in/'
    temp_user_token: Optional[str] = None
