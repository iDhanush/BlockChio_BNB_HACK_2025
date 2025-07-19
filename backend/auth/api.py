from auth import schemas
from fastapi import APIRouter
from auth.schemas import WalletAuthPayload
from auth.auth import wallet_auth
from fastapi import Response

auth_router = APIRouter(tags=['auth'], prefix='/v1/auth')


@auth_router.post('/user/wallet-auth')
async def google_auth_handler(wallet_payload: WalletAuthPayload, response: Response):
    user, token, refresh_token = await wallet_auth(wallet_payload.wallet)

    # Set cookies
    response.set_cookie(
        key="aTok",
        value=token,
        httponly=True,
        secure=True,  # Use False for local dev if not HTTPS
        samesite="none",  # Or "Strict"/"None" as needed
        max_age=60 * 60 * 24 * 365  # 1 year for refresh token
    )
    response.set_cookie(
        key="rTok",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 60 * 24 * 365  # 1 year for refresh token
    )

    return {
        "status": "success",
        "data": schemas.Token(
            access_token=token,
            refresh_token=refresh_token,
            profile=user.model_dump()
        ),
        "message": "Login successful"
    }
