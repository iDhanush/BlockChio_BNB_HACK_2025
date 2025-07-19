from platform import freedesktop_os_release
import jwt
import random
import string
from globar_vars import Var
from random import randint
from datetime import datetime, timedelta


# CREATE ACCESS TOKEN
def create_access_token(user_id: str) -> str:
    expires_delta = timedelta(minutes=Var.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_payload = {
        "user_id": user_id,
        "iss": 'productgpt',
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + expires_delta,
        "sub": Var.ACCESS_TOKEN_JWT_SUBJECT
    }

    print('ssssssssssssssss', access_token_payload, Var.SECRET_KEY, Var.ALGORITHM)
    encoded_jwt = jwt.encode(access_token_payload, Var.SECRET_KEY, algorithm=Var.ALGORITHM)
    return encoded_jwt


def create_refresh_token(user_id: str) -> str:
    refresh_token_expires = timedelta(days=365)  # 1-year expiry
    refresh_token_payload = {
        "user_id": user_id,
        "iss": "productgpt",  # Issuer
        "iat": datetime.utcnow(),  # Issued at
        "exp": datetime.utcnow() + refresh_token_expires  # Expiration
    }
    encoded_refresh_token = jwt.encode(
        refresh_token_payload,
        Var.R_SECRET_KEY,
        algorithm=Var.ALGORITHM
    )
    return encoded_refresh_token


def invoke_otp() -> str:
    otp = randint(100000, 999999)
    return str(otp)


# CREATE RANDOM UNIQUE ID
def invoke_uid(length=10, prefix="uid"):
    char_pool = string.ascii_lowercase + string.ascii_uppercase + string.digits
    uid = "".join(random.choices(char_pool, k=length))
    return f'{prefix}_{uid}'
