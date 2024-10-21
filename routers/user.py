from typing import Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import exc
from sqlalchemy.orm import Session

from auth2.auth_schema import verify_token
from db_initializer import get_db
from models import user as user_model
from schemas.user import (
    CreateDoctorProfileSchema,
    CreateMedicalHistory,
    CreateUserSchema,
    DecodedToken,
    DoctorProfileBaseSchema,
    DoctorProfileSchema,
    MedicalHistorySchema,
    UserSchema,
)
from services.db import user as user_db_services

router = APIRouter()


class SetTypePayload(BaseModel):
    user_type: user_model.USER_TYPE_CHOICES


class SetMedicalHistoryStatusPayload(BaseModel):
    status: user_model.MEDICAL_HISTORY_STATUS


class GetProfileByKeywordPayload(BaseModel):
    keywords: List[str]


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


@router.post("/user/set-type/{id}", response_model=UserSchema, tags=["User"])
def set_user_type(
    id: int,
    payload: SetTypePayload = Body(),
    current_user: DecodedToken = Depends(verify_token),
    session: Session = Depends(get_db),
):
    # Comment this for creation of first admin
    if current_user.user_type != user_model.USER_TYPE_CHOICES.admin.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You cannot perform this action",
        )
    return user_db_services.set_user_type(session, id, payload.user_type)


@router.post(
    "/user/doctor-profile/",
    response_model=DoctorProfileSchema,
    tags=["User", "Doctor"],
)
def create_doctor_profile(
    payload: CreateDoctorProfileSchema = Body(),
    current_user: DecodedToken = Depends(verify_token),
    session: Session = Depends(get_db),
):
    if current_user.user_type != user_model.USER_TYPE_CHOICES.doctor.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only user with user_type = 'doctor' can perform this action",
        )

    keywords = []

    for keyword in payload.keywords:
        db_keyword = session.query(user_model.Keyword).filter_by(name=keyword).first()

        if db_keyword is None:
            db_keyword = user_model.Keyword(name=keyword)
            session.add(db_keyword)
            session.commit()
            session.refresh(db_keyword)

        keywords.append(db_keyword)

    new_profile = user_db_services.create_doctor_profile(
        session,
        profile=DoctorProfileBaseSchema(
            address=payload.address,
            establishment=payload.establishment,
            keywords=keywords,
            title=payload.title,
        ),
        user_id=current_user.id,
        keywords=keywords,
    )

    return new_profile


@router.get(
    "/user/doctor-profile/{id}",
    response_model=DoctorProfileSchema,
    tags=["User", "Doctor"],
)
def get_doctor_profile_by_id(
    id: int,
    _: DecodedToken = Depends(verify_token),
    session: Session = Depends(get_db),
):
    return user_db_services.get_doctor_profile_by_id(session, id)


@router.post(
    "/user/doctor-profile/query",
    response_model=List[DoctorProfileSchema],
    tags=["User", "Doctor"],
)
def get_doctor_profile_by_keyword(
    payload: GetProfileByKeywordPayload = Body(),
    _: DecodedToken = Depends(verify_token),
    session: Session = Depends(get_db),
):
    return user_db_services.get_doctor_profile_by_keyword(session, payload.keywords)


@router.post(
    "/user/medical-history/",
    response_model=MedicalHistorySchema,
    tags=["User", "Medical history"],
)
def create_medical_history(
    payload: CreateMedicalHistory = Body(),
    current_user: DecodedToken = Depends(verify_token),
    session: Session = Depends(get_db),
):
    if current_user.user_type != user_model.USER_TYPE_CHOICES.doctor.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only user with user_type = 'doctor' can perform this action",
        )
    return user_db_services.create_medical_history(session, payload, current_user.id)


@router.get(
    "/user/medical-history/{id}",
    response_model=MedicalHistorySchema,
    tags=["User", "Medical history"],
)
def get_medical_history_by_id(
    id: int,
    _: DecodedToken = Depends(verify_token),
    session: Session = Depends(get_db),
):
    return user_db_services.get_medical_history_by_id(session, id)


@router.get(
    "/user/medical-history/identity/{id}",
    response_model=List[MedicalHistorySchema],
    tags=["User", "Medical history"],
)
def get_medical_history_by_identity_id(
    id: int,
    _: DecodedToken = Depends(verify_token),
    session: Session = Depends(get_db),
):
    return user_db_services.get_medical_history_by_patient_id(session, id)


@router.get(
    "/user/medical-history/created-by/{id}",
    response_model=List[MedicalHistorySchema],
    tags=["User", "Medical history"],
)
def get_medical_history_by_creator_id(
    id: int,
    _: DecodedToken = Depends(verify_token),
    session: Session = Depends(get_db),
):
    return user_db_services.get_medical_history_by_creator_id(session, id)


@router.post(
    "/user/medical-history/set-status/{id}",
    response_model=MedicalHistorySchema,
    tags=["User", "Medical history"],
)
def set_user_type(
    id: int,
    payload: SetMedicalHistoryStatusPayload = Body(),
    current_user: DecodedToken = Depends(verify_token),
    session: Session = Depends(get_db),
):
    if current_user.user_type != user_model.USER_TYPE_CHOICES.doctor.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You cannot perform this action",
        )

    medical_history = (
        session.query(user_model.MedicalHistory)
        .filter(user_model.MedicalHistory.id == id)
        .one_or_none()
    )

    if medical_history is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Medical with id {id} does not exist",
        )

    medical_history.status = payload.status
    session.commit()
    session.refresh(medical_history)

    return medical_history
