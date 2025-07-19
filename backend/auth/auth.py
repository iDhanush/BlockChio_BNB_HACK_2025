import asyncio
import random
from google.oauth2 import id_token
import jwt
import json
import aiohttp
import datetime
from auth.utils import email_template
from utils.tokenizer import invoke_otp
from globar_vars import Var
from utils import tokenizer
from typing import Tuple, Optional
from user.utils import get_or_reg_user, reg_temp_user
from responses import StandardException
from fastapi import Request, security, Security
from auth.schemas import TokenPayload, User, OtpAttempt, OtpRequest, PhoneAuthPayload
from google.auth.transport import requests

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


async def get_current_user(token: str = None if Var.TEST_MODE else Security(reusable_oauth2)):
    if Var.TEST_MODE:
        # user = await get_test_user()
        user = await Var.db.get_user(user_id='usr_1RpgF4sAQC')
    else:
        token_data = await decode_token(token, Var.SECRET_KEY, Var.ALGORITHM)
        user = await Var.db.get_user(user_id=token_data.user_id)
    if not user:
        raise StandardException(status_code=403, details="User not found", message='User not found')
    return user


async def get_beta_user(token: str = Security(reusable_oauth2)):
    token_data = await decode_token(token, Var.SECRET_KEY, Var.ALGORITHM)
    user = await Var.db.get_user(user_id='usr_4L9ptTsLrK')
    if not user:
        raise StandardException(status_code=403, details="User not found", message='User not found')
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


async def google_auth(code: str, uri: str, temp_user_id: str) -> Tuple:
    """Complete Google OAuth flow and return user information with tokens"""
    try:
        # Get ID token with exponential backoff retry strategy
        id_token_value = await get_idtoken_with_retry(code, uri)

        # Verify and decode the token
        idinfo = verify_and_decode_token(id_token_value)
        # Get or register user
        print(idinfo)
        user = await get_or_reg_user(
            email=idinfo.get('email'),
            name=idinfo.get('name'),
            avatar=idinfo.get('picture'),
            temp_user_id=temp_user_id
        )

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


async def get_idtoken_with_retry(code: str, uri: str) -> str:
    """Get ID token with exponential backoff retry strategy"""
    max_retries = 5
    base_delay = 1  # Start with 1-second delay

    for attempt in range(max_retries):
        try:
            return await request_idtoken(code, uri)
        except StandardException as e:
            # Don't retry on client errors (4xx)
            if e.status_code < 500:
                raise

            # Calculate delay with exponential backoff and some jitter
            delay = min(base_delay * (2 ** attempt) + (random.random() * 0.5), 15)

            # Log the retry attempt
            if attempt < max_retries - 1:
                await asyncio.sleep(delay)
            else:
                raise

    # This should never happen due to the raise in the loop
    raise StandardException(500, "Failed to get ID token after multiple attempts")


async def request_idtoken(code: str, uri: str) -> str:
    """Request ID token from Google OAuth API"""
    timeout = aiohttp.ClientTimeout(total=10, connect=3, sock_read=7)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            response = await session.post(
                'https://accounts.google.com/o/oauth2/token',
                data={
                    "code": code,
                    "client_id": Var.GOOGLE_CLIENT_ID,
                    "client_secret": Var.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": uri,
                    "grant_type": "authorization_code"
                }
            )

            # Read response body (needed for both success and error cases)
            response_text = await response.text()

            if response.status != 200:

                if response.status == 400:
                    # Client errors like invalid code
                    raise StandardException(403, "Invalid authorization code", response_text)
                elif response.status == 429:
                    # Rate limiting
                    raise StandardException(429, "Rate limited by Google", response_text)
                else:
                    # Other server errors
                    raise StandardException(response.status, "Google authentication failed", response_text)

            # Parse response JSON
            try:
                response_data = await response.json()
            except Exception as e:
                raise StandardException(500, "Invalid response from Google", response_text)

            # Extract and return ID token
            id_token_value = response_data.get('id_token')
            if not id_token_value:
                raise StandardException(500, "Missing ID token in response", response_text)

            return id_token_value

        except aiohttp.ClientError as e:
            raise StandardException(500, "Network error", str(e))


