from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import exc
from sqlalchemy.orm import Session

from auth2.auth_schema import verify_token
from db_initializer import get_db
from models import user as user_model
from schemas.user import CreateUserSchema, DecodedToken, UserSchema
from services.db import user as user_db_services

router = APIRouter()


@router.post("/auth/signup", response_model=UserSchema, tags=["authentication"])
def signup(payload: CreateUserSchema = Body(), session: Session = Depends(get_db)):
    """Processes request to register user account."""
    payload.hashed_password = user_model.User.hash_password(payload.hashed_password)
    try:
        user = user_db_services.create_user(session, user=payload)
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists or identity does not exist or belongs to existing user",
        )
    return user


@router.post("/auth/login", response_model=Dict, tags=["authentication"])
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


@router.get("/user/me", response_model=UserSchema, tags=["User"])
def get_me(
    current_user: DecodedToken = Depends(verify_token),
    session: Session = Depends(get_db),
):
    return user_db_services.get_user_by_id(session, current_user.id)


class SetTypePayload(BaseModel):
    user_type: user_model.USER_TYPE_CHOICES


@router.post("/user/set-type/{id}", response_model=UserSchema, tags=["User"])
def set_user_as_doctor(
    id: int,
    payload: SetTypePayload = Body(),
    current_user: DecodedToken = Depends(verify_token),
    session: Session = Depends(get_db),
):
    # Comment this for creation of first admin
    if current_user.user_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You cannot perform this action",
        )
    return user_db_services.set_user_type(session, id, payload.user_type)
