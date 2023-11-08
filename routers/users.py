from fastapi import APIRouter, Depends
from typing import Annotated
from jose import JWTError, jwt
from ..dependencies import get_current_user, oauth2_scheme
from ..models.models import User
from ..config import SECRET_KEY, ALGORITHM

router = APIRouter(
    tags=["users"],
    dependencies= [Depends(oauth2_scheme)]
)

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/get_token/")
async def read_own_items(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
