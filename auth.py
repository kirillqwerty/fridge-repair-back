"""JWT-based admin authentication."""
import os
import time
import logging
import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from storage import read_json, write_json, ensure_seeded

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def _secret() -> str:
    return os.environ.get("JWT_SECRET", "change-me-default-secret")


def _alg() -> str:
    return os.environ.get("JWT_ALG", "HS256")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def create_token(username: str, ttl_hours: int = 24) -> str:
    payload = {
        "sub": username,
        "iat": int(time.time()),
        "exp": int(time.time()) + ttl_hours * 3600,
    }
    return jwt.encode(payload, _secret(), algorithm=_alg())


def decode_token(token: str) -> dict:
    return jwt.decode(token, _secret(), algorithms=[_alg()])


async def get_admin_user() -> dict:
    """Get the admin user record, seeding if missing."""
    username = os.environ.get("ADMIN_USERNAME", "admin")
    default_pwd = os.environ.get("ADMIN_DEFAULT_PASSWORD", "admin123")
    seed = {"username": username, "password_hash": hash_password(default_pwd)}
    current = await read_json("users", None)
    if not current:
        await write_json("users", seed)
        logger.info("[auth] seeded default admin user: %s", username)
        return seed
    return current


async def set_admin_password(new_password: str) -> None:
    user = await get_admin_user()
    user["password_hash"] = hash_password(new_password)
    await write_json("users", user)


async def authenticate(username: str, password: str) -> dict | None:
    user = await get_admin_user()
    if user.get("username") != username:
        return None
    if not verify_password(password, user.get("password_hash", "")):
        return None
    return user


async def require_admin(token: str | None = Depends(oauth2_scheme)) -> dict:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не авторизован")
    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Срок сессии истёк")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен")
    user = await get_admin_user()
    if payload.get("sub") != user.get("username"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
    return {"username": user["username"]}
