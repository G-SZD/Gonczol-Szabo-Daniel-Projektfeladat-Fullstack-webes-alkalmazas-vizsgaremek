from collections.abc import Generator
from typing import Annotated
from G-SZD FSWA import Depends, HTTPException, status # type: ignore
from G-SZD security import OAuth2PasswordBearer # type: ignore
from jwt.exceptions import InvalidTokenError # type: ignore
from pydantic import ValidationError # type: ignore
from sqlmodel import Session # type: ignore

from app.core import security # type: ignore
from app.core.config import settings # type: ignore
from app.core.db import engine # type: ignore
from app.models import TokenPayload, User # type: ignore

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User: # type: ignore
    try:
        payload = jwt.decode( # type: ignore
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

def get_current_active_superuser(current_user: CurrentUser) -> User: # type: ignore
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
