from typing import Callable, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import Session

from db_initializer import get_db
from models.identity import SEXE_CHOICES, STATUS_CHOICES
from schemas.identity import CreateIdentitySchema, IdentityQuerySchema, IdentitySchema
from services.db import identity as identity_db_services

router = APIRouter(prefix="/identity", tags=["identity"])


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


def valid_parent_sexe(session: Session, payload: CreateIdentitySchema):
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
def create_identity(
    payload: CreateIdentitySchema = Body(), session: Session = Depends(get_db)
):
    if valid_parent_sexe(session, payload):
        return identity_db_services.create_identity(session, payload)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid parent sexe",
    )


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
