from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import exc
from sqlalchemy.orm import Session

from db_initializer import get_db
from models import user as user_model
from schemas.user import CreateUserSchema, UserLoginSchema, UserSchema
from services.db import user as user_db_services

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/signup", response_model=UserSchema)
def signup(payload: CreateUserSchema = Body(), session: Session = Depends(get_db)):
    """Processes request to register user account."""
    payload.hashed_password = user_model.User.hash_password(payload.hashed_password)
    try:
        user = user_db_services.create_user(session, user=payload)
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    return user


@router.post("/login", response_model=Dict)
def login(
    payload: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)
):
    """Processes user's authentication and returns a token
    on successful authentication.

    request body:

    - username: Unique identifier for a user e.g email,
                phone number, name

    - password:
    """
    try:
        user: user_model.User = user_db_services.get_user(
            session=session, username=payload.username
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user credentials"
        )

    is_validated: bool = user.validate_password(payload.password)
    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user credentials"
        )

    return user.generate_token()
