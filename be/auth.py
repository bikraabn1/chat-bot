from fastapi import APIRouter, Request, HTTPException, status, Response
from fastapi.responses import RedirectResponse
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import httpx

router = APIRouter(prefix="/auth", tags=["auth"])
load_dotenv()

account = {"username": "admin123", "password": "admin123"}


class LoginAccount(BaseModel):
    username: str
    password: str


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")

    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
        return payload
    except JWTError:
        return None


@router.get("/verify-token")
def verify_token(req: Request):
    token = req.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not Authenticated")

    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token Invalid")

    return {"username": payload.get("sub")}


@router.post("/login-jwt")
def login_with_jwt(req: LoginAccount, res: Response):
    if req.username != account["username"] or req.password != account["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = create_access_token({"sub": req.username})

    res.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        expires=timedelta(minutes=30),
    )

    return {"message": "Login Successfully"}


@router.get("/callback")
async def google_callback(request: Request):
    code = request.query_params.get("code")

    if not code:
        return {"error": "no code provided"}

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": f"{os.getenv('BASE_URL')}/auth/callback",
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(token_url, data=data)
        token_resp.raise_for_status()
        tokens = token_resp.json()

        userinfo_resp = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )

        userinfo_resp.raise_for_status()
        userinfo = userinfo_resp.json()

    jwt_token = create_access_token({"sub" : userinfo["email"]})
    response = RedirectResponse(url="http://localhost:5173/")
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=1800
    )

    return response
