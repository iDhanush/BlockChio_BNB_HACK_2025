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
        "sub": Var.ACCESS_TOKEN_JWT_SUBJECT}
    encoded_jwt = jwt.encode(access_token_payload, Var.SECRET_KEY, algorithm=Var.ALGORITHM)
    return encoded_jwt


# CREATE REFRESH TOKEN
def create_refresh_token(user_id: str) -> str:
    refresh_token_expires = timedelta(days=365)  # Set your desired refresh token duration
    refresh_token_payload = {
        "user_id": user_id,
        "iss": 'productgpt',
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + refresh_token_expires,
    }
    encoded_refresh_token = jwt.encode(refresh_token_payload, Var.R_SECRET_KEY, algorithm=Var.ALGORITHM)
    return encoded_refresh_token


# CREATE OTP TOKEN
def create_otp_token(email: str, otp, ip) -> str:
    otp_expires = timedelta(minutes=10)  # Set your desired refresh token duration
    refresh_token_payload = {
        "email": email,
        "otp": otp,
        "ip": ip,
        "iss": 'productgpt',
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + otp_expires,
    }
    otp_token = jwt.encode(refresh_token_payload, Var.R_SECRET_KEY, algorithm=Var.ALGORITHM)
    return otp_token


def invoke_otp() -> str:
    otp = randint(100000, 999999)
    return str(otp)


# CREATE RANDOM UNIQUE ID
def invoke_uid(length=10, prefix="uid"):
    char_pool = string.ascii_lowercase + string.ascii_uppercase + string.digits
    uid = "".join(random.choices(char_pool, k=length))
    return f'{prefix}_{uid}'
