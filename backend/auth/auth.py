import jwt
from fastapi import Depends
import json
import aiohttp
from globar_vars import Var
from utils import tokenizer
from typing import Tuple, Optional
from user.utils import get_or_reg_user
from responses import StandardException
from fastapi import Request, security, Security
from auth.schemas import TokenPayload, User

reusable_oauth2 = security.OAuth2PasswordBearer(tokenUrl="/auth")


async def get_token(request: Request) -> str:
    payload = json.loads((await request.body()).decode())
    return payload.get('token')


async def decode_token(token: str, secret_key: str, algorithm: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise StandardException(status_code=403, details="Token has expired", message='Token has expired')
    except jwt.InvalidTokenError:
        raise StandardException(status_code=403, details="Invalid token", message='Invalid token')


async def get_access_token(refresh_token) -> tuple:
    token_data = await decode_token(refresh_token, Var.R_SECRET_KEY, Var.ALGORITHM)
    user = await Var.db.get_user(user_id=token_data.user_id)
    if not user:
        raise StandardException(status_code=403, details="User not found", message='User not found')
    token = tokenizer.create_access_token(token_data.user_id)
    return user, token


async def get_current_user(
        request: Request,
        token: Optional[str] = None if Var.TEST_MODE else Depends(reusable_oauth2)
):
    # If no token from header, check cookie
    if token is None:
        token = request.cookies.get("aTok")

    if not token:
        raise StandardException(status_code=401, details="Unauthorized", message="Missing access token")

    token_data = await decode_token(token, Var.SECRET_KEY, Var.ALGORITHM)
    user = await Var.db.get_user(user_id=token_data.user_id)
    if not user:
        raise StandardException(status_code=403, details="User not found", message="User not found")

    return user


async def get_user(current_user: User = Security(get_current_user)):
    if not current_user.is_active:
        raise StandardException(status_code=488, details="User Blocked", message='User Blocked')
    return current_user


async def get_superuser(current_user: User = Security(get_current_user)):
    if not current_user.is_superuser:
        raise StandardException(
            status_code=403, details="The user doesn't have enough privileges",
            message='The user doesn\'t have enough privileges'
        )
    return current_user


async def wallet_auth(wallet: str) -> Tuple:
    try:
        user = await get_or_reg_user(wallet=wallet)
        # Generate tokens
        internal_token = tokenizer.create_access_token(user.user_id)
        refresh_token = tokenizer.create_refresh_token(user.user_id)

        return user, internal_token, refresh_token
    except aiohttp.ClientError as e:
        raise StandardException(500, "Network error connecting to Google", str(e))
    except jwt.PyJWTError as e:
        raise StandardException(401, "Invalid authentication token", str(e))
    except Exception as e:
        raise StandardException(500, "Authentication failed", str(e))