def verify_and_decode_token(token: str) -> dict:
    """Verify and decode the Google ID token"""
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            Var.GOOGLE_CLIENT_ID
        )
        if idinfo.get('aud') != Var.GOOGLE_CLIENT_ID:
            raise StandardException(401, "Token was not issued for this application")
        return idinfo

    except jwt.PyJWTError as e:
        raise StandardException(401, "Invalid token format", str(e))


async def email_auth(otp_attempt: OtpAttempt, temp_user_id:Optional[str] = None):
    if not await Var.db.verify_otp(otp_attempt):
        raise StandardException(400, "Invalid OTP", message="Invalid OTP. Please try again")

    user = await get_or_reg_user(email=otp_attempt.email, temp_user_id=temp_user_id)
    internal_token = tokenizer.create_access_token(user.user_id)
    refresh_token = tokenizer.create_refresh_token(user.user_id)
    return user, internal_token, refresh_token


async def phone_auth(phone_payload: PhoneAuthPayload):
    is_verified = await validate_otp(phone_payload.phone, phone_payload.verification_id, phone_payload.otp)
    if not is_verified:
        raise StandardException(400, "Invalid OTP", message="Invalid OTP. Please try again")
    user = await get_or_reg_user(phone=f'91{phone_payload.phone}')
    internal_token = tokenizer.create_access_token(user.user_id)
    refresh_token = tokenizer.create_refresh_token(user.user_id)
    return user, internal_token, refresh_token


async def temp_auth():
    user = await reg_temp_user()
    internal_token = tokenizer.create_access_token(user.user_id)
    refresh_token = tokenizer.create_refresh_token(user.user_id)
    return user, internal_token, refresh_token


def get_otp_token(email: str, otp: str, ip: str) -> str:
    otp_token = tokenizer.create_otp_token(email, otp, ip)
    return otp_token


async def generate_otp(email: str, ip: str) -> str:
    otp = invoke_otp()
    otp_token = get_otp_token(email, otp, ip)
    otp_data = OtpRequest(email=email, otp=otp, ip=ip, otp_token=otp_token, requested_at=datetime.datetime.now(Var.IST))
    await Var.db.add_otp(otp_data)
    return otp


async def send_otp_via_email(email, otp):
    await Var.EMAIL_SERVER.send_email(email, f"{otp} is your ProductGPT OTP",
                                      email_template.format(otp=otp, year=datetime.datetime.now(Var.IST).year))


async def send_otp_via_sms(phone_number):
    url = (
        f"https://cpaas.messagecentral.com/verification/v3/send"
        f"?countryCode=91"
        f"&customerId={Var.OTP_CID}"
        f"&flowType=SMS"
        f"&mobileNumber={phone_number}"
        f"&expiry=600")
    headers = {
        'authToken': Var.OTP_AUTH_TOKEN
    }
    print(url, headers)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                res = await response.json()

                verification_id = res.get('data').get('verificationId')
                if verification_id:
                    return verification_id
            raise StandardException(400, "Failed to send OTP via SMS", message="Failed to send OTP via SMS")


async def validate_otp(phone_number, verification_id, code):
    url = (
        f"https://cpaas.messagecentral.com/verification/v3/validateOtp"
        f"?countryCode=91"
        f"&mobileNumber={phone_number}"
        f"&verificationId={verification_id}"
        f"&customerId={Var.OTP_CID}"
        f"&code={code}"
    )
    headers = {
        'authToken': Var.OTP_AUTH_TOKEN
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                res = await response.json()
                print(res)
                status_code = res.get('responseCode')
                if status_code == 200:
                    return True
                return False
    except Exception as ex:
        print(ex)
        return False
