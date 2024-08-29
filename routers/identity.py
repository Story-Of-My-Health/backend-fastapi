from typing import Callable, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import Session

from db_initializer import get_db
from models.identity import SEXE_CHOICES
from schemas.identity import CreateIdentitySchema, IdentitySchema
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


def valid_parent_sexe(session: Session, payload: CreateIdentitySchema):
    if payload.father_id:
        father: IdentitySchema = get_identity(
            lambda: identity_db_services.get_identity_by_id(session, payload.father_id),
            error_msg=f"Father identity not found",
        )
        return father.sexe.value == SEXE_CHOICES.male.value

    if payload.mother_id:
        mother: IdentitySchema = get_identity(
            lambda: identity_db_services.get_identity_by_id(session, payload.mother_id),
            error_msg=f"Mother identity not found",
        )
        return mother.sexe.value == SEXE_CHOICES.female.value

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
    identity_key: Optional[str] = None, session: Session = Depends(get_db)
):
    if identity_key != None:
        return get_identity(
            lambda: identity_db_services.get_identity_by_key(session, identity_key),
            error_msg=f'Identity with identity key "{identity_key}" not found',
        )

    return identity_db_services.get_identities(session)


@router.get("/{id}", response_model=List[IdentitySchema] | IdentitySchema)
def get_identity_by_id(id: int, session: Session = Depends(get_db)):
    return get_identity(
        lambda: identity_db_services.get_identity_by_id(session, id),
        error_msg=f"Identity with id {id} not found",
    )
