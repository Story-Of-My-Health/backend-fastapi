import os
import shutil
import uuid
from typing import Callable, List, Optional

from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import exc
from sqlalchemy.orm import Session

from auth2.auth_schema import verify_token
from db_initializer import get_db
from models.identity import SEXE_CHOICES, STATUS_CHOICES, Identity
from models.user import USER_TYPE_CHOICES
from notifications import notify_client
from schemas.identity import (
    CreateIdentitySchema,
    IdentityQuerySchema,
    IdentitySchema,
    UpdateIdentitySchema,
)
from schemas.notification import (
    NotificationAction,
    NotificationModel,
    NotificationSchema,
)
from schemas.user import DecodedToken
from services.db import identity as identity_db_services

router = APIRouter(prefix="/identity", tags=["identity"])

UPLOAD_DIR = "./static/img"


def generate_uuid_filename(filename: str):
    extension = os.path.splitext(filename)[1]
    return f"{uuid.uuid4()}{extension}"


def get_identity(
    get_fn: Callable,
    error_msg: str,
):
    try:
        identity = get_fn()
    except exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_msg,
        )
    return identity


def set_identity_status(session: Session, id: int, identity_status: STATUS_CHOICES):
    try:
        identity = identity_db_services.set_identity_status(
            session, id, identity_status
        )
    except exc.InvalidRequestError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status can no longer be modified",
        )

    return identity


def valid_parent_sexe(
    session: Session, payload: CreateIdentitySchema | UpdateIdentitySchema
):
    if payload.father_id:
        father: IdentitySchema = get_identity(
            lambda: identity_db_services.get_identity_by_id(session, payload.father_id),
            error_msg=f"Father identity not found",
        )
        return father.sexe == SEXE_CHOICES.male

    if payload.mother_id:
        mother: IdentitySchema = get_identity(
            lambda: identity_db_services.get_identity_by_id(session, payload.mother_id),
            error_msg=f"Mother identity not found",
        )
        return mother.sexe == SEXE_CHOICES.female

    return True


@router.post("/", response_model=IdentitySchema)
async def create_identity(
    payload: CreateIdentitySchema = Body(), session: Session = Depends(get_db)
):
    if not valid_parent_sexe(session, payload):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid parent sexe",
        )

    await notify_client(
        NotificationSchema(
            performer_id=0,
            action=NotificationAction.CREATE.value,
            model=NotificationModel.IDENTITY.value,
        )
    )

    return identity_db_services.create_identity(session, payload)


@router.get("/", response_model=List[IdentitySchema] | IdentitySchema)
def get_identities(
    identity_key: Optional[str] = None,
    sexe: Optional[SEXE_CHOICES] = None,
    first_name: Optional[str] = None,
    address: Optional[str] = None,
    status: Optional[STATUS_CHOICES] = None,
    session: Session = Depends(get_db),
):
    if identity_key:
        return get_identity(
            lambda: identity_db_services.get_identity_by_key(session, identity_key),
            error_msg=f'Identity with identity key "{identity_key}" not found',
        )

    query = IdentityQuerySchema(
        sexe=sexe, first_name=first_name, address=address, status=status
    )
    return identity_db_services.get_identities(session, query)


@router.get("/{id}", response_model=List[IdentitySchema] | IdentitySchema)
def get_identity_by_id(id: int, session: Session = Depends(get_db)):
    return get_identity(
        lambda: identity_db_services.get_identity_by_id(session, id),
        error_msg=f"Identity with id {id} not found",
    )


@router.post("/validate", response_model=IdentitySchema)
def validate_identity(id: int, session: Session = Depends(get_db)):
    return set_identity_status(session, id, STATUS_CHOICES.done)


@router.post("/reject", response_model=IdentitySchema)
def reject_identity(id: int, session: Session = Depends(get_db)):
    return set_identity_status(session, id, STATUS_CHOICES.rejected)


@router.put("/edit/{id}", response_model=IdentitySchema)
async def edit_identity(
    id: int, payload: UpdateIdentitySchema = Body(), session: Session = Depends(get_db)
):
    if not valid_parent_sexe(session, payload):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid parent sexe",
        )

    try:
        identity = identity_db_services.update_identity(session, id, payload)
    except exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Identity with id {id} does not exist or its status is still pending or rejected",
        )

    await notify_client(
        NotificationSchema(
            performer_id=0,
            action=NotificationAction.UPDATE.value,
            model=NotificationModel.IDENTITY.value,
        )
    )

    return identity


@router.post("/upload-img/", response_model=IdentitySchema)
async def upload_profile_img(
    profile_img: UploadFile = File(...),
    session: Session = Depends(get_db),
    current_user: DecodedToken = Depends(verify_token),
):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    filename = generate_uuid_filename(profile_img.filename)
    img_location = os.path.join(UPLOAD_DIR, filename)

    with open(img_location, "wb") as buffer:
        shutil.copyfileobj(profile_img.file, buffer)

    identity = (
        session.query(Identity)
        .filter(Identity.id == current_user.identity_id)
        .one_or_none()
    )

    identity.profile_img = img_location[len("./static/") :]
    session.commit()
    session.refresh(identity)

    return identity
