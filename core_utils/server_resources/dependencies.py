from typing import Union
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from .database.users_db import UserDatabase
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


# to get a string like this run:
# openssl rand -hex 32
# TODO: Create a unique SECRET_KEY in the .config
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


user_database = UserDatabase()
users_dict = user_database.get_users()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthLevels:
    NO_AUTH = 0
    BASIC = 1
    ADMIN = 2


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    # email: Union[str, None] = None
    full_name: Union[str, None] = None
    auth_level: int = 0


class UserInDB(User):
    password_hash: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_dict, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_admin_user(
        current_user: User = Depends(get_current_user)):
    if current_user.auth_level < AuthLevels.ADMIN:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_user_auth_level(
        current_user: User = Depends(get_current_user)):
    return current_user.auth_level

async def current_user_is_admin(
    auth_level: int = Depends(get_current_user_auth_level)):
    return auth_level == AuthLevels