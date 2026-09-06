from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.database.session import get_db
from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.schemas import LoginRequest, TokenResponse
from app.modules.auth.service import AuthService
from app.modules.users.schemas import UserPublic
from app.modules.users.service import to_public_user

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    session: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> TokenResponse:
    return AuthService(session, settings).login(credentials)


@router.get("/me", response_model=UserPublic)
def read_current_user(current_user: CurrentUser) -> UserPublic:
    return to_public_user(current_user)
