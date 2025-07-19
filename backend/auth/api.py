import datetime
from globar_vars import Var
from auth import schemas
from fastapi import Request
from fastapi import APIRouter, Depends
from responses import StandardResponse, StandardException
from auth.schemas import EmailAuthPayload, OtpAttempt, GoogleAuthPayload, PhoneAuthPayload
from auth.auth import get_token, get_access_token, google_auth, email_auth, generate_otp, send_otp_via_email, \
    send_otp_via_sms, phone_auth, temp_auth, get_current_user

auth_router = APIRouter(tags=['auth'], prefix='/v1/auth')


@auth_router.post('/user/google-auth')
async def google_auth_handler(google_payload: GoogleAuthPayload):
    temp_user_id = None
    if google_payload.temp_user_token:
        try:
            temp_user = await get_current_user(token=google_payload.temp_user_token)
            temp_user_id = temp_user.user_id
        except:
            pass
    user, token, refresh_token = await google_auth(google_payload.code, google_payload.uri, temp_user_id)
    return StandardResponse(status="success", data=schemas.Token(access_token=token, refresh_token=refresh_token,
                                                                 profile=user.model_dump()),
                            message="Login successful")


@auth_router.post('/user/email-auth')
async def email_auth_handler(email_payload: EmailAuthPayload, request: Request):
    if not email_payload.otp:
        otp = await generate_otp(email=str(email_payload.email), ip=request.client.host)
        await send_otp_via_email(email_payload.email, otp)
        return StandardResponse(status="success", data=None, message="OTP sent successfully")
    temp_user = None
    if email_payload.temp_user_token:
        try:
            temp_user = await get_current_user(token=email_payload.temp_user_token)
        except:
            pass
    otp_attempt = OtpAttempt(email=str(email_payload.email), otp=email_payload.otp, ip=request.client.host,
                             attempted_at=datetime.datetime.now(Var.IST))
    user, token, refresh_token = await email_auth(otp_attempt, temp_user_id=temp_user.user_id)
    return StandardResponse(status="success",
                            data=schemas.Token(access_token=token, refresh_token=refresh_token,
                                               profile=user.model_dump()), message="OTP verified successfully")


@auth_router.post('/user/refresh')
async def refresh_auth(refresh_token: str = Depends(get_token)):
    user, token = await get_access_token(refresh_token)
    return StandardResponse(status="success",
                            data=schemas.RToken(access_token=token, profile=user.model_dump(), user_id=user.user_id),
                            message="Token refreshed successfully")


@auth_router.post('/user/phone-auth')
async def phone_auth_handler(phone_payload: PhoneAuthPayload):
    if not phone_payload.otp:
        verification_id = await send_otp_via_sms(phone_payload.phone)
        if not verification_id:
            raise StandardException(message="Failed to send OTP", status_code=500)
        return StandardResponse(status="success", data={'verification_id': verification_id},
                                message="OTP sent successfully")
    user, token, refresh_token = await phone_auth(phone_payload)
    return StandardResponse(status="success",
                            data=schemas.Token(access_token=token, refresh_token=refresh_token,
                                               profile=user.model_dump()), message="OTP verified successfully")


@auth_router.post('/user/temp-auth')
async def temp_auth_handler():
    user, token, refresh_token = await temp_auth()
    return StandardResponse(status="success",
                            data=schemas.Token(access_token=token, refresh_token=refresh_token,
                                               profile=user.model_dump()), message="Temp user created successfully")
